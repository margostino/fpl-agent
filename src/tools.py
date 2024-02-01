import os

import requests
from langchain.tools import tool
from pydantic import BaseModel, Field

from config import config

GRAPHQL_ENDPOINT = "https://anfield-api-margostino.vercel.app/api/query"
EVENTS_QUERY = """
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
        }
    }
}
"""


class GameweekId(BaseModel):
    gameweek_id: int = Field(description="should be and ID between 1 and 38")


@tool("gameweek-tool", args_schema=GameweekId)
def get_gameweek_by_id(gameweek_id: int) -> list[dict]:
    """
    Get information about a specific Premier League Gameweek by ID.
    This returns all results for a given Premier League Gameweek.
    When "finished" attribute in response if False, the game is still in progress or has not yet started.
    """
    print(f"Fetching information about Gameweek ID {gameweek_id}")
    variables = {"id": gameweek_id}

    headers = {"Authorization": f"Baerer {config.anfield_api_key}"}
    res = requests.post(
        GRAPHQL_ENDPOINT,
        json={"query": EVENTS_QUERY, "variables": variables},
        timeout=10,
        headers=headers,
    )
    if res.status_code != 200:
        print(f"Failure querying events. Error: {res.status_code} - {res.content}")
    fixtures = res.json()["data"]["event"]["fixtures"]
    return fixtures
