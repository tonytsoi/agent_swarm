from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langgraph_swarm import create_handoff_tool
from langchain_tavily import TavilySearch
import os
import credentials

os.environ['AWS_DEFAULT_REGION'] = "us-east-1"
os.environ["AWS_ACCESS_KEY_ID"] = credentials.access_key
os.environ["AWS_SECRET_ACCESS_KEY"] = credentials.secret_key
tavily_api_key = credentials.tavily_api_key

llm = init_chat_model("us.meta.llama4-maverick-17b-instruct-v1:0",
                            model_provider="bedrock_converse")

web_search = TavilySearch(max_results=3, tavily_api_key=tavily_api_key)

transfer_to_math_teacher = create_handoff_tool(
    agent_name="Math Teacher",
    description="Transfer user to the Mathematics teacher.",
)

transfer_to_history_teacher = create_handoff_tool(
    agent_name="History Teacher",
    description="Transfer user to the History teacher.",
)

english_teacher = create_react_agent(
    model=llm,
    tools=[web_search, transfer_to_math_teacher, transfer_to_history_teacher],
    prompt=(
        "You are an English teacher who answers questions about English grammar."
    ),
    name="English Teacher",
)