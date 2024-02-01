import streamlit as st
from pydantic import BaseModel

from agent import FplAgent


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class App(BaseModel):
    _instance = None
    openai_api_key: str = None
    anfield_api_key: str = None
    agent: FplAgent = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(App).__new__(cls)  # pylint: disable=E1120
            cls._instance.__initialized = False  # Change access modifier to public
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True

        super().__init__()
        self.set_title()
        self.set_api_keys()

        if self.has_valid_api_keys():
            st.header("Output")
            self.agent = FplAgent(model="gpt-4-0125-preview")

    def set_title(self):
        st.set_page_config(page_title="⚽️ FPL Agent")
        st.title("⚽️ Ask about Fantasy PL")

    def set_api_keys(self):
        self.openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
        self.anfield_api_key = st.sidebar.text_input("Anfield API Key", type="password")

    def has_valid_api_keys(self) -> bool:
        if self.openai_api_key is None or self.anfield_api_key is None:
            return False

        is_anfield_api_key_valid = self.anfield_api_key.startswith("ak-")
        is_openai_api_key_valid = self.openai_api_key.startswith("sk-")

        if not is_anfield_api_key_valid:
            st.warning("Please enter your Anfield API key!", icon="⚠")

        if not is_openai_api_key_valid:
            st.warning("Please enter your OpenAI API key!", icon="⚠")

        return is_anfield_api_key_valid and is_openai_api_key_valid


app = App()
