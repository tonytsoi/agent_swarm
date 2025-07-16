from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from langgraph_swarm import  create_swarm
import streamlit as st
import uuid
from math_teacher import math_teacher
from english_teacher import english_teacher 
from history_teacher import history_teacher 

# Create agent swarm
workflow = create_swarm(
    [math_teacher, english_teacher, history_teacher],
    default_active_agent="Math Teacher",
)
checkpointer = MemorySaver()    
app = workflow.compile(checkpointer=checkpointer)

thread_id = uuid.uuid4()
config = {"configurable": {"thread_id": thread_id, "parallel_tool_calls": False}}

def generate_response(input_text):
    # Use the agents
    config = {"configurable": {"thread_id": "abc123"}}
    for step in app.stream(
            {"messages": [HumanMessage(content=f"{input_text}")]},
            config,
            stream_mode="values",
    ):
        
        if step["messages"][-1].type != 'human':
            for sentence in step["messages"][-1].content.split("/n"):
                yield sentence + "  \n\n"
            # Print all outputs
            # yield step["messages"][-1]
                     
st.title("Multi-Agent Swarm")
st.caption("Powered by Llama 4 Maverick")
st.image("agent_swarm.jpg")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message['content'])

# Accept user input
if prompt := st.chat_input("What do you want to ask?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(generate_response(prompt))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})