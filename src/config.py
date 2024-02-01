import streamlit as st
from pydantic import BaseModel


class Config(BaseModel):
    openai_api_key: str = None
    anfield_api_key: str = None
    anfield_graphql_endpoint: str = None

    def __init__(self, openai_api_key: str = None, anfield_api_key: str = None, **data):
        super().__init__(**data)
        self.openai_api_key = openai_api_key
        self.anfield_api_key = anfield_api_key
        self.anfield_graphql_endpoint = st.secrets.anfield_api.endpoint


config = Config()
