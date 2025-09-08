from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig, function_tool, handoff, set_tracing_disabled, RunContextWrapper, SQLiteSession
import os
from dotenv import load_dotenv
import asyncio
from rich import print

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

session = SQLiteSession("user_1", "conversation.db")

agent = Agent(
    name="Assistant",
    instructions="you are a helpful assistant",
    model=model,
)

async def main():
  
    user_data = await session.get_items()   
    
    for user in user_data:
        print(f"{user['role']}: {user['content']}")

asyncio.run(main())


# while True:
#     prompt = input("write prompt here.... ")
    
#     if prompt == "exit":
#         break
    
#     res = Runner.run_sync(
#         starting_agent=agent,
#         input=prompt,
#         session=session,
#         run_config=RunConfig(model=model)
#     )
    
#     print(res.final_output)   
