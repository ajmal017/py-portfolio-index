from decimal import Decimal
from datetime import date, datetime
from typing import Optional, List, Dict, DefaultDict, Any
from py_portfolio_index.constants import Logger
from py_portfolio_index.models import RealPortfolio, RealPortfolioElement, Money
from py_portfolio_index.common import divide_into_batches
from py_portfolio_index.portfolio_providers.common import PriceCache
from py_portfolio_index.portfolio_providers.base_portfolio import (
    BaseProvider,
    CacheKey,
)
from py_portfolio_index.exceptions import ConfigurationError
from collections import defaultdict
import uuid
from py_portfolio_index.enums import Provider
from functools import lru_cache
from os import environ
from pytz import UTC

FRACTIONAL_SLEEP = 60
BATCH_SIZE = 50

CACHE_PATH = "webull_tickers.json"


def nearest_value(all_historicals, pivot) -> Optional[dict]:
    filtered = [z for z in all_historicals if z]
    if not filtered:
        return None
    return min(
        filtered,
        key=lambda x: abs(
            datetime.strptime(x["begins_at"], "%Y-%m-%dT%H:%M:%SZ").date() - pivot
        ),
    )


def nearest_multi_value(
    symbol: str, all_historicals, pivot: Optional[date] = None
) -> Optional[Decimal]:
    filtered = [z for z in all_historicals if z and z["symbol"] == symbol]
    if not filtered:
        return None
    if pivot is not None:
        lpivot = pivot or date.today()
        closest = min(
            filtered,
            key=lambda x: abs(
                datetime.strptime(x["begins_at"], "%Y-%m-%dT%H:%M:%SZ").date() - lpivot
            ),
        )
    else:
        closest = filtered[0]
    if closest:
        value = closest.get("last_trade_price", closest.get("high_price", None))
        return Decimal(value)
    return None


class InstrumentDict(dict):
    def __init__(self, refresher, *args):
        super().__init__(*args)
        self.refresher = refresher

    def __missing__(self, key):
        mapping = self.refresher()
        self.update(mapping)
        if key in self:
            return self[key]
        raise ValueError(f"Could not find instrument {key} after refresh")


class WebullProvider(BaseProvider):
    """Provider for interacting with stocks held in
    Webull
    """

    PROVIDER = Provider.WEBULL
    SUPPORTS_BATCH_HISTORY = 0
    PASSWORD_ENV = "WEBULL_PASSWORD"
    USERNAME_ENV = "WEBULL_USERNAME"
    TRADE_TOKEN_ENV = "WEBULL_TRADE_TOKEN"
    DEVICE_ID_ENV = "WEBULL_DEVICE_ID"

    def _get_provider(self):
        from webull import webull  # for paper trading, import 'paper_webull'

        return webull

    def __init__(
        self,
        username: str | None = None,
        password: str | None = None,
        trade_token: str | None = None,
        device_id: str | None = None,
        skip_cache: bool = False,
    ):

        if not username:
            username = environ.get(self.USERNAME_ENV, None)
        if not password:
            password = environ.get(self.PASSWORD_ENV, None)
        if not trade_token:
            trade_token = environ.get(self.TRADE_TOKEN_ENV, None)
        if not device_id:
            device_id = environ.get(self.DEVICE_ID_ENV, None)
        if not (username and password and trade_token and device_id):
            raise ConfigurationError(
                "Must provide ALL OF username, password, trade_token, and device_id arguments or set environment variables WEBULL_USERNAME, WEBULL_PASSWORD, WEBULL_TRADE_TOKEN, and WEBULL_DEVICE_ID "
            )
        webull = self._get_provider()
        self._provider = webull()
        # we must set both of these to have a valid login
        self._provider._did = device_id
        self._provider._headers["did"] = device_id
        BaseProvider.__init__(self)
        self._provider.login(username=username, password=password)

        self._provider.get_trade_token(trade_token)
        account_info: dict = self._provider.get_account()
        if account_info.get("success") is False:
            raise ConfigurationError(f"Authentication is expired: {account_info}")
        self._price_cache: PriceCache = PriceCache(fetcher=self._get_instrument_prices)
        self._local_instrument_cache: Dict[str,str] = {}
        if not skip_cache:
            self._load_local_instrument_cache()

    def _load_local_instrument_cache(self):
        from platformdirs import user_cache_dir
        from pathlib import Path
        import json

        path = Path(user_cache_dir("py_portfolio_index", ensure_exists=True))
        file = path / CACHE_PATH
        if not file.exists():
            self._local_instrument_cache = {}
            return
        with open(file, "r") as f:
            self._local_instrument_cache = json.load(f)
            # corruption guard
            if not isinstance(self._local_instrument_cache, dict):
                self._local_instrument_cache = {}

    def _save_local_instrument_cache(self):
        from platformdirs import user_cache_dir
        from pathlib import Path
        import json

        path = Path(user_cache_dir("py_portfolio_index", ensure_exists=True))
        file = path / CACHE_PATH
        with open(file, "w") as f:
            json.dump(self._local_instrument_cache, f)

    @lru_cache(maxsize=None)
    def _get_instrument_price(
        self, ticker: str, at_day: Optional[date] = None
    ) -> Optional[Decimal]:
        # TODO: determine if there is a bulk API
        webull_id = self._local_instrument_cache.get(ticker)
        if not webull_id:
            # skip the call
            webull_id = str(self._provider.get_ticker(ticker))
            self._local_instrument_cache[ticker] = webull_id
            self._save_local_instrument_cache()
        if at_day:
            historicals = self._provider.get_bars(
                tId=webull_id,
                interval="d1",
                timeStamp=int(
                    datetime(
                        day=at_day.day,
                        month=at_day.month,
                        year=at_day.year,
                        tzinfo=UTC,
                    ).timestamp()
                ),
            )
            return Decimal(value=list(historicals.itertuples())[0].vwap)
        else:
            stored = self._price_cache.get_prices(tickers=[ticker])
            if stored:
                return stored[ticker]
            quotes: dict = self._provider.get_quote(tId=webull_id)
            if not quotes.get("askList"):
                return None
            rval = Decimal(quotes["askList"][0]["price"])
            return rval

    def _buy_instrument(
        self, symbol: str, qty: Optional[float], value: Optional[Money] = None
    ) -> dict:
        from webull import webull
        import requests

        # we should always have this at this point, as we would have had
        # to check price
        rtId:Optional[str] = self._local_instrument_cache.get(symbol)
        if not rtId:
            tId = self._provider.get_ticker(symbol)
            self._local_instrument_cache[symbol] = tId
            self._save_local_instrument_cache()
        else:
            tId = rtId


        def place_order(
            provider: webull,
            tId=tId,
            price=value,
            action="BUY",
            orderType="LMT",
            enforce="GTC",
            quant = qty,
            outsideRegularTradingHour=True,
            stpPrice=None,
            trial_value=0,
            trial_type="DOLLAR",
        ):
            """
            Place an order - redefined here to

            price: float (LMT / STP LMT Only)
            action: BUY / SELL / SHORT
            ordertype : LMT / MKT / STP / STP LMT / STP TRAIL
            timeinforce:  GTC / DAY / IOC
            outsideRegularTradingHour: True / False
            stpPrice: float (STP / STP LMT Only)
            trial_value: float (STP TRIAL Only)
            trial_type: DOLLAR / PERCENTAGE (STP TRIAL Only)
            """

            headers = provider.build_req_headers(
                include_trade_token=True, include_time=True
            )
            data = {
                "action": action,
                "comboType": "NORMAL",
                "orderType": orderType,
                "outsideRegularTradingHour": outsideRegularTradingHour,
                "quantity": quant if orderType == "MKT" else int(quant),
                "serialId": str(uuid.uuid4()),
                "tickerId": tId,
                "timeInForce": enforce,
            }

            # Market orders do not support extended hours trading.
            if orderType == "MKT":
                data["outsideRegularTradingHour"] = False
            elif orderType == "LMT":
                data["lmtPrice"] = float(price)
            elif orderType == "STP":
                data["auxPrice"] = float(stpPrice)
            elif orderType == "STP LMT":
                data["lmtPrice"] = float(price)
                data["auxPrice"] = float(stpPrice)
            elif orderType == "STP TRAIL":
                data["trailingStopStep"] = float(trial_value)
                data["trailingType"] = str(trial_type)
            response = requests.post(
                provider._urls.place_orders(provider._account_id),
                json=data,
                headers=headers,
                timeout=provider.timeout,
            )
            return response.json()

        return place_order(
            self._provider,
            action="BUY",
            price=value,
            quant=qty,
            orderType="MKT",
            enforce="DAY",
        )

    def buy_instrument(self, ticker: str, qty: Decimal, value: Optional[Money] = None):
        if qty:
            float_qty = float(qty)
            import math

            if float_qty > 1:
                remainder_part, int_part = math.modf(float_qty)

                orders = [int(int_part), round(remainder_part, 4)]
            else:
                orders = [float_qty]        
            orders_kwargs_list = [{'qty':order, 'value':None} for order in orders]
        else:
            orders_kwargs_list = [{'qty':None, 'value':value}]
        for order_kwargs in orders_kwargs_list:
            output = self._buy_instrument(ticker, **order_kwargs)
            msg = output.get("msg")
            if not output.get("success"):
                if msg:
                    Logger.error(msg)
                    if 'Your session has expired' in str(msg):
                        raise ConfigurationError(msg)
                    raise ValueError(msg)
                Logger.error(output)
                raise ValueError(output)
        return True

    def get_unsettled_instruments(self) -> set[str]:
        """We need to efficiently bypass
        paginating all orders if possible
        so just check the account info for if there
        is any cash held for orders first"""
        orders = self._provider.get_current_orders()
        return set(item['ticker']["symbol"] for item in orders)

    def _get_stock_info(self, ticker: str) -> dict:
        info = self._provider.get_ticker_info(ticker)
        # matches = self._provider.find_instrument_data(ticker)
        # for match in matches:
        #     if match["symbol"] == ticker:
        #         return {
        #             "name": match["simple_name"],
        #             "exchange": match["exchange"],
        #             "market": match["market"],
        #             "country": match["country"],
        #             "tradable": bool(match["tradable"]),
        #         }
        return info

    def get_holdings(self)->RealPortfolio:
        accounts_data = self._get_cached_value(
            CacheKey.ACCOUNT, callable=self._provider.get_portfolio
        )
        my_stocks = self._get_cached_value(
            CacheKey.POSITIONS, callable=self._provider.get_positions
        )
        unsettled = self._get_cached_value(
            CacheKey.UNSETTLED, callable=self.get_unsettled_instruments
        )

        pre = {}
        symbols = []
        for row in my_stocks:
            local: Dict[str, Any] = {}
            local["units"] = row["position"]
            # instrument_data = self._provider.get_instrument_by_url(row["instrument"])
            ticker = row["ticker"]["symbol"]
            local["ticker"] = ticker
            symbols.append(ticker)
            local["value"] = 0
            local["weight"] = 0
            pre[ticker] = local
        prices = self._price_cache.get_prices(symbols)
        total_value = Decimal(0.0)
        for s in symbols:
            if not prices[s]:
                continue
            total_value += prices[s] * Decimal(pre[s]["units"])
        final = []
        for s in symbols:
            local = pre[s]
            value = Decimal(prices[s] or 0) * Decimal(
                pre[s]["units"]
            )
            local["value"] = Money(value=value)
            local["weight"] = value / total_value
            local["unsettled"] = s in unsettled
            final.append(local)
        out = [RealPortfolioElement(**row) for row in final]
        cash = Decimal(accounts_data["cashBalance"])
        return RealPortfolio(holdings=out, cash=Money(value=cash), provider=self)

    def get_instrument_prices(self, tickers: List[str], at_day: Optional[date] = None):
        return self._price_cache.get_prices(tickers=tickers, date=at_day)

    def _get_instrument_prices(
        self, tickers: List[str], at_day: Optional[date] = None
    ) -> Dict[str, Optional[Decimal]]:
        batches: List[Dict[str, Optional[Decimal]]] = []
        for list_batch in divide_into_batches(tickers, 1):
            # TODO: determine if there is a bulk API
            ticker: str = list_batch[0]
            webull_id = self._local_instrument_cache.get(ticker)
            if not webull_id:
                # skip the call
                webull_id = str(self._provider.get_ticker(ticker))
                self._local_instrument_cache[ticker] = webull_id
                self._save_local_instrument_cache()
            if at_day:
                historicals = self._provider.get_bars(
                    stock=ticker,
                    interval="d1",
                    timeStamp=int(
                        datetime(
                            day=at_day.day,
                            month=at_day.month,
                            year=at_day.year,
                            tzinfo=UTC,
                        ).timestamp()
                    ),
                )
                batches.append(
                    {ticker: Decimal(value=list(historicals.itertuples())[0].vwap)}
                )
            else:
                quotes = self._provider.get_quote(tId=webull_id)
                if not quotes.get("askList"):
                    rval = None
                else:
                    rval = Decimal(quotes["askList"][0]["price"])
                batches.append({ticker: rval})
        prices: Dict[str, Optional[Decimal]] = {}
        for fbatch in batches:
            prices = {**prices, **fbatch}
        return prices

    def get_profit_or_loss(self, include_dividends: bool = True) -> Money:
        my_stocks = self._get_cached_value(
            CacheKey.POSITIONS, callable=self._provider.get_positions
        )
        pls: List[Money] = []
        for x in my_stocks:
            pl = Money(value=Decimal(x["unrealizedProfitLoss"]))
            pls.append(pl)
        _total_pl = sum(pls)  # type: ignore
        if not include_dividends:
            return Money(value=_total_pl)
        return Money(value=_total_pl) + sum(self._get_dividends().values())

    def _get_dividends(self) -> DefaultDict[str, Money]:
        dividends:dict = self._provider.get_dividends()
        dlist = dividends.get('dividendList', [])
        base = []
        for item in dlist:
            base.append({'value':Money(value=Decimal(item['dividendAmount'])), 'ticker':item['tickerTuple']['symbol']})
        final = defaultdict(lambda: Money(value=0))
        for item in base:
            final[item['ticker']] += item['value']
        return final


class WebullPaperProvider(WebullProvider):
    PROVIDER = Provider.WEBULL_PAPER
    PASSWORD_ENV = "WEBULL_PAPER_PASSWORD"
    USERNAME_ENV = "WEBULL_PAPER_USERNAME"
    TRADE_TOKEN_ENV = "WEBULL_PAPER_TRADE_TOKEN"
    DEVICE_ID_ENV = "WEBULL_PAPER_DEVICE_ID"

    def _get_provider(self):
        from webull import paper_webull

        return paper_webull
