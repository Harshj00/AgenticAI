import os
import streamlit as st
from agent import Agent
from memory import load_memory, save_memory

st.set_page_config(page_title="Agent UI")

if 'agent' not in st.session_state:
    st.session_state.agent = Agent()
    st.session_state.history = load_memory()
    st.session_state.last_user = ""
    st.session_state.last_response = ""

st.title("AI Agent (Streamlit)")

with st.sidebar:
    st.header("Controls")
    if st.button("Clear Memory"):
        save_memory([])
        st.session_state.history = []
        st.success("Memory cleared.")

user_input = st.text_input("You:", key="user_input")
if st.button("Send") and user_input:
    with st.spinner("Thinking..."):
        try:
            response = st.session_state.agent.run(user_input)
        except Exception as e:
            response = f"Error: {e}"
    # update local history for display and clear input
    st.session_state.history = load_memory()
    # clear the input box for next message
    try:
        st.session_state.user_input = ""
    except Exception:
        pass
    # keep last conversation pair in session state so we can display immediately
    st.session_state.last_user = user_input
    st.session_state.last_response = response

st.subheader("Conversation")
mem = st.session_state.get('history', [])
if not mem:
    st.info("No conversation yet. Say something to start.")
else:
    # show the most recent response immediately at the top if available
    if st.session_state.get('last_response'):
        if st.session_state.get('last_user'):
            st.markdown(f"**You:** {st.session_state.last_user}")
        st.markdown(f"**Agent:** {st.session_state.last_response}")
        st.write("---")
    for m in mem:
        role = m.get('role','')
        content = m.get('content','')
        if role == 'user':
            st.markdown(f"**You:** {content}")
        elif role == 'assistant':
            st.markdown(f"**Agent:** {content}")
        else:
            st.markdown(f"**{role}:** {content}")
