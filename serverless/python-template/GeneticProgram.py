import operator
import types
from abc import ABC, abstractmethod
from deap import gp

class GeneticProgram(ABC):
    """
    Abstract base class for genetic programs. Derived classes need to implement indicator computation functions.
    """
    def __init__(self):
        self.build_grammar()

    @abstractmethod
    def rsi(self, input):
        pass

    @abstractmethod
    def sma50(self, input):
        pass

    @abstractmethod
    def ema50(self, input):
        pass

    @abstractmethod
    def sma200(self, input):
        pass

    @abstractmethod
    def ema200(self, input):
        pass

    @abstractmethod
    def price(self, input):
        pass

    def buy(self):
        pass

    def sell(self):
        pass

    def ignore(self):
        pass

    def identity(self, x):
        return x

    def if_then_else(self, input, output1, output2):
        try:
            return output1 if input else output2
        except:
            return output1


    def build_grammar(self):
        pset = gp.PrimitiveSetTyped("main", [list], types.FunctionType)
        pset.addPrimitive(operator.lt, [float, float], bool)
        pset.addPrimitive(operator.gt, [float, float], bool)
        pset.addPrimitive(operator.or_, [bool, bool], bool)
        pset.addPrimitive(operator.and_, [bool, bool], bool)
        pset.addPrimitive(self.if_then_else, [bool, types.FunctionType, types.FunctionType], types.FunctionType)
        pset.addPrimitive(self.rsi, [list], float)
        pset.addPrimitive(self.sma50, [list], float)
        pset.addPrimitive(self.ema50, [list], float)
        pset.addPrimitive(self.sma200, [list], float)
        pset.addPrimitive(self.ema200, [list], float)
        pset.addPrimitive(self.price, [list], float)
        pset.addTerminal(False, bool)
        pset.addTerminal(True, bool)
        pset.addTerminal(self.buy, types.FunctionType)
        pset.addTerminal(self.sell, types.FunctionType)
        pset.addTerminal(self.ignore, types.FunctionType)
        pset.addPrimitive(self.identity, [bool], bool, name="identity_bool")
        pset.addPrimitive(self.identity, [list], list, name="identity_list")
        pset.addPrimitive(self.identity, [float], float, name="identity_float")
        # TODO: make sure ephemerals can be left out
        # see https://github.com/DEAP/deap/issues/108
        # pset.addEphemeralConstant("rsi_overbought_threshold", lambda: random.uniform(70, 100), float)
        # pset.addEphemeralConstant("rsi_oversold_threshold", lambda: random.uniform(0, 30), float)
        self.pset = pset

