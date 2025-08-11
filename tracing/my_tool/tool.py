from agents import function_tool

@function_tool
def plus(a: int, b: int):
    "Plus tool fire --->"
    return f"your answer is {a + b}"
