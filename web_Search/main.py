from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool, RunConfig, set_tracing_disabled
import os
import requests
from dotenv import load_dotenv

load_dotenv()

tavily_api_key = os.getenv("TAVILY_API_KEY")   
set_tracing_disabled(disabled= True)

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"), 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

Model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)


@function_tool
def web_search(query: str):
    "Perform a web search using Tavily API"
    url = "https://api.tavily.com/search"
    headers = {"Authorization": f"Bearer {tavily_api_key}"}
    payload = {"query": query, "search_depth": "basic"}

    res = requests.post(url, json=payload, headers=headers)
    if res.status_code == 200:
        data = res.json()
        return data.get("results", [])
    else:
        return {"error": res.text}


agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant. Use web_search tool when you need up-to-date info.",
    model=Model,
    tools=[web_search],   
)

prompt = input("what is your query? ")

result = Runner.run_sync(
    starting_agent= agent,
    input = prompt,
    run_config= RunConfig
)

print(result.final_output)