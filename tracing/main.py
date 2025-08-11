
from agents import Agent, RunConfig, Runner, OpenAIChatCompletionsModel, set_tracing_export_api_key, AsyncOpenAI, trace
from dotenv import load_dotenv
import os
from decouple import config
from rich import print
from my_tool.tool import plus

API_KEY = config("OPENAI_API_KEY")
KEY = config("GOOGLE_API_KEY")


load_dotenv()


set_tracing_export_api_key(API_KEY)

client = AsyncOpenAI(
    api_key= KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

Model = OpenAIChatCompletionsModel(
    model= "gemini-2.0-flash",
    openai_client= client
)


# math_agent = Agent(
#     name = "Math teacher",
#     instructions= "you are helpful math assistant",
#     model= Model,
#     handoff_description="This is math teacher"
    
# )

agent = Agent(
    name = "My Math Assistant",
    instructions= "you are a helpful math teacher",
    model= Model,
    tools = [plus],
    # handoffs= [math_agent]
)

with trace("Agent with Work flow"):
   result = Runner.run_sync(
   starting_agent= agent,
    input = "what is 2 +2 ?",
    run_config= RunConfig
)


   res = Runner.run_sync(
       starting_agent= agent,
       input = f"{result.final_output}  * 1000",
       run_config= RunConfig(tracing_disabled= False)
  
   )

print(res.final_output)