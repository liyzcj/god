from typing import List


def binary_search(numbers: List[int], target: int) -> int:
    """
    Binary search algorithm, note that numbers must be ordered.

    Parameters
    ----------
    numbers : List[int]
        the array with int value.
    target : int
        target number.

    Returns
    -------
    int
        the index of target number if exists, else return -1.
    """
    low = 0
    up = len(numbers) - 1
    while low <= up:
        mid = (low + up) // 2
        if numbers[mid] == target:
            return mid
        elif numbers[mid] > target:
            up = mid - 1
        else:
            low = mid + 1
    return -1
