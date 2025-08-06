import asyncio
import os
from dotenv import load_dotenv
from agents import Agent, Runner, RunConfig, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, SQLiteSession
from rich import print


load_dotenv()
set_tracing_disabled(disabled=True)

async def main():

    session = SQLiteSession(session_id="user_1", db_path="conversation.db")
    # await session.clear_session()
    userData = await session.get_items()
    # for user in userData:
    #     print(f"[bold green]{user['role']}[/bold green]: {user['content']}")

    gemini_api_key = os.getenv("Gemini_Api_Key")
    client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=client
    )


    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant",
        model=model
    )


    while True:
        prompt = input("write prompt here... ")
        if prompt.lower() == "exit":
            break

        result = await Runner.run(
            starting_agent=agent,
            input=prompt,
            run_config=RunConfig,
            session=session
        )

        print(f"[bold blue]Assistant:[/bold blue] {result.final_output}")
        
        

asyncio.run(main())
