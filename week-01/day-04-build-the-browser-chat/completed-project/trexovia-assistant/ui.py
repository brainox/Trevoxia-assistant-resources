import streamlit as st

from app import process_message
from memory import load_history


st.set_page_config(
    page_title="Trevoxia Assistant",  # 1
    page_icon="💬",
)

if "history" not in st.session_state:          # 1
    st.session_state.history = load_history()  # 2

history = st.session_state.history             # 3

st.title("Trevoxia Assistant")
st.caption("A browser chat with persistent JSON memory")

for message in history:                     # 1
    with st.chat_message(message["role"]):  # 2
        st.markdown(message["content"])  

if user_message := st.chat_input("Message Trevoxia"):  # 1
    with st.chat_message("user"):
        st.markdown(user_message)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):            # 2
                reply = process_message(
                    user_message,
                    history,
                )
            st.markdown(reply)                         # 3
    except Exception as error:
        st.error(f"I could not generate a response: {error}")  # 4

with st.sidebar:
    st.subheader("Memory")
    # user message: count
    st.write(f"User messages: {len([msg for msg in history if msg['role'] == 'user'])}")  # 2
    # Assistant message count
    st.write(f"Assistant messages: {len([msg for msg in history if msg['role'] == 'assistant'])}")  # 3

    if st.button("Clear history", use_container_width=True):
        process_message("clear", history)       # 2
        st.rerun()                              # 3