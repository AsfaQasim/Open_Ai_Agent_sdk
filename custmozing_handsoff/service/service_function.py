from agents import RunContextWrapper
from input_data_Schema.input_Schema import MyInputData


async def service(ctx:RunContextWrapper, input_data: MyInputData):
    print(ctx.context)
    print(input_data.reason)