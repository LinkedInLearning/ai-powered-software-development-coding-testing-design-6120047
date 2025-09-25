# Example 1: Calculator function
def calculate(x: float, y: float, operation: str) -> float:
    """
    Perform basic arithmetic operations on two numbers.
    
    Args:
        x: First number
        y: Second number
        operation: Operation to perform ('+', '-', '*', '/')
    
    Returns:
        Result of the operation
        
    Raises:
        ValueError: If operation is not supported
        ZeroDivisionError: If attempting to divide by zero
    """
    operations = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b if b != 0 else float('inf')
    }
    
    if operation not in operations:
        raise ValueError(f"Unsupported operation: {operation}")
    
    return operations[operation](x, y)


# Example 2: List comprehension for squares
def calculate_squares(numbers: list) -> list:
    """
    Calculate squares of numbers using list comprehension.
    
    Args:
        numbers: List of numbers to square
        
    Returns:
        List of squared numbers
    """
    return [num ** 2 for num in numbers]


# Example usage and testing
if __name__ == "__main__":
    # Test calculator
    print("Calculator Tests:")
    print(f"10 + 5 = {calculate(10, 5, '+')}")
    print(f"10 / 5 = {calculate(10, 5, '/')}")
    print(f"10 * 5 = {calculate(10, 5, '*')}")
    print(f"10 - 5 = {calculate(10, 5, '-')}")
    
    # Test error handling
    try:
        print(f"10 / 0 = {calculate(10, 0, '/')}")
    except ZeroDivisionError:
        print("Division by zero handled gracefully")
    
    try:
        print(f"10 % 5 = {calculate(10, 5, '%')}")
    except ValueError as e:
        print(f"Error: {e}")
    
    print("\nSquares Calculation:")
    numbers = [1, 2, 3, 4, 5]
    squares = calculate_squares(numbers)
    print(f"Squares of {numbers} = {squares}")
    
    # Additional pythonic examples
    print("\nAdditional Pythonic Examples:")
    
    # Using map() for squares
    squares_map = list(map(lambda x: x ** 2, numbers))
    print(f"Using map(): {squares_map}")
    
    # Using generator expression
    squares_gen = list(x ** 2 for x in numbers)
    print(f"Using generator: {squares_gen}")
    
    # Dictionary comprehension
    squares_dict = {num: num ** 2 for num in numbers}
    print(f"Dictionary of squares: {squares_dict}")