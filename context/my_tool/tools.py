from agents import function_tool, RunContextWrapper
from user_data_type.userdata import UserData

@function_tool
def get_age(ctx: RunContextWrapper[UserData]):
    """Returns the user's age."""   
    print(" Age function called")
    print("ctx-->", ctx.context.name)
    return f"Your age is {ctx.context.age}"