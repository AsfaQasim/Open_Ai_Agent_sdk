from agents import Agent
from my_config.config import Model
from my_tool.tools import get_age
from instruction.dynamicinstruction import dynamic_instruction
from user_data_type.userdata import UserData

agent = Agent [UserData](
    name = "Assistant", 
    instructions= dynamic_instruction,
    model= Model,
    tools = [get_age]
)
