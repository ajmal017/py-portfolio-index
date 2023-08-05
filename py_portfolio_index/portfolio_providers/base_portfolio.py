from math import floor, ceil
from typing import Dict, Union, Optional, Set, List
from decimal import Decimal
from datetime import date

from py_portfolio_index.common import print_money, print_per, round_up_to_place
from py_portfolio_index.constants import Logger
from py_portfolio_index.enums import RoundingStrategy, Provider
from py_portfolio_index.exceptions import PriceFetchError
from py_portfolio_index.models import Money, OrderPlan, OrderElement
from functools import lru_cache
from py_portfolio_index.models import RealPortfolio


class BaseProvider(object):
    PROVIDER = Provider.DUMMY
    MIN_ORDER_VALUE = Money(value=1)
    MAX_ORDER_DECIMALS = 2
    SUPPORTS_BATCH_HISTORY = 0

    @property
    def valid_assets(self) -> Set[str]:
        return set()

    def _get_instrument_price(self, ticker: str, at_day: Optional[date] = None):
        raise NotImplementedError

    def get_holdings(self) -> RealPortfolio:
        raise NotImplementedError

    def get_instrument_prices(
        self, tickers: List[str], at_day: Optional[date] = None
    ) -> Dict[str, Optional[Decimal]]:
        output = {}
        for ticker in tickers:
            output[ticker] = self.get_instrument_price(ticker, at_day=at_day)
        return output

    @lru_cache(maxsize=None)
    def get_instrument_price(
        self, ticker: str, at_day: Optional[date] = None
    ) -> Optional[Decimal]:
        try:
            return self._get_instrument_price(ticker, at_day)
        except NotImplementedError as e:
            raise e
        except Exception as e:
            raise PriceFetchError(e)

    def buy_instrument(self, ticker: str, qty: Decimal, value:Optional[Decimal] = None) -> bool:
        raise NotImplementedError

    def get_unsettled_instruments(self) -> Set[str]:
        raise NotImplementedError

    def purchase_ticker_value_dict(
        self,
        to_buy: Dict[str, Money],
        purchasing_power: Union[Money, Decimal, int, float],
        plan_only: bool = False,
        fractional_shares: bool = True,
        skip_errored_stocks=False,
        rounding_strategy=RoundingStrategy.CLOSEST,
        ignore_unsettled: bool = True,
    ):
        purchased = Money(value=0)
        purchasing_power_resolved = Money(value=purchasing_power)
        target_value: Money = Money(value=sum([v for k, v in to_buy.items()]))
        diff = Money(value=0)
        if ignore_unsettled:
            unsettled = self.get_unsettled_instruments()
        else:
            unsettled = set()
        break_flag = False
        for key, value in to_buy.items():
            if key in unsettled:
                Logger.info(f"Skipping {key} with unsettled orders.")
                continue
            try:
                raw_price = self.get_instrument_price(key)
                if not raw_price:
                    raise ValueError(f"No price found for this instrument: {key}")
                price: Money = Money(value=raw_price)
                Logger.info(f"got price of {price} for {key}")
            except Exception as e:
                if not skip_errored_stocks:
                    raise e
                else:
                    continue
            if not price:
                price = Money(value=0)
            if price == Money(value=0):
                to_buy_currency = Money(value=0)
            else:
                to_buy_currency = value / price

            if fractional_shares:
                to_buy_units = round(to_buy_currency, 4)
            else:
                if rounding_strategy == RoundingStrategy.CLOSEST:
                    to_buy_units = Money(value=int(round(to_buy_currency, 0)))
                elif rounding_strategy == RoundingStrategy.FLOOR:
                    to_buy_units = Money(value=floor(to_buy_currency))
                elif rounding_strategy == RoundingStrategy.CEILING:
                    to_buy_units = Money(value=ceil(to_buy_currency))
                else:
                    raise ValueError(
                        "Invalid rounding strategy provided with non-fractional shares."
                    )
            if not to_buy_units:
                Logger.info(f"skipping {key} because no units to buy")
                continue
            purchasing = to_buy_units * price

            Logger.info(f"Need to buy {to_buy_units} units of {key}.")
            if (purchasing_power_resolved - purchasing) < Money(value=0):
                Logger.info("Out of money, buying what is possible and exiting")
                break_flag = True
                purchasing = purchasing_power_resolved
                to_buy_units = Decimal(round(purchasing / price, 4).value)
            if to_buy_units > Decimal(0):
                Logger.info(f"going to buy {to_buy_units} of {key}")
                try:
                    if not plan_only:
                        successfully_purchased = self.buy_instrument(key, to_buy_units)
                    if successfully_purchased:
                        purchasing_power_resolved = (
                            purchasing_power_resolved - purchasing
                        )
                        purchased += purchasing
                        diff += abs(value - purchasing)
                        Logger.info(
                            f"bought {to_buy_units} of {key}, {purchasing_power_resolved} left"
                        )
                except Exception as e:
                    print(e)
                    if not skip_errored_stocks:
                        raise e
            if break_flag:
                Logger.info(
                    f"No purchasing power left, purchased {print_money(purchased)} of {print_money(target_value)}."
                )
                break
        Logger.info(
            f"$ diff from ideal for purchased stocks was {print_money(diff)}. {print_per(diff / target_value)} of total purchase goal."
        )

    def handle_order_element(self, element: OrderElement, dry_run: bool = False):
        if element.qty:
            units = Decimal(element.qty)

        elif element.value:
            raw_price = self.get_instrument_price(element.ticker)
            if not raw_price:
                raise ValueError(
                    f"No price found for this instrument: {element.ticker}"
                )
            price: Money = Money(value=raw_price)
            Logger.info(f"got price of {price} for {element.ticker}")
            units = round_up_to_place(
                (element.value / price).value, self.MAX_ORDER_DECIMALS
            )
        else:
            raise ValueError("Order element must have qty or value")
        if not dry_run:
            self.buy_instrument(element.ticker, units, value)
            Logger.info(f"Bought {units} of {element.ticker}")
        else:
            Logger.info(f"Would have bought {units} of {element.ticker}")

    def purchase_order_plan(
        self,
        plan: OrderPlan,
        skip_errored_stocks=False,
        ignore_unsettled: bool = True,
        plan_only: bool = False,
    ):
        if ignore_unsettled:
            unsettled = self.get_unsettled_instruments()
        else:
            unsettled = set()
        for item in plan.to_buy:
            if item.ticker in unsettled:
                Logger.info(f"Skipping {item.ticker} with unsettled orders.")
                continue
            try:
                self.handle_order_element(item, dry_run=plan_only)
            except Exception as e:
                print(e)
                if not skip_errored_stocks:
                    raise e

    def refresh(self):
        pass
