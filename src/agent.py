import threading

import streamlit as st
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI

from config import config
from prompt import FPL_AGENT_PROMPT
from tools.events import get_all_gameweeks, get_gameweek_by_id
from tools.h2h import get_h2h_by_short_names
from tools.players import get_player_by_web_name, get_players_by_team_shortname
from tools.teams import get_all_teams, get_team_by_short_name


class FplAgent:
    _instance = None
    _lock = threading.Lock()
    executor: AgentExecutor

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                # pylint: disable=no-value-for-parameter
                cls._instance = super(FplAgent, cls).__new__(cls)
                model = st.secrets.llm.model
                llm = ChatOpenAI(
                    model=model,
                    temperature=0,
                    openai_api_key=config.openai_api_key,
                )
                tools = [
                    get_gameweek_by_id,
                    get_all_gameweeks,
                    get_players_by_team_shortname,
                    get_player_by_web_name,
                    get_team_by_short_name,
                    get_all_teams,
                    get_h2h_by_short_names,
                ]
                agent = create_openai_tools_agent(llm, tools, prompt=FPL_AGENT_PROMPT)

                cls._instance.executor = AgentExecutor(
                    agent=agent,
                    tools=tools,
                    verbose=True,
                    max_iterations=100,
                    max_execution_time=300,
                    return_intermediate_steps=True,
                    handle_parsing_errors=True,
                )

        return cls._instance
