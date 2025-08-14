from agents import function_tool

@function_tool
def plus(a: int, b: int):
    "Plus tool fire --->"
    return f"Your answer is {a + b}"
