from agents import function_tool

@function_tool
def add(n1: int, n2: int):
    """Adds two numbers and returns the result."""
    print("Add tool fired --->")
    return f"The sum is {n1 + n2}"

@function_tool
def weather(city: str):
    """Returns mock weather info for a given city."""
    print("Weather tool fired --->")
    return f"The current weather in {city} is sunny, 30°C."
