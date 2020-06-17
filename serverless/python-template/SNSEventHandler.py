import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import json
from abc import ABC
import boto3
import os
SNS_ARN = os.environ.get('SNS_ARN', "")



class SNSEventException(Exception):
    pass

class SNSMessageException(Exception):
    pass

class ITFSNSException(Exception):
    pass


class AbstractSNSEventHandler(ABC):
    '''
    Base class for ITF Events and Strategies
    triggered by an SNS message
    required
    '''

    sns_event = {}
    sns_subscribe_arn = ""
    sns_publish_topic_prefix = ""
    sns_publish_topic = "" # automatically set, but can be overwritten manually
    sns_client_response = None
    _parameters = None


    def __init__(self, *args, **kwargs):
        if 'sns_event' in kwargs:
            self._sns_event = kwargs['sns_event']  # SNS event that triggered the function
            self.sns_event = self._sns_event       # trigger setter to parse incoming msgs
                                                   # don't really like this, but left it for now
        self.sns_publish_topic_prefix = "itf-sns-sls-event-"


    @property
    def sns_event(self):
        return self._sns_event  # or not the droids we're looking for?

    @sns_event.setter
    def sns_event(self, sns_event):    # former "context" -> all the data is actually in event, not context
        try:
            self.raw_sns_message = sns_event['Records'][0]['Sns']['Message']
        except KeyError as e:
            logger.error("SNS messages not found! Check code and configurations.")


    def emit_sns_message(self, message_data={}):
        # message data must be json serializable and not empty
        if not message_data:
            raise SNSMessageException("message_data is empty or missing!")
        try:
            json.dumps(message_data)
        except Exception as e:
            raise SNSMessageException(str(e))

        sns_subscribed_arn = self.sns_event['Records'][0]['Sns']['TopicArn'] # TODO: perhaps not good to assume we were
                                                                             # invoked via SNS, remove in production?
        logger.info("Received message from SNS ARN {}".format(sns_subscribed_arn))

        if not self.sns_publish_topic.startswith("itf-sns-"):
            # use instance class name
            self.sns_publish_topic = self.sns_publish_topic_prefix
            self.sns_publish_topic += str(self.__class__.__name__).lower()

        if not self.sns_publish_topic.startswith("itf-sns-"):
            raise ITFSNSException("SNS topic must start with 'itf-sns-'")

        logger.debug("using " + SNS_ARN + " as ARN base")
        # sns_publishing_arn = ":".join(SNS_ARN.split(":")[0:-1].append(self.sns_publish_topic))
        sns_publishing_arn = SNS_ARN  # TODO: this is set temporarily, for debug purposes
        logger.info("using " + sns_publishing_arn + " as ARN for publishing")

        logger.info("Publishing message to SNS ARN {}".format(sns_publishing_arn))

        sns_client = boto3.client('sns')
        self.sns_client_response = sns_client.publish(
            TargetArn=sns_publishing_arn,
            Message=json.dumps({'default': json.dumps(message_data)}),
            MessageStructure='json'
        )


#
# EXAMPLE SNS MESSAGE FROM DATA APP ON HEROKU
# {'Records': [{
#     'EventSource': 'aws:sns',
#     'EventVersion': '1.0',
#     'EventSubscriptionArn': 'arn:aws:sns:us-east-1:983584755688:itt-sns-data-core-stage:493ba9a2-52f0-4c12-b1a4-7bdaee803690'
#         ,
#     'Sns': {
#         'Type': 'Notification',
#         'MessageId': 'dc693f13-b8d8-5445-88b1-6c9954471f92',
#         'TopicArn': 'arn:aws:sns:us-east-1:983584755688:itt-sns-data-core-stage'
#             ,
#         'Subject': None,
#         'Message': '[{"source": "binance", "category": "price", "symbol": "ETH/BTC", "value": 0.077133, "timestamp": 1527835230.836},
#
