
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Runner, Agent, RunConfig, set_tracing_disabled, RunContextWrapper, enable_verbose_stdout_logging, handoff, HandoffInputData
from agents.handoffs import THandoffInput
import os
from dotenv import load_dotenv
from rich import print
from typing import Callable
from pydantic import BaseModel

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

# prompt = input("Enter your question: ")
result = Runner.run_sync(
    starting_agent= triage_Agent,
     input=  """
     What is 2 + 2?
     what is the gravity of earth?
     """, 
    
)

# input_filter: Callable[[HandoffInputData], HandoffInputData] | None = None,

def input_filter(data: HandoffInputData) -> HandoffInputData:
    return data
print("Input filter is executed")


class Myinputtype(BaseModel):
    user_query : str

#  On_handoff

def on_handoff(wrapper:RunContextWrapper, input_type: Myinputtype):
    print("On handoff function executed!")


handoff_Agent = handoff(
    agent =  triage_Agent,
    tool_name_override= "new agent",
    tool_description_override= "You are an expert in maths and physics",
    input_filter = input_filter,
    on_handoff = on_handoff,
    input_type= Myinputtype
)

print(handoff_Agent)

print(result.final_output)