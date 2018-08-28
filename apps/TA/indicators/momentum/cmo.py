from settings import LOAD_TALIB

if LOAD_TALIB:
    import talib

from apps.TA import HORIZONS
from apps.TA.storages.abstract.indicator import IndicatorStorage
from apps.TA.storages.abstract.indicator_subscriber import IndicatorSubscriber
from apps.TA.storages.data.price import PriceStorage
from settings import logger


class CmoStorage(IndicatorStorage):

    def produce_signal(self):
        pass


class CmoSubscriber(IndicatorSubscriber):
    classes_subscribing_to = [
        PriceStorage
    ]

    def handle(self, channel, data, *args, **kwargs):

        self.index = self.key_suffix

        if self.index is not 'close_price':
            logger.debug(f'index {self.index} is not `close_price` ...ignoring...')
            return

        new_cmo_storage = CmoStorage(ticker=self.ticker,
                                     exchange=self.exchange,
                                     timestamp=self.timestamp)

        for horizon in HORIZONS:
            periods = horizon * 14

            close_value_np_array = self.get_values_array_from_query(
                PriceStorage.query(
                    ticker=self.ticker,
                    exchange=self.exchange,
                    index='close_price',
                    periods_range=periods
                ),
                limit=periods)

            timeperiod = min([len(close_value_np_array), periods])
            cmo_value = talib.CMO(close_value_np_array, timeperiod=timeperiod)[-1]
            logger.debug(f'saving Cmo value {cmo_value} for {self.ticker} on {periods} periods')

            new_cmo_storage.periods = periods
            new_cmo_storage.value = int(float(cmo_value))
            new_cmo_storage.save()
