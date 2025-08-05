from agents import RunContextWrapper

def activate(ctx: RunContextWrapper, agent) -> bool:
    age = ctx.context.get("age", 0) 
    if age >= 18:
        return True
    print(" User is under 18 — tool access denied.")
    return False
