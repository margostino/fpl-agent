from langchain.prompts import PromptTemplate

FPL_AGENT_PROMPT = PromptTemplate.from_template(
    """
        SYSTEM
        You are a helpful assistant. 
        Your job is to answer questions as the best you can about Premier League Gameweeks (season 2023/24). 
        
        PLACEHOLDER
        {chat_history}
        
        HUMAN
        {input}

        PLACEHOLDER
        {agent_scratchpad}
    """
)
