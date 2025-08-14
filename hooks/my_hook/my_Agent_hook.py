from agents import Agent, AgentHooks, RunContextWrapper, Tool
from typing import Any
import requests
class MyAgentHook(AgentHooks):
   async def on_start(self, context: RunContextWrapper, agent: Agent) -> None:
      print("start agent hook")
      print(f"Agent running: {agent.name}")
      print("start context", context.context)
      print("start agent name",agent.name)
      
      url = f"https://jsonplaceholder.typicode.com/users/{context.context.id}"
      res = requests.get(url)
      result = res.json()
      context.context.obj = result
      print(context.context.obj)
      
   async def on_end(self, context: RunContextWrapper, agent: Agent, output: Any) -> None:
      print("End Agent hook")
      print(f"Output: {output}")
      
   async def on_tool_start(
      self,
      context: RunContextWrapper,
      agent: Agent,
      tool: Tool,
   ) -> None:
      print("start tool hook --->")

   async def on_tool_end(
      self,
      context: RunContextWrapper,
      agent: Agent,
      tool: Tool,
      result: str,
   ) -> None:
      print("End tool hook --->")
    
   # async def on_handoff(
   #    self,
   #    context: RunContextWrapper,
   #    source: Agent,    
   #    agent: Agent,      
   # ) -> None:
   #    print(f"Handoff hook: from {source.name} to {agent.name}")
