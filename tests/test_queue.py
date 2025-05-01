"""
Tests for ABQueue (async bounded queue) - ported and adapted from the TypeScript queue.test.ts
"""

import asyncio

import pytest

from simplexbot.queue import ABQueue, ABQueueError


@pytest.mark.asyncio
@pytest.mark.parametrize("maxsize", [10, 1, 0])
async def test_async_queue_api(maxsize):
    arr = list(range(100))
    q = ABQueue[int](maxsize)
    results = await asyncio.gather(enqueue_arr(q, arr), dequeue_arr(q))
    assert arr == results[1]


@pytest.mark.asyncio
@pytest.mark.parametrize("maxsize", [10, 1, 0])
async def test_async_queue_iterator_api(maxsize):
    arr = list(range(100))
    q = ABQueue[int](maxsize)
    results = await asyncio.gather(enqueue_arr(q, arr), iter_queue(q))
    assert arr == results[1]


@pytest.mark.asyncio
async def test_enqueue_dequeue_closed_queue_raises():
    q = ABQueue[int](10)
    await q.enqueue(1)
    await q.enqueue(2)
    await q.close()
    with pytest.raises(ABQueueError):
        await q.enqueue(3)
    assert await q.dequeue() == 1
    assert await q.dequeue() == 2
    with pytest.raises(ABQueueError):
        await q.dequeue()
    with pytest.raises(ABQueueError):
        await q.enqueue(3)


# Helper functions
async def enqueue_arr(q, xs):
    for x in xs:
        await q.enqueue(x)
    await q.close()


async def dequeue_arr(q):
    out = []
    try:
        while True:
            out.append(await q.dequeue())
    except ABQueueError:
        pass
    return out


async def iter_queue(q):
    out = []
    async for x in q:
        out.append(x)
    return out
