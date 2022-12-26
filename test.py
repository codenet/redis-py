import math
import time

from redis.client import Redis, AsyncWriter
from redis.key_types import KeyCacheProp

def test_async_writer():
    r = Redis()
    r.flushall()

    ar = AsyncWriter()

    for i in range(100):
        ar.set(str(i), i)

    ar.wait_all()

    for i in range(100):
        x = r.get(str(i))
        assert int(x) == i



def bench_async_writer():
    r = Redis()
    r.flushall()

    ar = AsyncWriter()

    def bench(rds):
        for i in range(10000):
            x = math.factorial(i % 5000) + 3 // 7
            rds.set(str(i), x % 100)

    st = time.time()
    bench(ar)
    ar.wait_all()
    ed = time.time()

    print("async writes:", ed - st)

    r.flushall()

    st = time.time()
    bench(r)
    ed = time.time()
    print("sync writes:", ed - st)

    #
    #
    # for i in range(1000):
    #     print(r.get(str(i)))


def test_async_pipelined_writer():
    r = Redis()
    r.flushall()

    p = r.pipeline()

    p.watch("x")
    input("press enter to continue")
    p.multi()
    p.set("a", 2)
    p.get("a")

    print(p.execute())

    # ar = AsyncPipelinedWriter()
    #
    # for i in range(100):
    #     ar.set(str(i), i)
    #
    # ar.execute()
    #
    # ar.wait_all()
    #
    # for i in range(100):
    #     x = r.get(str(i))
    #     assert int(x) == i


if __name__ == "__main__":
    # bench()
    # test_flush()
    # print("test")
    test_async_writer()
    bench_async_writer()


    # class First(object):
    #     def __init__(self):
    #         print("first")
    #
    #
    # class Second():
    #     def __init__(self):
    #         print("second")
    #
    #
    # class Third(First):
    #     def __init__(self):
    #         print("third")
    #
    #
    # class Fourth(Third, Second):
    #     def __init__(self):
    #         super(Third, self).__init__()
    #         print("that's it")
    #
    # f = Fourth()