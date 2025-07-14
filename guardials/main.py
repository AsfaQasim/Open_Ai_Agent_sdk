from agents import Agent, OpenAIChatCompletionsModel, Runner,set_tracing_disabled
from agents.agent import InputGuardrail
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

set_tracing_disabled(disabled=True)
load_dotenv()

gemini_api_key = os.getenv("Gemini_Api_Key")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client 
)

def my_guardrail(input_text: str) -> bool:
    if any(word in input_text.lower() for word in ["add", "subtract", "multiply", "divide"]):
        return True
    return False

guardrail = InputGuardrail(
    guardrail_function=my_guardrail,
    name="math_only_guardrail"
)

agent = Agent(
    name="Assistant",
    instructions="You're a math-only assistant.",
    mcp_config={
        "input_guardrails": [guardrail]
    },
    model=model
)

prompt = input("What is your question? ")

result = Runner.run_sync(
    starting_agent=agent,
    input= prompt
)

print(result.final_output)
