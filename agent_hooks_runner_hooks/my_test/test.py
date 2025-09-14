from agents import Agent, AgentHooks, RunHooks, RunContextWrapper
from pydantic import BaseModel

# ✅ Pydantic model for context
class MyData(BaseModel):
    name: str
    age: int
    role: str

# ✅ Example data for context
my_data = MyData(name="asfa", age=123, role="student")

# ✅ Run-level hooks (trigger during each run)
class MyCustomHook(RunHooks):
    async def on_agent_start(
        self, context: RunContextWrapper[MyData], agent: Agent[MyData]
    ):
        print(
            f"[HOOK] Starting agent {agent.name} | "
            f"User: {context.context.name}, Age: {context.context.age}, Role: {context.context.role}"
        )

    async def on_agent_end(
        self, context: RunContextWrapper[MyData], agent: Agent[MyData], final_output
    ):
        print(f"[HOOK] Completed agent {agent.name} | Final Output: {final_output}")


# ✅ Agent-level hooks (trigger on run start/end)
class MyCustomRunHook(AgentHooks):
    async def on_run_start(self, run):
        print(f"[RUN HOOK] Run started: {run.id}")

    async def on_run_end(self, run):
        print(f"[RUN HOOK] Run ended: {run.id} | Final Output: {run.final_output}")
