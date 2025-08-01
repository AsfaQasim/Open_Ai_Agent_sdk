
from agents import RunContextWrapper, Agent
from user_data_type.userdata import UserData



def dynamic_instruction(
    ctx: RunContextWrapper[UserData], agent: Agent [UserData]
):
    return f"your name is {ctx.context.name}, you are a helpful assistant"