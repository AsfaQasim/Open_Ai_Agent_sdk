
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Runner, Agent, RunConfig, set_tracing_disabled, RunContextWrapper
import os
from dotenv import load_dotenv


load_dotenv()
set_tracing_disabled(disabled= True)

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
    model_provider= external_client,
    tracing_disabled=True
)
agent = Agent(
    name = "Assistant",
    instructions= "You are a helpful assistant!",
  
)

result = Runner.run_sync(
    starting_agent= agent,
    input = "What is the capital pf pakistan?",
    run_config=config
    
)
print(result.final_output)