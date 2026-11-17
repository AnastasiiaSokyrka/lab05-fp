from streams import (
    fib_stream,
    first_stats,
    moving_average,
    naturals,
    running_totals,
    take,
)


def main() -> None:
    numbers = (4, 1, 7, 2, 6, 3)
    print("(max, min, range):")
    for index, stats in enumerate(first_stats(numbers, 3, 3), start=1):
        print(f"  {index}. {stats}")
    print(f"Infinite stream, skip 2: {first_stats(naturals(10), 4, 3, skip=2)}")
    print(f"Fibonacci: {take(10, fib_stream())}")
    print(f"Moving averages: {take(3, moving_average(numbers, 3))}")
    print(f"Running totals: {tuple(running_totals(numbers))}")


if __name__ == "__main__":
    main()
