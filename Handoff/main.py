
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Runner, Agent, RunConfig, set_tracing_disabled, RunContextWrapper, enable_verbose_stdout_logging
import os
from dotenv import load_dotenv

load_dotenv()
set_tracing_disabled(disabled= True)

enable_verbose_stdout_logging()

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


math_Expert = Agent (
    name = "Mathematician",
    instructions= "You are an expert in Mathematics, Solve problem accurately and explain your reasoning when needed",
    model= model,
    handoff_description= "Handles all mathematical questions and calculations"
)

physics_Expert = Agent (
    name = "Physician",
    instructions= "You are an expert in physics, Solve problem accurately and explain your reasoning physics realted question when needed",
    model= model,
    handoff_description= "Handles all physics questions and theoritical problem calculations"
)

triage_Agent = Agent(
    name = "Triage agent",
    instructions= (
        "Help the user with their question",
        "If they ask about maths question, handsoff to the math agent",
        "If they ask about physics question, handsoff to the physics agent"
    ),
    handoffs= [math_Expert, physics_Expert],
    model = model
)

prompt = input("Enter your question: ")
result = Runner.run_sync(
    starting_agent= triage_Agent,
    input= prompt,
    
)

print(result.final_output)