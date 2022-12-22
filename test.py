import math
import time

from redis.client import Redis
from redis.key_types import KeyCacheProp


def bench():
    keys = {"c": KeyCacheProp.WRITE_ONCE}
    r = Redis(host='localhost', key_types=keys)

    r.flushall()

    r.set('x', 'a')
    r.set('x:c', 'a')
    r.get('x:c')

    st = time.time()
    print(r.get('x:c'))
    ed = time.time()
    print((ed - st))

    st = time.time()
    print(r.get('x'))
    ed = time.time()
    print((ed - st))

    print("------------")

    for i in range(10):
        r.hset('y:c', str(i), str(i))
        r.hset('y', str(i), str(i))

    for i in range(10):
        r.hget('y:c', str(i))

    st = time.time()
    r.hget('y:c', '5')
    ed = time.time()
    print((ed - st))

    t1 = ed - st

    st = time.time()
    r.hget('y', '5')
    ed = time.time()
    print((ed - st))

    t2 = ed - st

    print("hget saved:", abs(t2 - t1) * 1000, "ms")

    print("------------")

    st = time.time()
    r.hgetall('y:c')
    ed = time.time()
    print((ed - st))

    t1 = ed - st

    st = time.time()
    r.hgetall('y')
    ed = time.time()
    print((ed - st))

    t2 = ed - st

    print("hgetall saved", abs(t2 - t1) * 1000, "ms")

    print("------------")

    st = time.time()
    r.hmget('y:c', '1', '2', '3', '4')
    ed = time.time()
    print((ed - st) )

    st = time.time()
    r.hmget('y', '1', '2', '3', '4')
    ed = time.time()
    print((ed - st) )

    print("hmget saved", abs(t2 - t1) * 1000, "ms")


def test_flush():
    keys = {"c": KeyCacheProp.WRITE_ONCE}
    r = Redis(host='localhost', key_types=keys)
    r.set("kk:c", "kkk")
    assert r.get("kk:c") is not None
    print(r.get("kk:c"))
    r.flushall()
    assert r.get("kk:c") is None


# def test_async_writer():
#     r = Redis()
#     r.flushall()
#
#     ar = AsyncWriter()
#
#     for i in range(100):
#         ar.set(str(i), i)
#
#     ar.wait_all()
#
#     for i in range(100):
#         x = r.get(str(i))
#         assert int(x) == i



# def bench_async_writer():
#     r = Redis()
#     r.flushall()
#
#     ar = AsyncWriter()
#
#     def bench(rds):
#         for i in range(10000):
#             x = math.factorial(i % 5000) + 3 // 7
#             rds.set(str(i), x % 100)
#
#     st = time.time()
#     bench(ar)
#     ar.wait_all()
#     ed = time.time()
#
#     print("async writes:", ed - st)
#
#     r.flushall()
#
#     st = time.time()
#     bench(r)
#     ed = time.time()
#     print("sync writes:", ed - st)

    #
    #
    # for i in range(1000):
    #     print(r.get(str(i)))

#
# if __name__ == "__main__":
#     # bench()
#     # test_flush()
#     # print("test")
#     test_async_writer()
#     bench_async_writer()