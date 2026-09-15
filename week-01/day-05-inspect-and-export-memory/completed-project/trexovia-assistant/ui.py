import streamlit as st

from app import process_message
from memory import (
    count_messages,
    format_history_as_markdown,
    load_history,
)


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
    user_count = count_messages(history, "user")            # 1
    assistant_count = count_messages(history, "assistant")  # 2

    st.write(f"User messages: {user_count}")
    st.write(f"Assistant messages: {assistant_count}")

    with st.expander("Inspect saved memory"):  # 1
        st.json(history)

    st.download_button(
        "Download conversation",
        data=format_history_as_markdown(history),  # 1
        file_name="trevoxia-conversation.md",      # 2
        mime="text/markdown",                      # 3
        use_container_width=True,
    ) 

    if st.button("Clear history", use_container_width=True):
        process_message("clear", history)       # 2
        st.rerun()                              # 3