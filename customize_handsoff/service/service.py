from agents import RunContextWrapper
from pydantic import BaseModel

class my_input(BaseModel):
    reason: str


async def service(ctx:RunContextWrapper, input_data:my_input):
    print(ctx.context)
    print(input_data.reason)



