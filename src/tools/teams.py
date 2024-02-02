import requests
import streamlit as st
from langchain.tools import tool
from pydantic import BaseModel, Field

from config import config

TEAMS_QUERY = """
query Teams{
	teams {
		name
		shortName
		strengthAttackHome
		strengthAttackAway
		strengthOverallHome
		strengthOverallAway
		strengthDefenceHome
		strengthDefenceAway
	}
}
"""

TEAM_QUERY = """
query Team($shortName: String!) {
	team(shortName: $shortName) {
		name
		shortName
		strengthAttackHome
		strengthAttackAway
		strengthOverallHome
		strengthOverallAway
		strengthDefenceHome
		strengthDefenceAway
	}
}
"""


class ShortName(BaseModel):
    short_name: str = Field(description="should be and ID between 1 and 38")


@tool("team-tool", args_schema=ShortName)
def get_team_by_short_name(short_name: str) -> dict:
    """
    Get information about specific Team for a given team short name (e.g. shortname for Liverpool is LIV).
    This returns a single team information for the given Team Short Name.
    If you need information about Players for a given Team, you can use the players tool and get stats for the players of this team.
    """
    print(f"Fetching information about Team {short_name}")
    variables = {"shortName": short_name}

    headers = {"Authorization": f"Baerer {config.anfield_api_key}"}
    res = requests.post(
        config.anfield_graphql_endpoint,
        json={"query": TEAM_QUERY, "variables": variables},
        timeout=10,
        headers=headers,
    )
    if res.status_code != 200:
        print(f"Failure querying team. Error: {res.status_code} - {res.content}")

    players = res.json()["data"]["team"]

    return players


@tool("teams-tool")
def get_all_teams() -> list[dict]:
    """
    Get information about all teams. This returns all teams information (e.g. short name for each team).
    """
    print("Fetching information about Teams")

    headers = {"Authorization": f"Baerer {config.anfield_api_key}"}
    res = requests.post(
        config.anfield_graphql_endpoint,
        json={"query": TEAMS_QUERY},
        timeout=10,
        headers=headers,
    )
    if res.status_code != 200:
        print(f"Failure querying teams. Error: {res.status_code} - {res.content}")

    players = res.json()["data"]["teams"]

    return players
