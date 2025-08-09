from pyexpat import model
from agents import Agent, RunConfig, Runner,  InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from my_config.config import Model
from my_guardial.guardials_agent import guardial_agent
from decorator.input_guardial import guardial_input_function
from decorator.output_guardial import gurdial_output_function

hotel_assistant = Agent(
    name="Hotel Care Assistant",
    instructions=(
        "You are a friendly and professional hotel assistant. "
        "Help guests with booking rooms, checking availability, "
        "providing asfa's hotel information, and suggesting local attractions. "
        "Always be polite, concise, and ensure the guest feels valued."
    ),
    model=Model,
    input_guardrails= [guardial_input_function],
    output_guardrails= [gurdial_output_function]
)

RunConfig(model=model)

prompt = input("what is your query?: ")

try:
    result = Runner.run_sync(
        starting_agent=hotel_assistant,
        input= prompt,
        run_config=RunConfig() 
    )

    print(result.final_output)

except InputGuardrailTripwireTriggered as e:
    print(f"Trip input \n {e}")
    
except OutputGuardrailTripwireTriggered as e:
    print(f"Trip output \n {e}")

