from collections import deque
from collections.abc import Iterable, Iterator
from itertools import accumulate, count, islice, starmap
from typing import TypeVar

T = TypeVar("T")
Number = int | float


def take(n: int, items: Iterable[T]) -> tuple[T, ...]:
    if n < 0:
        raise ValueError("n must be non-negative")
    return tuple(islice(items, n))


def drop(n: int, items: Iterable[T]) -> Iterator[T]:
    if n < 0:
        raise ValueError("n must be non-negative")
    return islice(items, n, None)


def sliding_window(items: Iterable[T], k: int) -> Iterator[tuple[T, ...]]:
    if k <= 0:
        raise ValueError("k must be positive")
    source = iter(items)
    window = deque(islice(source, k), maxlen=k)
    if len(window) < k:
        return
    yield tuple(window)
    for item in source:
        window.append(item)
        yield tuple(window)


def window_stats(first: Number, *rest: Number) -> tuple[Number, Number, Number]:
    values = (first, *rest)
    high, low = max(values), min(values)
    return high, low, high - low


def first_stats(
    items: Iterable[Number], k: int, n: int, *, skip: int = 0
) -> tuple[tuple[Number, Number, Number], ...]:
    if k <= 0:
        raise ValueError("k must be positive")
    return take(n, starmap(window_stats, sliding_window(drop(skip, items), k)))


def naturals(start: int = 0) -> Iterator[int]:
    return count(start)


def fib_stream() -> Iterator[int]:
    current, following = 0, 1
    while True:
        yield current
        current, following = following, current + following


def moving_average(items: Iterable[Number], k: int) -> Iterator[float]:
    return (sum(window) / k for window in sliding_window(items, k))


def running_totals(items: Iterable[Number]) -> Iterator[Number]:
    return accumulate(items)
