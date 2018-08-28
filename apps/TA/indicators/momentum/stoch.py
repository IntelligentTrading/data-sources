from settings import LOAD_TALIB

if LOAD_TALIB:
    import talib

from apps.TA import HORIZONS
from apps.TA.storages.abstract.indicator import IndicatorStorage
from apps.TA.storages.abstract.indicator_subscriber import IndicatorSubscriber
from apps.TA.storages.data.price import PriceStorage
from settings import logger


class StochStorage(IndicatorStorage):

    def produce_signal(self):
        pass


class StochSubscriber(IndicatorSubscriber):
    classes_subscribing_to = [
        PriceStorage
    ]

    def handle(self, channel, data, *args, **kwargs):

        self.index = self.key_suffix

        if self.index is not 'close_price':
            logger.debug(f'index {self.index} is not `close_price` ...ignoring...')
            return

        new_stoch_storage = StochStorage(ticker=self.ticker,
                                     exchange=self.exchange,
                                     timestamp=self.timestamp)

        for horizon in HORIZONS:
            periods = horizon * 5

            high_value_np_array = self.get_values_array_from_query(
                PriceStorage.query(
                    ticker=self.ticker,
                    exchange=self.exchange,
                    index='high_price',
                    periods_range=periods
                ),
                limit=periods)

            low_value_np_array = self.get_values_array_from_query(
                PriceStorage.query(
                    ticker=self.ticker,
                    exchange=self.exchange,
                    index='low_price',
                    periods_range=periods
                ),
                limit=periods)

            close_value_np_array = self.get_values_array_from_query(
                PriceStorage.query(
                    ticker=self.ticker,
                    exchange=self.exchange,
                    index='close_price',
                    periods_range=periods
                ),
                limit=periods)

            slowk, slowd = talib.STOCH(high_value_np_array, low_value_np_array, close_value_np_array,
                                       fastk_period=horizon*5, slowk_period=horizon*3,
                                       slowk_matype=0, slowd_period=horizon*3, slowd_matype=0)[-1]
            logger.debug(f'saving Stoch value {slowk}, {slowd} for {self.ticker} on {periods} periods')

            new_stoch_storage.periods = periods
            new_stoch_storage.value = f'{slowd}:{slowd}'
            new_stoch_storage.save()
