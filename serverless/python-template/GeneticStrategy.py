from StrategyHandler import AbstractStrategyHandler
import logging
from deap import gp

from GeneticProgram import GeneticProgram
logger = logging.getLogger('TradingStrategy123')
logger.setLevel(logging.INFO)


class GeneticStrategy(AbstractStrategyHandler, GeneticProgram):
    """"
    A lambda doge baby.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        GeneticProgram.__init__(self)
        self.individual = kwargs['individual']


    def make_signal(self) -> int:
        from StrategyHandler import BUY, SELL, IGNORE
        doge = gp.compile(self.individual, self.pset)
        outcome = doge([])
        if outcome == self.buy:
            self.signal = BUY
        elif outcome == self.sell:
            self.signal = SELL
        elif outcome == self.ignore:
            self.signal = IGNORE
        else:
            raise Exception("Unknown outcome produced by doge baby... singularity?!?")

        return self.signal

    @property
    def used_indicators(self):
        return ["RSI", "SMA"]  # TODO: add logic to auto-populate from individual

    def rsi(self, input):
        return self.get_indicator("RSI")

    def sma50(self, input):
        return self.get_indicator("SMA")

    def price(self, input):
        return self.get_indicator("price")

    # TODO: implement the methods below once the API supports them
    def ema50(self, input):
        pass

    def sma200(self, input):
        pass

    def ema200(self, input):
        pass


def check_strategy_gp(event, context):
    logger.info("\n-------------------\n" +
                "Trading Strategy GP" +
                "\n-------------------")
    logger.info('Event: {e}\nContext: {c}'.format(e=event, c=context))
    try:
        logger.info("initiating objects...............")
        mock_individual = 'if_then_else(gt(price(ARG0), sma50(ARG0)), if_then_else(gt(17.64793885409774, 84.48578956778925), ' \
                          'if_then_else(True, ignore, ignore), sell), if_then_else(and_(True, False), ' \
                          'if_then_else(True, sell, ignore), if_then_else(True, buy, ignore)))'
        mock_individual = 'if_then_else(gt(rsi(ARG0), sma50(ARG0)), buy, sell)'
        this_trading_strategy = GeneticStrategy(sns_event=event, individual=mock_individual)
        logger.info("running..........................")
        this_trading_strategy.run()
        logger.info("saving...........................")
        this_trading_strategy.save()
    except Exception as e:
        logger.warning("Exception: {}".format(e))
    return


