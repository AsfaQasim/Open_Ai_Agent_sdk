from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, handoff, set_tracing_disabled
import os
from dotenv import load_dotenv
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from service.service_function import service
from my_tools.tools import add, weather
from input_data_Schema.input_Schema import MyInputData
from agents.extensions import handoff_filters
from policy.activate import activate



load_dotenv()
set_tracing_disabled(disabled= True)

gemini_Api_key = os.getenv("Gemini_Api_Key")


client = AsyncOpenAI(
 api_key= gemini_Api_key, 
 base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

Model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client= client
)

Math_agent = Agent(
    name = "Math Assistant",
    instructions= f"""
    {RECOMMENDED_PROMPT_PREFIX}
    """,
    model=Model,
    tools=[add, weather],
    handoff_description= "This helpful math assistant"
)

math_teacher = handoff(
    agent = Math_agent,
    tool_name_override= "math_teacher",
    # tool_description_override="This is helpful math teacher",
    on_handoff= service,
    input_type= MyInputData,
    input_filter= handoff_filters.remove_all_tools,
    is_enabled= activate
)

assistant = Agent (
    name = "Assistant",
    instructions= "You are a helpful assistant",
    model= Model,
    handoffs= [math_teacher],
)

result = Runner.run_sync(
    starting_agent=assistant, 
    input = "what is weather of karachi and what is 2 + 2?",
    context= {"name": "asfa", "age": 12, "role": "teacher"}
)


print(result.final_output)
# print(result.last_agent.name)
# print(assistant.handoffs)