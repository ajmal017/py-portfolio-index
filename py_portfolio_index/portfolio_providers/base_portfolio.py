from math import floor, ceil
from typing import Dict, Union, Optional, Set
from decimal import Decimal
from datetime import date

from py_portfolio_index.common import print_money, print_per
from py_portfolio_index.constants import Logger
from py_portfolio_index.enums import RoundingStrategy
from py_portfolio_index.exceptions import PriceFetchError
from py_portfolio_index.models import Money
from functools import lru_cache


class BaseProvider(object):
    def _get_instrument_price(self, ticker: str, at_day: Optional[date] = None):
        raise NotImplementedError

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

    def buy_instrument(self, ticker: str, qty: Decimal):
        raise NotImplementedError

    def get_unsettled_instruments(self) -> Set[str]:

        raise NotImplementedError

    def purchase_ticker_value_dict(
        self,
        to_buy: Dict[str, Money],
        purchasing_power: Union[Money, float],
        plan_only: bool = False,
        fractional_shares: bool = True,
        skip_errored_stocks=False,
        rounding_strategy=RoundingStrategy.CLOSEST,
        ignore_unsettled: bool = True,
    ):
        purchased = Money(value=0)
        purchasing_power = Money(value=purchasing_power)
        target_value: Money = sum([v for k, v in to_buy.items()])
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
                price = self.get_instrument_price(key)
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
                to_buy_units = round(to_buy_currency, 4).value
            else:
                if rounding_strategy == RoundingStrategy.CLOSEST:
                    to_buy_units = Decimal(int(round(to_buy_currency, 0)))
                elif rounding_strategy == RoundingStrategy.FLOOR:
                    to_buy_units = Decimal(floor(to_buy_currency))
                elif rounding_strategy == RoundingStrategy.CEILING:
                    to_buy_units = Decimal(ceil(to_buy_currency))
                else:
                    raise ValueError(
                        "Invalid rounding strategy provided with non-fractional shares."
                    )
            if not to_buy_units:
                continue
            purchasing = to_buy_units * price

            Logger.info(f"Need to buy {to_buy_units} units of {key}.")
            if (purchasing_power - purchasing) < Money(value=0):
                break_flag = True
                purchasing = purchasing_power
                to_buy_units = Decimal(round(purchasing / price, 4).value)
            if to_buy_units > Decimal(0):
                Logger.info(f"going to buy {to_buy_units} of {key}")
                try:
                    if not plan_only:
                        self.buy_instrument(key, to_buy_units)
                    purchasing_power = purchasing_power - purchasing
                    purchased += purchasing
                    diff += abs(value - purchasing)
                    Logger.info(
                        f"bought {to_buy_units} of {key}, {purchasing_power} left"
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
