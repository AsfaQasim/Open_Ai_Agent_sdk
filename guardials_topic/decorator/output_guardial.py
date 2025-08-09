from agents import RunContextWrapper, GuardrailFunctionOutput, Runner,output_guardrail, TResponseInputItem, Agent
from my_guardial.guardials_agent import guardial_agent

@output_guardrail

async def gurdial_output_function(ctx:RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]):
    result = await Runner.run(guardial_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info= result.final_output,
        tripwire_triggered=result.final_output.is_hotel_asfas_account_or_tax_query
        
    )