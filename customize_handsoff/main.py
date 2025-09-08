from agents import Agent, Runner, OpenAIChatCompletionsModel,AsyncOpenAI, RunConfig, function_tool, handoff, set_tracing_disabled, RunContextWrapper
import os
from dotenv import load_dotenv
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from service.service import service, my_input
from agents.extensions import handoff_filters
from restriction.restriction import res

load_dotenv()
set_tracing_disabled(disabled= True)

api_key = os.getenv("Gemini_Api_Key")

client = AsyncOpenAI(
    api_key= api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(
    model ="gemini-2.0-flash",
    openai_client= client
)
@function_tool
def plus(n1:int, n2:int):
    "plus tool fire--->"
    print("plus tool fire---->")
    return f"Here is plus tool {n1 +n2}"
    
@function_tool
def weather_tool(city: str) -> str:
    print("Weather tool---->")
    return f"The {city} weather is 33 degree"
   
math_assistant = Agent(
    name = "Math_Assistant",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    you are a helpful math assistant""",
    model = model,
    tools= [plus],
    handoff_description= "This is helpful math assistant"
)
     
math_teacher = handoff(
    agent =math_assistant,
    tool_name_override="math_teacher",
    tool_description_override="here is math assistant",
    on_handoff= service,
    input_type= my_input,
    input_filter= handoff_filters.remove_all_tools,
    is_enabled= res
    
)

agent = Agent(
    name = "Assistant",
    instructions= "you are a helpful assistant",
    model = model,
    handoffs=[math_teacher],
    tools=[weather_tool]
)
res = Runner.run_sync(
    starting_agent= agent,
    input = "what is the weather of kaarchi? and what is 2 +5?",
    context = {"name": "xyz", "age": 30, "role": "student"},
    run_config= RunConfig(model = model)
)

print(res.final_output)
# print(agent.handoffs)
