from agents import Agent, RunConfig, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, enable_verbose_stdout_logging
import os
from dotenv import load_dotenv
from my_hook.my_Agent_hook import MyAgentHook
from my_tool.tool import plus
from typing import Optional, Dict, Any
from pydantic import BaseModel
import asyncio

load_dotenv()

gemini_api_key  = os.getenv("Gemini_Api_Key")
set_tracing_disabled(disabled= True)
# enable_verbose_stdout_logging()

class MyContext(BaseModel):
    id: str
    obj: Optional[Dict[str, Any]] = None

client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    
)

Model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client= client
)

math_assistant = Agent(
    name = "Math Assistant",
    instructions= "You are a helpful assistant",
    model= Model,
    hooks = MyAgentHook(),
    tools = [plus]
)

agent = Agent(
    name = "Assistant",
    instructions= "You are a helpful teacher",
    model= Model,
    hooks = MyAgentHook(),
    handoffs= [math_assistant],
)

#  async function

async def main():
    context = MyContext(id="3")
    res = await Runner.run(
        starting_agent=math_assistant,
        input="what is 2 + 2?",
        context=context
    )
    print(res.final_output)

asyncio.run(main())
