
from agents import  AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv
import os

load_dotenv()

gemini_Api_key = os.getenv("Gemini_Api_Key")


client = AsyncOpenAI(
    api_key= gemini_Api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

Model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client= client
)