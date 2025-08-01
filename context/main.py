# type: ignore
from pyexpat import model
from agents import Agent, RunConfig,set_tracing_disabled, Runner
from my_agent.agent import agent
from user_data_type.userdata import UserData
 

set_tracing_disabled(disabled= True)

user_1 = UserData(name="asfa", age=123, role="student")


result = Runner.run_sync(
    agent , 
    input =  "hello",
    run_config = RunConfig(),
    context =  user_1
)

print(result.final_output)