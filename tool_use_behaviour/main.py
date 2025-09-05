from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig, AsyncOpenAI, function_tool, set_tracing_disabled, ModelSettings
import os
from dotenv import load_dotenv
from agents.agent import StopAtTools

load_dotenv()
set_tracing_disabled(disabled=True)

api_key = os.getenv("Gemini_Api_Key")

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

@function_tool
def plus(n1: int, n2: int):
    """This tool adds two integers and returns their sum."""
    print("plus ")
    return f"Result: {n1+n2}"

@function_tool
def sub(n1: int, n2: int):
    """This tool subtracts the second integer from the first and returns the result."""
    print("sub tool -->")
    return f"Result: {n1-n2}"

@function_tool
def mul(n1: int, n2: int):
    """This tool multiplies two integers and returns the product."""
    print("mul tool fire--->")
    return f"Result: {n1*n2}"

agent = Agent(
    name="Assistant",
    instructions=(
        "You are a math assistant. "
        "Whenever the user asks any math question, you MUST call the correct tool "
        "(plus, sub, mul). Never compute by yourself."
    ),
    model=model,
    tools=[plus, sub, mul],
    tool_use_behavior=StopAtTools(stop_at_tool_names= ["mul", "plus"]),
    model_settings=ModelSettings(tool_choice= "mul")
    
)
res = Runner.run_sync(
    starting_agent=agent,
    # input="what is 2 + 2 jo bh answer aye use multiply kro 2 se jo bh answer aye use 10 se subtract krdo",
    input = "what is 2 +5?",
    run_config=RunConfig(model=model)   
)


print(res.final_output)

