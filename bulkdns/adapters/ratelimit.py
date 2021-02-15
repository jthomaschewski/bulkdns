from time import time, sleep
from bulkdns import log


class Ratelimiter(object):
    def __init__(self, limit: int, period: int = 300) -> None:
        self.limit = limit
        self.period = period
        self._requests = []

    def enforce_limit(self):
        self._requests.append(time())

        # filter request within period
        self._requests = list(filter(
            lambda a: a > (time() - self.period), self._requests
        ))
        oldest_request_time = min(self._requests)
        sleep_seconds = abs((time() - self.period) - oldest_request_time)

        if len(self._requests) - 1 != self.limit:
            return

        # rate limit reached => sleep
        log.warn(
            'Rate limiting api requests - reached limit of %s requests in the last %s seconds. Waiting %i seconds' %
            (self.limit, self.period, sleep_seconds)
        )
        sleep(sleep_seconds)

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            self.enforce_limit()
            return func(*args, **kwargs)

        return wrapper
