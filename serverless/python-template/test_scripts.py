from StrategyHandler import AbstractStrategyHandler
from TradingStrategy123 import TradingStrategy123

test_json = {"Records": [
  {
    "EventSource": "aws:sns",
    "EventVersion": "1.0",
    "EventSubscriptionArn": "arn:aws:sns:us-east-1:983584755688:itt-sns-data-core-stage:493ba9a2-52f0-4c12-b1a4-7bdaee803690"
        ,
    "Sns": {
        "Type": "Notification",
        "MessageId": "dc693f13-b8d8-5445-88b1-6c9954471f92",
        "TopicArn": "arn:aws:sns:us-east-1:983584755688:itt-sns-data-core-stage"
            ,
        "Subject": "None",
        "Message": [{"source": "binance", "category": "price", "symbol": "ETH/BTC", "value": 0.077133, "timestamp": 1527835230.836}]
    }
  }
]
}

# def test1():
abh = AbstractStrategyHandler()
d = abh.get_indicator("RSI")
print(d)

ts123 = TradingStrategy123(sns_event=test_json)
ts123.emit_sns_message({"hello":"world"})
# ts123.run()
# ts123.save()
