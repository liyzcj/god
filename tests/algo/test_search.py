from god.algo import search


def test__binary_search():
    for n in range(100):
        numbers = [i * 10 for i in range(n)]
        for i in range(n):
            assert search.binary_search(numbers, i * 10) == i
            assert search.binary_search(numbers, i * 10 - 5) == -1

        numbers = [10] * n
        position = search.binary_search(numbers, 10)
        if n == 0:
            assert position == -1
        else:
            assert position >= 0 and position < n
        assert search.binary_search(numbers, 5) == -1
        assert search.binary_search(numbers, 15) == -1
