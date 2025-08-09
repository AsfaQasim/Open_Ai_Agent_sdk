
from agents import OpenAIChatCompletionsModel, AsyncOpenAI,set_tracing_disabled
import os
from dotenv import load_dotenv
load_dotenv()


set_tracing_disabled(disabled= True)
gemini_api_key = os.getenv("Gemini_Api_Key")

client = AsyncOpenAI(
    api_key= gemini_api_key,
     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)



Model = OpenAIChatCompletionsModel(
    model= "gemini-2.0-flash",
    openai_client= client
)