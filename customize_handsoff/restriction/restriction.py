from agents import RunContextWrapper

async def res(ctx:RunContextWrapper, agent):
    if ctx.context["age"] >= 18:
        return True
    return False