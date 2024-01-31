from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from prompt import FPL_AGENT_PROMPT
from tools import get_gameweek_by_id


class FplAgent(BaseModel):
    model: str
    executor: AgentExecutor = None

    def __init__(self, model: str, openai_api_key: str, **data):
        super().__init__(model=model, **data)
        llm = ChatOpenAI(model=model, temperature=0, openai_api_key=openai_api_key)
        tools = [get_gameweek_by_id]
        agent = create_openai_tools_agent(llm, tools, prompt=FPL_AGENT_PROMPT)

        self.model = model
        self.executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            max_iterations=100,
            max_execution_time=300,
            return_intermediate_steps=True,
        )
