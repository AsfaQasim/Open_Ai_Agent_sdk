from agents import Agent, ItemHelpers, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled
from dotenv import load_dotenv
import os
import asyncio
from rich import print
from openai.types.responses import  ResponseTextDeltaEvent
load_dotenv()

set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("Gemini_Api_Key")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

next_js_Agent = Agent(
    name="Next js agent",
    instructions="You are specialized in Next.js. Help with routing, auth, API routes, etc.",
    model=model
)

python_agent = Agent(
    name="Python agent",
    instructions="You are specialized in Python. Help with FastAPI, data handling, etc.",
    model=model
)

triage_Agent = Agent(
    name="Triage Agent",
    instructions="You help users and forward tasks to either the Next.js or Python agent.",
    model=model,
    handoffs=[next_js_Agent, python_agent]
)

async def main():
    prompt = input("What is your query? ")

    res =  Runner.run_streamed(
        starting_agent=triage_Agent,
        input=prompt
    )
    
    async for event in res.stream_events():
        if event.type == "raw_response_event" and not isinstance(event.data, ResponseTextDeltaEvent):
        #    print(event.data.delta)
           continue
        elif event.type == "agent_updated_stream_event":
            continue
        elif event.type == "run_item_stream_event":
            if event.item.type == "message_output_item":
                # print(event.item.raw_item.content[0].text)
                print(ItemHelpers.text_message_output(event.item))
    print("\nFinal Output:", res.final_output)    
if __name__ == "__main__":
    asyncio.run(main())