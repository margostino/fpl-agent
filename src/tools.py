from langchain.tools import tool
from pydantic import BaseModel, Field


class GameweekId(BaseModel):
    gameweek_id: int = Field(description="should be and ID between 1 and 38")


@tool("gameweek-tool", args_schema=GameweekId)
def get_gameweek_by_id(gameweek_id: int) -> str:
    """
    Get information about a specific Premier League Gameweek by ID.
    This returns all results for a given Premier League Gameweek.
    """
    print(f"Fetching information about Gameweek ID {gameweek_id}")
    output = """
        - Manchester United vs Liverpool: 3-10
        - Arsenal vs Chelsea: 1-2
    """
    return output
