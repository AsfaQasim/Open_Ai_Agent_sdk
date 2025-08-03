from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig, Runner, set_tracing_disabled
import os 
from  dotenv import load_dotenv
from my_tool.tool import plus, subtract

load_dotenv()


gemini_api_key = os.getenv("Gemini_Api_Key")

set_tracing_disabled(disabled= True)

client = AsyncOpenAI(
    api_key= gemini_api_key, 
     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

)

Model = OpenAIChatCompletionsModel(
    model= "gemini-2.0-flash",
    openai_client= client
)

agent = Agent(
    name = "Assistant",
    instructions= "You are a helpful assistant",
    model= Model,
    tools = [subtract, plus]
)

result = Runner.run_sync(
    starting_agent= agent, 
    input = "what is 2-2  ?",
    run_config= RunConfig,
    context= {"name": "asfa", "age": 20, "role": "student"}
)

# for s in agent.tools:
#     print(s.params_json_schema)



print(result.final_output)

# print(agent.tools)





