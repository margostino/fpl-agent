import streamlit as st
from langchain.agents import AgentExecutor
from langchain_community.callbacks import StreamlitCallbackHandler

from agent import FplAgent
from config import config


def generate_response(input_query: str, agent_executor: AgentExecutor):
    st_callback = StreamlitCallbackHandler(st.container())
    try:
        response = agent_executor.invoke(
            {"input": input_query, "chat_history": []},
            config={"callbacks": [st_callback]},
        )
        return st.success(response["output"])
    except Exception as e:
        print(f"Agent failed: {e}")
        return st.success("There was an error processing your query. Please try again.")


def main():
    st.set_page_config(page_title="⚽️ FPL Agent")
    st.title("⚽️ 🏆 You'll never walk alone!")

    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        value=st.secrets.api_key.openai,
    )

    anfield_api_key = st.sidebar.text_input(
        "Anfield API Key", type="password", value=st.secrets.api_key.anfield
    )

    has_valid_anfield_api_key = anfield_api_key and anfield_api_key.startswith("ak-")
    has_valid_openai_api_key = openai_api_key and openai_api_key.startswith("sk-")

    if not has_valid_anfield_api_key:
        st.warning("Please enter your Anfield API key!", icon="⚠")

    if not has_valid_openai_api_key:
        st.warning("Please enter your OpenAI API key!", icon="⚠")

    question_list = [
        "",
        "Which team was the best team in Gameweek 1?",
        "How many goals have been scored in Gameweek 1?",
        "Other",
    ]
    query_text = st.selectbox("Select an example query:", question_list)

    if query_text == "Other":
        query_text = st.text_input(
            "Enter your query:",
            placeholder="Enter query here ...",
        )

    if has_valid_anfield_api_key and has_valid_openai_api_key and query_text != "":
        st.header("Output")
        config.anfield_api_key = anfield_api_key
        config.openai_api_key = openai_api_key
        fpl_agent = FplAgent()
        generate_response(query_text, fpl_agent.executor)


main()
