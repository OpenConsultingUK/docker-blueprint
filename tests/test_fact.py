import pytest  # Testing framework for Python

from fact.lib import InvalidFactorialError, factorial  # Import the factorial function and custom exception


@pytest.mark.parametrize(
    "n, expected",
    [
        (1, 1),       # Test case: factorial of 1 is 1
        (2, 2),       # Test case: factorial of 2 is 2
        (3, 6),       # Test case: factorial of 3 is 6
        (10, 3628800),  # Test case: factorial of 10 is 3628800
    ],
)
def test_factorial(n: int, expected: int) -> None:
    """
    Test the `factorial` function with valid inputs.

    Args:
        n (int): The input number for calculating the factorial.
        expected (int): The expected result of the factorial calculation.

    Returns:
        None: Test passes if the actual result matches the expected result.
    """
    assert factorial(n) == expected


@pytest.mark.parametrize(
    "n",
    [
        -1,      # Test case: negative input
        -100,    # Test case: large negative input
    ],
)
def test_invalid_factorial(n: int) -> None:
    """
    Test the `factorial` function with invalid inputs that should raise InvalidFactorialError.

    Args:
        n (int): The invalid input number.

    Returns:
        None: Test passes if the function raises InvalidFactorialError for invalid inputs.
    """
    with pytest.raises(InvalidFactorialError):
        factorial(n)