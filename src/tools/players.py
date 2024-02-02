import requests
from langchain.tools import tool
from pydantic import BaseModel, Field

from config import config

PLAYERS_QUERY = """
query Players($teamShortName: String!) {
	players(teamShortName: $teamShortName) {
		webName
		team
		news
		position
		chanceOfPlayingNextRound
		eventPoints
		expectedGoals
		expectedGoalsPer90
		expectedAssists
		expectedAssistsPer90
		expectedGoalsConceded
		expectedGoalsConcededPer90
		expectedGoalInvolvements
		expectedGoalInvolvementsPer90
		form
		formRank
		formRankType
		valueForm
		valueSeason
		nowCost
		nowCostRank
		nowCostRankType
		pointsPerGame
		selectedByPercent
		selectedRank
		selectedRankType
		totalPoints
		transfersInEvent
		transfersOutEvent
		minutes
		goalsScored
		assists
		cleanSheets
		goalsConceded
		ownGoals
		penaltiesSaved
		penaltiesMissed
		penaltiesOrder
		influence
		influenceRank
		influenceRankType
		ownGoals
		starts
		startsPer90
		pointsPerGame
		ictIndex
		ictIndexRank
		ictIndexRankType
		directFreekicksOrder
		cornersAndIndirectFreekicksOrder
		threat
		threatRank
		threatRankType
		creativity
		creativityRank
		creativityRankType
		bps
		bonus
		redCards
		yellowCards
	}
}
"""

PLAYER_QUERY = """
query Player($webName: String!) {
	player(webName: $webName) {
		webName
		team
		news
		position
		chanceOfPlayingNextRound
		eventPoints
		expectedGoals
		expectedGoalsPer90
		expectedAssists
		expectedAssistsPer90
		expectedGoalsConceded
		expectedGoalsConcededPer90
		expectedGoalInvolvements
		expectedGoalInvolvementsPer90
		form
		formRank
		formRankType
		valueForm
		valueSeason
		nowCost
		nowCostRank
		nowCostRankType
		pointsPerGame
		selectedByPercent
		selectedRank
		selectedRankType
		totalPoints
		transfersInEvent
		transfersOutEvent
		minutes
		goalsScored
		assists
		cleanSheets
		goalsConceded
		ownGoals
		penaltiesSaved
		penaltiesMissed
		penaltiesOrder
		influence
		influenceRank
		influenceRankType
		ownGoals
		starts
		startsPer90
		pointsPerGame
		ictIndex
		ictIndexRank
		ictIndexRankType
		directFreekicksOrder
		cornersAndIndirectFreekicksOrder
		threat
		threatRank
		threatRankType
		creativity
		creativityRank
		creativityRankType
		bps
		bonus
		redCards
		yellowCards
	}
}
"""


class TeamShortName(BaseModel):
    team_short_name: str = Field(
        description="should be the team short name. Example: For Liverpool is LIV"
    )


class WebName(BaseModel):
    web_name: str = Field(
        description="should be the web name of the player. Example: Haaland"
    )


@tool("team-players-tool", args_schema=TeamShortName)
def get_players_by_team_shortname(team_short_name: str) -> list[dict]:
    """
    Get information about all players for a given Team Short Name (e.g. shortname for Liverpool is LIV).
    This returns all players under the given Team Short Name.
    It is important to note that if the Team Short Name is "*" then all players for all teams will be returned.
    The teams information is found in the Team GraphQL query.
    The field "chanceOfPlayingNextRound" indicate the prediction to play the next game and together with the "news" field you can see if the player is injured or not.
    """
    print(f"Fetching information about Player in Team {team_short_name}")
    variables = {"teamShortName": team_short_name}

    headers = {"Authorization": f"Baerer {config.anfield_api_key}"}
    res = requests.post(
        config.anfield_graphql_endpoint,
        json={"query": PLAYERS_QUERY, "variables": variables},
        timeout=10,
        headers=headers,
    )
    if res.status_code != 200:
        print(f"Failure querying players. Error: {res.status_code} - {res.content}")

    players = res.json()["data"]["players"]

    return players


@tool("single-player-tool", args_schema=WebName)
def get_player_by_web_name(web_name: str) -> dict:
    """
    Get information about a single player for a given Web Name (e.g. Haaland).
    This returns a single player information.
    The field "chanceOfPlayingNextRound" indicate the prediction to play the next game and together with the "news" field you can see if the player is injured or not.
    """
    print(f"Fetching information about Player {web_name}")
    variables = {"webName": web_name}

    headers = {"Authorization": f"Baerer {config.anfield_api_key}"}
    res = requests.post(
        config.anfield_graphql_endpoint,
        json={"query": PLAYER_QUERY, "variables": variables},
        timeout=10,
        headers=headers,
    )
    if res.status_code != 200:
        print(f"Failure querying player. Error: {res.status_code} - {res.content}")

    players = res.json()["data"]["player"]

    return players
