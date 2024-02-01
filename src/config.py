from pydantic import BaseModel


class Config(BaseModel):
    openai_api_key: str = None
    anfield_api_key: str = None

    def __init__(self, openai_api_key: str = None, anfield_api_key: str = None, **data):
        super().__init__(**data)
        self.openai_api_key = openai_api_key
        self.anfield_api_key = anfield_api_key


config = Config()
