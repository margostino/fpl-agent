import requests
import streamlit as st
from langchain.tools import tool
from pydantic import BaseModel, Field

from config import config

QUERY = """
query HeadToHead($teamAShortName: String!, $teamHShortName: String!) {
	h2h(teamAShortName: $teamAShortName, teamHShortName: $teamHShortName) {
		Gameweeks {
			TeamAName
			ScoreTeamA
			TeamHName
			ScoreTeamH
			Kickoff
		}
		StatsTeamA {
			Name
			Value
			Description
		}
		StatsTeamH {
			Name
			Value
			Description
		}
	}
}
"""


class H2h(BaseModel):
    team_a_short_name: str = Field(
        description="should be a team short name player AWAY"
    )
    team_h_short_name: str = Field(
        description="should be a team short name player HOME"
    )


@tool("head-to-head-tool", args_schema=H2h)
def get_h2h_by_short_names(team_a_short_name: str, team_h_short_name: str) -> dict:
    """
    Get information about specific Team for a given team short name (e.g. shortname for Liverpool is LIV).
    This returns a single team information for the given Team Short Name.
    """
    print(
        f"Fetching information about the H2H between {team_h_short_name} and {team_a_short_name}"
    )
    variables = {
        "teamAShortName": team_a_short_name,
        "teamHShortName": team_h_short_name,
    }

    headers = {"Authorization": f"Baerer {config.anfield_api_key}"}
    res = requests.post(
        config.anfield_graphql_endpoint,
        json={"query": QUERY, "variables": variables},
        timeout=10,
        headers=headers,
    )
    if res.status_code != 200:
        print(f"Failure querying H2H. Error: {res.status_code} - {res.content}")

    h2h = res.json()["data"]["h2h"]

    return h2h
