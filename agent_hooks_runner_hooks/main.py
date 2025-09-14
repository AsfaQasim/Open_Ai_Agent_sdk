from agents import Agent, RunConfig, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled
import os
from dotenv import load_dotenv
from my_test.test import MyCustomHook, MyCustomRunHook, my_data

# Load .env keys
load_dotenv()
set_tracing_disabled(disabled=True)

# ✅ API Key
api_key = os.getenv("Gemini_Api_key")

# ✅ Async client for Gemini
client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# ✅ Model config
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

# ✅ Agent with agent-level hook
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=model,
    hooks=MyCustomRunHook()   # agent-level hook
)

# ✅ Runner executes with run-level hook + context
res = Runner.run_sync(
    starting_agent=agent,
    input="what is 2 + 2?",
    run_config=RunConfig(model=model),
    hooks=MyCustomHook(),     # run-level hook
    context=my_data           # custom context
)

# ✅ Final output
print("Final Answer:", res.final_output)
