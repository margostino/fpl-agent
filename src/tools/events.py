import requests
import streamlit as st
from langchain.tools import tool
from pydantic import BaseModel, Field

from config import config

GAMEWEEK_BY_ID_QUERY = """
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

GAMEWEEK_BY_ID_AND_TEAM_QUERY = """
query Event($id: Int!, $teamShortName: String!) {
    event(id: $id, teamShortName: $teamShortName) {
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

ALL_GAMEWEEKS_BY_TEAM_QUERY = """
query Events($teamShortName: String!) {
    events(teamShortName: $teamShortName) {
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


class TeamShortName(BaseModel):
    team_short_name: str = Field(
        description="should be the team short name. Example: For Liverpool is LIV"
    )


class GameweekIdByTeam(BaseModel):
    gameweek_id: int = Field(description="should be and ID between 1 and 38")
    team_short_name: str = Field(
        description="should be the team short name. Example: For Liverpool is LIV"
    )


class GameweekId(BaseModel):
    gameweek_id: int = Field(description="should be and ID between 1 and 38")


@tool("single-gameweek-tool", args_schema=GameweekId)
def get_gameweek_by_id(gameweek_id: int) -> list[dict]:
    """
    Get information about a specific Premier League Gameweek by ID.
    This returns all results for a given Premier League Gameweek.
    When "finished" attribute in response if False, the game is still in progress or has not yet started.
    The are 38 gameweeks in total. To know what is last gameweek played you have to use the variable "finished" and "kickoffTime".
    Remember what day is today when it comes to fetch the last and next game for a team.
    """
    print(f"Fetching information about Gameweek ID {gameweek_id}")
    variables = {"id": gameweek_id}

    headers = {"Authorization": f"Baerer {config.anfield_api_key}"}
    res = requests.post(
        config.anfield_graphql_endpoint,
        json={"query": GAMEWEEK_BY_ID_QUERY, "variables": variables},
        timeout=10,
        headers=headers,
    )
    if res.status_code != 200:
        print(f"Failure querying events. Error: {res.status_code} - {res.content}")

    fixtures = res.json()["data"]["event"]["fixtures"]

    return fixtures


@tool("single-gameweek-by-team-tool", args_schema=GameweekIdByTeam)
def get_gameweek_by_id_and_team(gameweek_id: int, team_short_name: str) -> list[dict]:
    """
    Get information about a specific Premier League Gameweek by ID and Team Short Name.
    This returns all results for a given Premier League Gameweek and Team specific.
    When "finished" attribute in response if False, the game is still in progress or has not yet started.
    The are 38 gameweeks in total. To know what is last gameweek played you have to use the variable "finished" and "kickoffTime".
    Remember what day is today when it comes to fetch the last and next game for a team.
    """
    print(
        f"Fetching information about Gameweek ID {gameweek_id} and team {team_short_name}"
    )
    variables = {"id": gameweek_id, "teamShortName": team_short_name}

    headers = {"Authorization": f"Baerer {config.anfield_api_key}"}
    res = requests.post(
        config.anfield_graphql_endpoint,
        json={"query": GAMEWEEK_BY_ID_AND_TEAM_QUERY, "variables": variables},
        timeout=10,
        headers=headers,
    )
    if res.status_code != 200:
        print(f"Failure querying events. Error: {res.status_code} - {res.content}")

    fixtures = res.json()["data"]["event"]["fixtures"]

    return fixtures


@tool("get-all-gameweeks-tool")
def get_all_gameweeks() -> list[dict]:
    """
    Get information about ALL gameweeks.
    This returns all gameweeks information with fixtures played and to-be played for the whole Premier League season.
    When "finished" attribute in response if False, the game is still in progress or has not yet started.
    The are 38 gameweeks in total. To know what was last gameweek played for some team you have to use the variable "finished" and "kickoffTime".
    So, in order to know the LAST played game of a Team you have to use the latest "kickoffTime" attribute, which is a date time with "finished" attribute as "True".
    And, in order to know the NEXT game of a Team you have to know first when was the LAST game for that team, fetch the Gameweek ID and the next will be the next game (e.g. if last game was gameweek 5, the next gameweek will be 6).
    Remember what day is today when it comes to fetch the last and next game for a team.
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


@tool("get-all-gameweeks-by-team-tool", args_schema=TeamShortName)
def get_all_gameweeks_by_team(team_short_name: str) -> list[dict]:
    """
    Get information about ALL gameweeks for a given Team Short Name (e.g. for Liverpool is LIV).
    This returns all gameweeks information with fixtures played and to-be played for such team in the whole Premier League season.
    When "finished" attribute in response if False, the game is still in progress or has not yet started.
    The are 38 gameweeks in total. To know what was last gameweek played for some team you have to use the variable "finished" and "kickoffTime".
    Remember what day is today when it comes to fetch the last and next game for a team.
    """
    print(f"Fetching information about all Gameweeks for {team_short_name}")

    variables = {"teamShortName": team_short_name}

    headers = {"Authorization": f"Baerer {config.anfield_api_key}"}
    res = requests.post(
        config.anfield_graphql_endpoint,
        json={"query": ALL_GAMEWEEKS_BY_TEAM_QUERY, "variables": variables},
        timeout=10,
        headers=headers,
    )
    if res.status_code != 200:
        print(
            f"Failure querying events for team. Error: {res.status_code} - {res.content}"
        )

    events = res.json()["data"]["events"]

    return events
