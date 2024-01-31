import streamlit as st
from langchain.agents import AgentExecutor
from langchain_community.callbacks import StreamlitCallbackHandler

from agent import FplAgent


def generate_response(input_query: str, agent_executor: AgentExecutor):
    st_callback = StreamlitCallbackHandler(st.container())
    response = agent_executor.invoke(
        {"input": input_query, "chat_history": []}, callbacks=[st_callback]
    )
    return st.success(response["output"])


def main():
    st.set_page_config(page_title="🦜🔗 Ask about Fantasy PL")
    st.title("🦜🔗 Ask about Fantasy PL")

    question_list = [
        "Which team was the best team in Gameweek 1?",
        "How many goals have been scored in Gameweek 1?",
        "Other",
    ]
    query_text = st.selectbox("Select an example query:", question_list)
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

    if query_text == "Other":
        query_text = st.text_input(
            "Enter your query:",
            placeholder="Enter query here ...",
        )

    if not openai_api_key.startswith("sk-"):
        st.warning("Please enter your OpenAI API key!", icon="⚠")
    if openai_api_key.startswith("sk-"):
        st.header("Output")
        agent = FplAgent(model="gpt-4-0125-preview", openai_api_key=openai_api_key)
        generate_response(query_text, agent.executor)


main()
