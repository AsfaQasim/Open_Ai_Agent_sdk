from ast import main
from agents import input_guardrail, Runner , Agent, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunConfig,RunContextWrapper,TResponseInputItem, GuardrailFunctionOutput,InputGuardrail,InputGuardrailTripwireTriggered
from dotenv import load_dotenv
import os
from rich import print
load_dotenv()


# Api_Key

gemini_Api_key = os.getenv("Gemini_Api_Key")

provider = AsyncOpenAI(
    api_key= gemini_Api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client= provider
)

# @input_guardrail(
#     name = "input"
# )
# def my_guadrails_func(ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
#     print("Guardial function is executed")
#     return GuardrailFunctionOutput (
#       output_info= None,
#       tripwire_triggered= False  
#     )
# @input_guardrail(
#     name = "input"
# )
def my_guadrails_func(ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    print("Guardial function is executed")
    return GuardrailFunctionOutput (
      output_info= None,
      tripwire_triggered= False  
    )
def my_guadrails_func1(ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    print("Guardial function is executed")
    return GuardrailFunctionOutput (
      output_info= None,
      tripwire_triggered= False  
    )
custom_guardrail = InputGuardrail(
    guardrail_function=my_guadrails_func,
    name="guardrail"
)

#  Agent
agent = Agent(
    name = "Assistant",
    instructions= "You are a helpful assistant",
    input_guardrails= [custom_guardrail]
)
try:
    result = Runner.run_sync(
        starting_agent=agent,
        input="What is the capital of Pakistan?",
        run_config=RunConfig(model)
    )
    print(result.input_guardrail_results)
    print(result.final_output)
    print(my_guadrails_func)

except InputGuardrailTripwireTriggered as e:
    print(e.guardrail_result)
    
print(custom_guardrail.get_name)
from agents import RunContextWrapper, Agent

my_guadrails_func1(
    ctx=RunContextWrapper(context=None), 
    agent=Agent(name="Assistant", instructions="Testing..."),
    input="hello"
)

#  async function 
async def amin():
 await my_guadrails_func1.run( # type: ignore
   ctx=RunContextWrapper(context=None),
    agent=Agent(name = "Assistant"),
    input = "hello"
)
import asyncio
asyncio.run(main())