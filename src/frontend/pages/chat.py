
import streamlit as st

st.set_page_config(page_title="Zoro AI")

st.title("Zoro AI")

st.text(f"Greetings, {st.session_state.get("username")}!")

st.divider()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask anything"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream("Dummy Message")
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
