import streamlit as st
from graph_builder import build_graph

st.title("Logical-Emotional Chatbot")

# Initialize session state
if "graph" not in st.session_state:
    st.session_state.graph = build_graph()
if "state" not in st.session_state:
    st.session_state.state = {"messages": [], "message_type": None}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input at the bottom
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.state["messages"] = st.session_state.chat_history.copy()
    # Get assistant response
    st.session_state.state = st.session_state.graph.invoke(st.session_state.state)
    last_message = st.session_state.state["messages"][-1]
    # Handle both dict and object with .content
    content = last_message["content"] if isinstance(last_message, dict) else getattr(last_message, "content", str(last_message))
    st.session_state.chat_history.append({"role": "assistant", "content": content})

# Display chat history (like ChatGPT)
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
