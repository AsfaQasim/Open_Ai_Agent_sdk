from agents import Agent
from data_schema.my_Data_output import MyDataOutput
from my_config.config import Model

guardial_agent = Agent(
    name = "Guardial Agent",
    instructions= "Check a hotel queries account or tax query",
    model = Model,
    output_type= MyDataOutput
)

