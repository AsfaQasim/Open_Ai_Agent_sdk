from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig, function_tool,set_tracing_disabled
import os
from dotenv import load_dotenv
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

load_dotenv()

api_key = os.getenv("Gemini_Api_Key")
set_tracing_disabled(disabled= True)

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"

)

model = OpenAIChatCompletionsModel(
    model= "gemini-2.0-flash",
    openai_client=client
)

python_agent= Agent(
    name= "python_Agent",
    instructions= f"""{RECOMMENDED_PROMPT_PREFIX}
    you are a helpful python agent""",
    model= model,
    handoff_description="you are a python agent assistant user anything about next js you can provide the best answer"
)

next_js= Agent(
    name= "Next_js_Agent",
    instructions= f"""{RECOMMENDED_PROMPT_PREFIX}
    you are a helpful next js agent""",
    model= model,
    handoff_description="you are a next js assistant user anything about next js you can provide the best answer"
        
)

@function_tool
def plus(n1:int, n2:int):
    "Here is plus tool"
    print("plus tool fire--->")
    return f"Plus tool fire {n1 +n2}"

agent = Agent(
    name = "Assistant",
    instructions="you are a helpful assistant",
    model= model,
    tools = [plus],
    handoffs=[next_js, python_agent]
)

prompt = input("what is your query? ")

res= Runner.run_sync(
    starting_agent=agent,
    input = prompt,
    run_config= RunConfig(model=model)
)

print(res.final_output)
# print(agent.handoffs)
print(res.last_agent.name)


# for ag in agent.handoffs:
#     print(f"{ag.name} {ag.instructions}")
    