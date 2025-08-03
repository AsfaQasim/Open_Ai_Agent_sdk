
from agents import FunctionTool, function_tool, RunContextWrapper
from tool_schema.my_tool_schema import MytoolSchema
from validator.validatetool import tool_validate



async def subtarct_function(ctx: RunContextWrapper,args):
    obj  = MytoolSchema.model_validate_json(args)
    print("subtarct tool fire--->")
    return f"your answer is {obj.n1 - obj.n2}"
    

subtract = FunctionTool(
    name = "subtract_tool",
    description= "Subtract function",
    params_json_schema= MytoolSchema.model_json_schema(),
    on_invoke_tool= subtarct_function,
    is_enabled= tool_validate ,
 
    
)

@function_tool(name_override="plus_tool",description_override="here is plus tool fire",is_enabled=tool_validate)
def plus(n1: int, n2: int):
    "plus tool fire"
    print("plus tool fire -->")
    return f"The plus tool is {n1 + n2}"