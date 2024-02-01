import os
from tkinter import ALL

import requests
import streamlit as st
from langchain.tools import tool
from pydantic import BaseModel, Field

from config import config

GAMEWEEK_QUERY = """
query Event($id: Int!) {
    event(id: $id) {
        name
        fixtures {
            finished
            kickoffTime
            teamAName
            teamAScore
            teamHName
            teamHScore
			stats {
				identifier
				teamA {
					value
					element
				}
				teamH {
					value
					element
				}
			}            
        }
    }
}
"""

ALL_GAMEWEEKS_QUERY = """
query Events {
    events {
		name
		fixtures {
			finished
			kickoffTime
			teamAName
			teamAScore			
			teamHName
            teamHScore
		}
    }
}
"""


class GameweekId(BaseModel):
    gameweek_id: int = Field(description="should be and ID between 1 and 38")


@tool("single-gameweek-tool", args_schema=GameweekId)
def get_gameweek_by_id(gameweek_id: int) -> list[dict]:
    """
    Get information about a specific Premier League Gameweek by ID.
    This returns all results for a given Premier League Gameweek.
    When "finished" attribute in response if False, the game is still in progress or has not yet started.
    The are 38 gameweeks in total. To know what is last gameweek/event played you have to use the variable "finished" and "kickoffTime".
    """
    print(f"Fetching information about Gameweek ID {gameweek_id}")
    variables = {"id": gameweek_id}

    headers = {"Authorization": f"Baerer {config.anfield_api_key}"}
    res = requests.post(
        config.anfield_graphql_endpoint,
        json={"query": GAMEWEEK_QUERY, "variables": variables},
        timeout=10,
        headers=headers,
    )
    if res.status_code != 200:
        print(f"Failure querying events. Error: {res.status_code} - {res.content}")

    fixtures = res.json()["data"]["event"]["fixtures"]

    return fixtures


@tool("all-gameweeks-tool")
def get_all_gameweeks() -> list[dict]:
    """
    Get information about ALL gameweeks. This returns all gameweeks information played and to-be played for the whole Premier League season.
    When "finished" attribute in response if False, the game is still in progress or has not yet started.
    The are 38 gameweeks in total. To know what is last gameweek/event played you have to use the variable "finished" and "kickoffTime".
    """
    print("Fetching information about all Gameweeks")

    headers = {"Authorization": f"Baerer {config.anfield_api_key}"}
    res = requests.post(
        config.anfield_graphql_endpoint,
        json={"query": ALL_GAMEWEEKS_QUERY},
        timeout=10,
        headers=headers,
    )
    if res.status_code != 200:
        print(f"Failure querying events. Error: {res.status_code} - {res.content}")

    events = res.json()["data"]["events"]

    return events
