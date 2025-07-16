from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langgraph_swarm import create_handoff_tool
import os
import credentials

os.environ['AWS_DEFAULT_REGION'] = "us-east-1"
os.environ["AWS_ACCESS_KEY_ID"] = credentials.access_key
os.environ["AWS_SECRET_ACCESS_KEY"] = credentials.secret_key

llm = init_chat_model("us.meta.llama4-maverick-17b-instruct-v1:0",
                            model_provider="bedrock_converse")

def add(a: float, b: float):
    """Add two numbers."""
    return a + b


def multiply(a: float, b: float):
    """Multiply two numbers."""
    return a * b


def divide(a: float, b: float):
    """Divide two numbers."""
    return a / b

transfer_to_history_teacher = create_handoff_tool(
    agent_name="History Teacher",
    description="Transfer user to the History teacher.",
)

transfer_to_english_teacher = create_handoff_tool(
    agent_name="English Teacher",
    description="Transfer user to the English teacher.",
)

math_teacher = create_react_agent(
    model=llm,
    tools=[add, multiply, divide,
           transfer_to_history_teacher, transfer_to_english_teacher],
    prompt=(
        "You are a Mathematics teacher who answers questions about Mathematics only."
    ),
    name="Math Teacher",
)