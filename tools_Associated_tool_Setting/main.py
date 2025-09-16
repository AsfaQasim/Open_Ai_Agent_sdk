from typing import Any
from agents import Agent, RunConfig, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, function_tool, ModelSettings, enable_verbose_stdout_logging,FunctionTool,RunContextWrapper
import os
from dotenv import load_dotenv
from agents.agent import StopAtTools
from rich import print
from pydantic import BaseModel

load_dotenv()

class Addition(BaseModel):
    a: int
    b: int


class FunctionArgs(BaseModel):
    username: str
    age: int
def do_Some_Work()->str:
    return "done"
async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
    parsed = FunctionArgs.model_validate_json(args)
    return do_Some_Work(data=f"{parsed.username} is {parsed.age} years old")

api_key = os.getenv("Gemini_Api_Key")
set_tracing_disabled(disabled=True)
enable_verbose_stdout_logging()

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

@function_tool(name_override="Addition", description_override= "Addition tool fire---->")
def plus(params: Addition):
    print("Here is plus tool fire---->")
    return f"Plus tool {params.a + params.b - 1}"

@function_tool
def human_review():
    "Human is the loop interface"
    print("Human review called--->")
    return "Human in the loop called"

# agent = Agent(
#     name="Assistant",
#     instructions="You are a helpful assistant",
#     model=model,
#     tools=[plus, human_review],
#     tool_use_behavior=StopAtTools(stop_at_tool_names=["Addition"]), 
#     model_settings=ModelSettings(
#         tool_choice="required"
#     ),
#     reset_tool_choice=False,
# )


tool = FunctionTool(
    name="process_user",
    description="Processes extracted user data",
    params_json_schema=FunctionArgs.model_json_schema(),
    on_invoke_tool=run_function,
)

example_agent = Agent(
    name = "example_Agent",
    instructions= "This is helping agent that does nothing special",
    tools = [tool]
)
# res = Runner.run_sync(
#     starting_agent= tool,
#     input="add 5 and 7",  
#     run_config=RunConfig(model=model),
#     max_turns=2          
# )

res = Runner.run_sync(
    starting_agent= example_agent,
    input= "process user data",
    run_config= RunConfig(model= model)
)

# print(res.final_output)
# print(tool.tools)
print(res.final_output)