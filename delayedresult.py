 #!/usr/bin/python
 # coding: utf-8

from pickle import loads, dumps
from redis import Redis
from uuid import uuid4

import time

QUEUE_KEY = 'coffee_queue'

redis = Redis()

class DelayedResult(object):
    def __init__(self, key):
        self.key = key
        self._rv = None

    @property
    def return_value(self):
        if self._rv is None:
            rv = redis.get(self.key)
            if rv is not None:
                self._rv = loads(rv)
        return self._rv


def now():
    return int(time.mktime(time.gmtime()))


def queuefunc(f):
    def delay(seconds, *args, **kwargs):
        qkey = QUEUE_KEY
        key = '%s:result:%s' % (qkey, str(uuid4()))
        s = dumps((f, key, args, kwargs))
        redis.zadd(QUEUE_KEY, s, now() + seconds)
        return DelayedResult(key)
    f.delay = delay
    return f


def queue_daemon(rv_ttl=500):
    clear_queue()     # remove any old jobs first
    while 1:
        jobs = redis.zrangebyscore(QUEUE_KEY, 0, now())
        for job in jobs:
            func, key, args, kwargs = loads(job)
            print "Executing job: %s" % func
            try:
                rv = func(*args, **kwargs)
            except Exception, e:
                rv = e
            if rv is not None:
                redis.set(key, dumps(rv))
                redis.expire(key, rv_ttl)

            redis.zrem(QUEUE_KEY, job)


def clear_queue():
    redis.delete(QUEUE_KEY)


'''
def queuefunc(f):
    def delay(*args, **kwargs):
        qkey = QUEUE_KEY
        key = '%s:result:%s' % (qkey, str(uuid4()))
        s = dumps((f, key, args, kwargs))
        redis.rpush(QUEUE_KEY, s)
        return DelayedResult(key)
    f.delay = delay
    return f


def queue_daemon(rv_ttl=500):
    while 1:
        msg = redis.blpop(QUEUE_KEY)
        func, key, args, kwargs = loads(msg[1])
        if func:
            print (func, key)
        try:
            rv = func(*args, **kwargs)
        except Exception, e:
            rv = e
        if rv is not None:
            redis.set(key, dumps(rv))
            redis.expire(key, rv_ttl)
'''

if __name__ == "__main__":
    print "Running background queue..."
    queue_daemon()