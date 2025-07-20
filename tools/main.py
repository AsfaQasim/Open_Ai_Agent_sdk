import random
from urllib import request
from agents import (
    Agent,
    RunConfig,
    Runner,
    OpenAIChatCompletionsModel,
    function_tool,
    RunContextWrapper,
    FunctionToolResult,
    ToolsToFinalOutputResult
)
from dotenv import load_dotenv
import os
import json
from openai import AsyncOpenAI
from agents.agent import StopAtTools

load_dotenv()

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
    tracing_disabled=True
)

@function_tool
def get_riddle() -> str:
    """
    Get a random riddle
    """
    riddles = [
        "1. I speak without a mouth and hear without ears. I have nobody, but I come alive with the wind. What am I?",
        "2. The more you take, the more you leave behind. What am I?",
        "3. What has keys but can't open locks?",
        "4. I’m tall when I’m young, and I’m short when I’m old. What am I?",
        "5. What has a heart that doesn’t beat?",
        "6. What can travel around the world while staying in the same corner?",
        "7. What gets wetter the more it dries?",
        "8. I have branches, but no fruit, trunk, or leaves. What am I?",
        "9. What begins with T, ends with T, and has T in it?",
        "10. What comes once in a minute, twice in a moment, but never in a thousand years?"
    ]
    return random.choice(riddles)

@function_tool
def get_Weather(city: str) -> str:
    """
    Get the weather for a given city
    """
    try:
        result = request.urlopen(
            f"https://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={city}"
        )
        data = json.load(result)
        temp = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        return f"The current weather in {city} is {temp}°C with {condition}."
    except Exception as e:
        return f"Could not fetch data due to {e}"


def my_func(wrapper: RunContextWrapper, tool_result: list[FunctionToolResult]) -> ToolsToFinalOutputResult:
    print("My func executed")
    return ToolsToFinalOutputResult(
        is_final_output=True,
        final_output="Hello world"
    )

agent = Agent(
    name="Assistant",
    instructions="""
    If the user asks for a riddle, first call get_riddle and tell the riddle with numbers.
    If the user asks about the weather, call the get_Weather function with the city name.
    """,
    model=model,
    tools=[get_riddle, get_Weather],
    # tool_use_behavior=StopAtTools(
    #     stop_at_tool_names=["get_Weather"]
    # )
    tool_use_behavior= my_func
)

prompt = input("What do you want? ")

result = Runner.run_sync(
    starting_agent=agent,
    input=prompt,
    run_config=config
)

print(result.final_output)
