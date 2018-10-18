import json
import logging
from apps.TA import TAException, JAN_1_2017_TIMESTAMP
from settings.redis_db import database, set_of_known_sets_in_redis
from apps.TA.storages.abstract.key_value import KeyValueStorage

logger = logging.getLogger(__name__)


class StorageException(TAException):
    pass


class TimeseriesException(TAException):
    pass


class TimeseriesStorage(KeyValueStorage):
    """
    stores things in a sorted set unique to each ticker and exchange
    todo: split the db by each exchange source

    """
    class_describer = "timeseries"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 'timestamp' REQUIRED, VALIDATE
        try:
            self.unix_timestamp = int(kwargs['timestamp'])  # int eg. 1483228800
        except KeyError:
            raise TimeseriesException("timestamp required for TimeseriesStorage objects")
        except ValueError:
            raise TimeseriesException(
                "timestamp must be castable as integer, received {ts}".format(
                    ts=kwargs.get('timestamp')))
        except Exception as e:
            raise StorageException(str(e))

        if self.unix_timestamp < JAN_1_2017_TIMESTAMP:
            raise TimeseriesException("timestamp before January 1st, 2017")

    def save_own_existance(self, describer_key=""):
        self.describer_key = describer_key or f'{self.__class__.class_describer}:{self.get_db_key()}'

        if self.describer_key not in set_of_known_sets_in_redis:
            set_of_known_sets_in_redis.add(self.describer_key)
            database.sadd("sorted_sets", self.describer_key)

    @classmethod
    def score_from_timestamp(cls, timestamp) -> float:
        return round(float(timestamp - JAN_1_2017_TIMESTAMP) / 300, 3)

    @classmethod
    def timestamp_from_score(cls, score) -> int:
        return int(score * 300) + JAN_1_2017_TIMESTAMP

    @classmethod
    def periods_from_seconds(cls, seconds) -> float:
        return float(seconds) / 300

    @classmethod
    def seconds_from_periods(cls, periods) -> int:
        return int(periods * 300)

    @classmethod
    def query(cls, key: str = "", key_suffix: str = "", key_prefix: str = "",
              timestamp: int = None, periods_range: float = 0.01,
              timestamp_tolerance: int = 299,
              *args, **kwargs) -> dict:

        """
        :param key: the exact redis sortedset key (optional)
        :param key_suffix: suffix on the key  (optional)
        :param key_prefix: prefix on the key (optional)
        :param timestamp: timestamp for most recent value returned  (optional, default returns latest)
        :param periods_range: number of periods desired in results (optional, default 0, so only return 1 value)
        :param timestamp_tolerance: tolerance in seconds on results within timestamp and period range (optional, defualt=299)
        :return: dict(values=[], ...)
        """

        sorted_set_key = cls.compile_db_key(key=key, key_prefix=key_prefix, key_suffix=key_suffix)
        logger.debug(f'query for sorted set key {sorted_set_key}')
        # example key f'{key_prefix}:{cls.__name__}:{key_suffix}'

        # do a quick check to make sure this is a class of things we know is in existence
        describer_key = f'{cls.class_describer}:{sorted_set_key}'
        if describer_key not in set_of_known_sets_in_redis:
            if database.sismember("sorted_sets", describer_key):
                set_of_known_sets_in_redis.add(describer_key)
            else:
                logger.warning("query made for unrecognized class type: " + str(describer_key))
                return {'error': "class type is unrecognized to database",
                        'values': []}

        # if no timestamp, assume query to find the most recent, the last one

        if not timestamp:
            query_response = database.zrange(sorted_set_key, -1, -1)
            try:
                [value, timestamp] = query_response[0].decode("utf-8").split(":")
            except:
                value, timestamp = "unknown", JAN_1_2017_TIMESTAMP

        else:
            # compress timestamps to scores
            target_score = cls.score_from_timestamp(timestamp)
            score_tolerance = cls.periods_from_seconds(timestamp_tolerance)

            query_response = database.zrangebyscore(
                sorted_set_key,
                (target_score - score_tolerance - periods_range),  # min_query_score
                (target_score + score_tolerance)  # max_query_score
            )

        # OLD example query_response = [b'0.06288:1532163247']
        # which came from f'{self.value}:{str(self.unix_timestamp)}'

        # NEW example query_response = [b'0.06288:1532163247']
        # which came from f'{self.value}:{str(score)}' where score = (self.timestamp-JAN_1_2017_TIMESTAMP)/300

        return_dict = {
            'values': [],
            'values_count': 0,
            'timestamp': timestamp,
            'earliest_timestamp': timestamp,
            'latest_timest': timestamp,
            'periods_range': periods_range or 1,
            'period_size': 300,
        }

        if not len(query_response):
            return return_dict

        try:
            return_dict['values_count'] = len(query_response)

            if len(query_response) < periods_range:
                return_dict["warning"] = "fewer values than query's periods_range"
                logger.info("Sorry we couldn't find enough values for you :(")
                # todo: add buffer values? no, let the receiver solve their own problem
                # todo: but perhaps publish an alert to create missing values around this timestamp

            values = [value_score.decode("utf-8").split(":")[0] for value_score in query_response]
            scores = [value_score.decode("utf-8").split(":")[1] for value_score in query_response]
            #  todo: double check that [-1] in list is most recent timestamp

            return_dict.update({
                'values': values,
                'earliest_timestamp': cls.timestamp_from_score(scores[0]),
                'latest_timest': cls.timestamp_from_score(scores[-1]),
            })

        except IndexError:
            return return_dict

        except Exception as e:
            logger.error("redis query problem: " + str(e))
            raise TimeseriesException(str(e))  # wtf happened?

    def save(self, publish=False, pipeline=None, *args, **kwargs):
        if not self.value:
            raise StorageException("no value set, nothing to save!")
        if not self.force_save:
            # validate some rules here?
            pass

        self.save_own_existance()

        z_add_key = f'{self.get_db_key()}'  # set key name
        z_add_score = f'{self.score_from_timestamp(self.unix_timestamp)}'  # timestamp as score (int or float)
        z_add_name = f'{self.value}:{z_add_score}'  # item unique value
        z_add_data = {"key": z_add_key, "name": z_add_name, "score": z_add_score}  # key, score, name
        logger.debug(f'saving data with args {z_add_data}')

        if pipeline is not None:
            logger.debug("added command to redis pipeline")
            if publish:
                pipeline = pipeline.publish(self.__class__.__name__, json.dumps(z_add_data))
            return pipeline.zadd(*z_add_data.values())

        else:
            logger.debug("no pipeline, executing zadd command immediately.")
            response = database.zadd(*z_add_data.values())
            if publish:
                database.publish(self.__class__.__name__, json.dumps(z_add_data))
            return response

    def get_value(self, *args, **kwargs):
        TimeseriesException("function not yet implemented! ¯\_(ツ)_/¯ ")
        pass



def round_sig_figs(value, sig_figs):
    value = float(value)
    non_decimal_place = len(str(int(value)))
    # decimal_places = max(len(str(value % 1))-2, 0)

    if value < 0:
        distance_from_decimal = 0
        for char in str(value):
            if char is ".": continue
            elif int(char) > 0: break
            else: distance_from_decimal += 1
        return round(value, (distance_from_decimal+sig_figs))
    else:
        return round(value, (sig_figs-non_decimal_place))



"""
We can scan the newest or oldest event ids with ZRANGE 4,
maybe later pulling the events themselves for analysis.

We can get the 10 or even 100 events immediately
before or after a timestamp with ZRANGEBYSCORE
combined with the LIMIT argument.

We can count the number of events that occurred
in a specific time period with ZCOUNT.

https://www.infoq.com/articles/redis-time-series
"""
