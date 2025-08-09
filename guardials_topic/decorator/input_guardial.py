
from agents import input_guardrail, RunContextWrapper, GuardrailFunctionOutput, Runner, TResponseInputItem, Agent
from my_guardial.guardials_agent import guardial_agent


@input_guardrail

async def guardial_input_function(ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    res = await Runner.run(guardial_agent, input = input , context= ctx.context)
    print(agent.name)
    return GuardrailFunctionOutput(
        output_info= res.final_output,
        tripwire_triggered= not res.final_output.is_hotel_asfas_query
    )
    
