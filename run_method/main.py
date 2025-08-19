from agents import Agent,Runner,AsyncOpenAI,OpenAIChatCompletionsModel,RunConfig, set_tracing_disabled
import os
from dotenv import load_dotenv
import asyncio
from rich import print
from openai.types.responses import ResponseTextDeltaEvent
load_dotenv()

gemini_api_key  = os.getenv("Gemini_Api_Key")

set_tracing_disabled(disabled = True)

client = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
 
)

Model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = client
)


math_agent = Agent(
    name = "Math Assistant",
    instructions = "you are a helpful math assistant",
    model = Model,
    handoff_description = "This is a math teacher"
)



agent = Agent(
    name = "Assistant",
    instructions = "you are a helpful assistant",
    model = Model,
    # handoffs = [math_agent]
)


# sync method

# res = Runner.run_sync(
#     agent, 
#     input = "what is the capital of pakistan?",
#     run_config = RunConfig
    
# )

# print(res.final_output)

#  async method

# async def main():
#     res = await Runner.run(
#         agent,
#         input = "what is the capital of pakistan?",
#         run_config = RunConfig
#     )
#     print(res.final_output)
# asyncio.run(main())

#  stream method


async def main():
    res =  Runner.run_streamed(
        agent,
        input = "1000 words essay of AI",
        run_config = RunConfig
    )
    async for event in res.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
         print(event.data.delta, end = "", flush = True)
      
asyncio.run(main())