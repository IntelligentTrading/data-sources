from StrategyHandler import AbstractStrategyHandler
import logging
logger = logging.getLogger('TradingStrategy123')
logger.setLevel(logging.INFO)


class TradingStrategy123(AbstractStrategyHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def make_signal(self) -> int:
        from StrategyHandler import BUY, SELL, IGNORE
        rsi = self.get_indicator("RSI")
        sma = self.get_indicator("SMA")

        if rsi > 70:
            self.signal = BUY
        else:
            self.signal = BUY

        return self.signal


    @property
    def used_indicators(self):
        return ["RSI", "SMA"]


def check_strategy_ABC(event, context):
    logger.info("\n-------------------\n" +
                "Trading Strategy ABC" +
                "\n-------------------")
    logger.info('Event: {e}\nContext: {c}'.format(e=event, c=context))
    try:
        logger.info("initiating objects...............")
        this_trading_strategy = TradingStrategy123(sns_event=event)
        logger.info("running..........................")
        this_trading_strategy.run()
        logger.info("saving...........................")
        this_trading_strategy.save()
    except Exception as e:
        logger.warning("Exception: {}".format(e))
    return


# Use this event for debugging
# event = {'Records':
#             [
#                 {'EventSource': 'aws:sns',
#                  'EventVersion': '1.0',
#                  'EventSubscriptionArn': 'arn:aws:sns:us-east-2:462951922947:sns-lambda-invoker:9a0bc70c-40df-438d-a0a6-d9f52efe48ce',
#                  'Sns':
#                      {'Type': 'Notification',
#                       'MessageId': '7813ef29-8e2b-5279-b548-bce1d92b1e6d',
#                       'TopicArn': 'arn:aws:sns:us-east-2:462951922947:sns-lambda-invoker',
#                       'Subject': None,
#                       'Message': '{"indicators" : {"RSI" : 75, "SMA": 0.0003}, "transaction_currency":"DOGE", "counter_currency":"BTC", "source":0,"resample_period" : 60}',
#                       'Timestamp': '2018-07-17T20:42:40.621Z',
#                       'SignatureVersion': '1',
#                       'Signature': 'koj+J28o82BFeuJXDELEg29UBIQ3qE1ltCNU4aFExE9ZmfJ3p+m4sPVRebXRVG6QObJ6/R8Qy3zyjVEhzIp4OqVs4nywO8Q0VayFlAm6IT4JTVMk4ElCwBM4OjCkiFHOxk+ao4VkfWVibnL1i5r1CjCD4wsaww2VMw7A9A5gm/lxjnkZf7yTcBqKpmthA8e4hywR/lFuIVt4CFaFlckHNb7iHyI6g0UL1ZWDSTaJxN0WlSvBP/TA/lPMxnrIcHPzcFRqarV6p/PMOHFtPGvpUb80zEseHOE41iIAY9j0SeE2c287bXpfqyrxIMJJc4Kt3kgl15MAb6nhlPn5pyoowA==',
#                       'SigningCertUrl': 'https://sns.us-east-2.amazonaws.com/SimpleNotificationService-ac565b8b1a6c5d002d285f9598aa1d9b.pem',
#                       'UnsubscribeUrl': 'https://sns.us-east-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-2:462951922947:sns-lambda-invoker:9a0bc70c-40df-438d-a0a6-d9f52efe48ce',
#                       'MessageAttributes': {}}}]}

# invoke to debug locally (up to SNS publishing)
# check_strategy_ABC(event, None)

# publish this msg to the invoking SNS topic to test the function:
# {"indicators" : {"RSI" : 75, "SMA": 0.0003}, "transaction_currency":"DOGE", "counter_currency":"BTC", "source":0,"resample_period" : 60}