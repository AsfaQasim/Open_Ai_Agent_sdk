
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Runner, Agent, RunConfig, set_tracing_disabled, RunContextWrapper, function_tool, enable_verbose_stdout_logging, ModelSettings, FunctionToolResult, ToolsToFinalOutputResult
import os
from dotenv import load_dotenv
from rich import print
from pydantic import BaseModel
from agents.agent import StopAtTools


enable_verbose_stdout_logging()

load_dotenv()
set_tracing_disabled(disabled= True)

gemini_Api_key = os.getenv("Gemini_Api_Key")

external_client = AsyncOpenAI(
    api_key=gemini_Api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client 
)

config = RunConfig(
    model=model,
    model_provider= external_client,
    tracing_disabled=True
)

def dynamic_instruction(wrapper:RunContextWrapper, agent:Agent) ->str:
    return "You are a helpful assiatant"
    
@function_tool
def add(a: int, b: int) -> int:
    """Add the two number."""
    return a + b

@function_tool
def sub(a: int, b: int) -> int:
    """Add the two number."""
    return a  - b

class OutputType(BaseModel):
    question:str
    answer: str
    
    
def my_func(wrapper: RunContextWrapper, tool_agent: list[FunctionToolResult]) -> ToolsToFinalOutputResult:
    print("my_Func_executed!")
    return ToolsToFinalOutputResult(
        is_final_output= True,
        final_output= "Hello"
    )
    
    
agent = Agent(
    name = "Assistant",
    instructions= dynamic_instruction,
    tools=[add],
    # model_settings= ModelSettings(
    #     tool_choice=  "auto"
    # 
    output_type= OutputType
  
)

prompt = input("What is your question?: ")

result = Runner.run_sync(
    starting_agent= agent,
    input = prompt,
    run_config=config
    
)
print(result.final_output)