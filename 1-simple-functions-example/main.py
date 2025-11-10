def get_weather(temp):
    """
    Determine if the weather is 'Hot' or 'Cold' based on temperature.
    
    Args:
        temp (float or int): Temperature value.
    
    Returns:
        str: "Hot" if temperature > 20, else "Cold".
    """
    return "Hot" if float(temp) > 20 else "Cold"


def add(a, b):
    """
    Return the sum of two numbers.
    
    Args:
        a (int or float): First number.
        b (int or float): Second number.
    
    Returns:
        int or float: Sum of a and b.
    """
    return a + b


def divide(a, b):
    """
    Divide a number by another.
    
    Args:
        a (int or float): Numerator.
        b (int or float): Denominator.
    
    Raises:
        ValueError: If attempting to divide by zero.
    
    Returns:
        float: The division result.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
