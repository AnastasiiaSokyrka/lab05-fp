from collections.abc import Iterator

import pytest

from streams import (
    drop,
    fib_stream,
    first_stats,
    moving_average,
    naturals,
    running_totals,
    sliding_window,
    take,
)


def test_stats() -> None:
    assert first_stats((4, 1, 7, 2, 6, 3), 3, 3) == ((7, 1, 6), (7, 1, 6), (7, 2, 5))
    assert first_stats((-1.5, -2), 1, 5) == ((-1.5, -1.5, 0), (-2, -2, 0))


def test_finite_edges() -> None:
    assert first_stats((), 2, 5) == ()
    assert first_stats((1, 2), 3, 5) == ()
    assert first_stats((1, 2), 2, 9) == ((2, 1, 1),)


def test_laziness() -> None:
    seen: list[int] = []

    def source() -> Iterator[int]:
        for value in naturals():
            seen.append(value)
            yield value

    iterator = source()
    assert first_stats(iterator, 3, 0, skip=2) == ()
    assert seen == []
    assert first_stats(iterator, 3, 2, skip=2) == ((4, 2, 2), (5, 3, 2))
    assert seen == [0, 1, 2, 3, 4, 5]
    assert next(iterator) == 6


def test_windows_and_invalid_sizes() -> None:
    assert list(sliding_window("abcd", 2)) == [("a", "b"), ("b", "c"), ("c", "d")]
    with pytest.raises(ValueError):
        list(sliding_window((1,), 0))
    with pytest.raises(ValueError):
        first_stats((), 0, 0)
    with pytest.raises(ValueError):
        take(-1, ())
    with pytest.raises(ValueError):
        drop(-1, ())


def test_stream_helpers() -> None:
    assert take(3, drop(3, fib_stream())) == (2, 3, 5)
    assert take(2, moving_average((2, 4, 8), 2)) == (3.0, 6.0)
    assert tuple(running_totals((2, 4, 8))) == (2, 6, 14)
