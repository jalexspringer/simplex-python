"""
Async Bounded Queue (ABQueue) for simplexbot
Ported from TypeScript src/queue.ts
Refactored for Python 3.13+ idioms (PEP 695 generics, context manager, RuntimeError)
"""

import asyncio
from collections.abc import AsyncIterator
from typing import TypeVar

T = TypeVar("T")


class ABQueueError(RuntimeError):
    """Raised when enqueue or dequeue is attempted on a closed queue."""


_queue_closed = object()


class ABQueue[T]:  # Python 3.13+ PEP 695 generics
    """Async bounded queue with close support, async iteration, and async context manager.

    This queue provides:
      - Bounded capacity enforced by maxsize
      - Support for asynchronous enqueue and dequeue
      - Graceful closing (no further enqueue/dequeue after close)
      - Async iteration (for item in async queue)
      - Async context manager support (with async ... as ...)

    Args:
        maxsize: Maximum number of items allowed in the queue.

    Raises:
        ABQueueError: If enqueue or dequeue is attempted after the queue is closed.
    """

    def __init__(self, maxsize: int):
        self._queue = asyncio.Queue(maxsize)
        self._enq_closed = False
        self._deq_closed = False
        self._lock = asyncio.Lock()

    async def enqueue(self, item: T) -> None:
        """Enqueue an item into the queue.

        Args:
            item: The item to enqueue.
        Raises:
            ABQueueError: If the queue is closed for enqueueing.
        """
        async with self._lock:
            if self._enq_closed:
                raise ABQueueError("enqueue: queue closed")
        await self._queue.put(item)

    async def dequeue(self) -> T:
        """Dequeue an item from the queue.

        Returns:
            The dequeued item.
        Raises:
            ABQueueError: If the queue is closed for dequeueing or was closed after this item.
        """
        async with self._lock:
            if self._deq_closed:
                raise ABQueueError("dequeue: queue closed")
        item = await self._queue.get()
        if item is _queue_closed:
            self._deq_closed = True
            raise ABQueueError("dequeue: queue closed")
        return item

    async def close(self) -> None:
        """Close the queue for enqueueing and signal closure to consumers.

        After calling close, no further items can be enqueued. One special sentinel is enqueued to signal closure to consumers.
        """
        async with self._lock:
            if not self._enq_closed:
                self._enq_closed = True
                await self._queue.put(_queue_closed)

    def __aiter__(self) -> AsyncIterator[T]:
        """Return async iterator for queue items until closed."""
        return self

    async def __anext__(self) -> T:
        """Return the next item from the queue or raise StopAsyncIteration if closed."""
        try:
            return await self.dequeue()
        except ABQueueError:
            raise StopAsyncIteration

    async def __aenter__(self):
        """Enter the async context manager (returns self)."""
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """Exit the async context manager, closing the queue."""
        await self.close()
