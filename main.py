import streamlit as st
from utils import create_assistant, delete_assistant, run_assistant, client

st.write("## Welcome to Openai Assitant beta 👋🏻")
st.write("By Akash Auti")

if "chat" not in st.session_state:
    st.session_state["chat"] = []
    st.session_state["assitant_name"] = None
    st.session_state["assitant_id"] = 0

assitant_list = []

assitants = list(client.beta.assistants.list())
for i in assitants:
    assitant_list.append({"name": i.name, "id": i.id, "instructions": i.instructions})
    assitant_id = i.id
    assitant_instructions = i.instructions

st.divider()

cols = st.columns((1, 1))
with cols[0]:
    selected_name = st.selectbox("Select a Name", [entry['name'] for entry in assitant_list])
    selected_assitant = next((entry for entry in assitant_list if entry['name'] == selected_name), None)
    if selected_assitant["name"] != st.session_state["assitant_name"]:
        st.session_state.clear()
        st.session_state["chat"] = []
        st.session_state["assitant_name"] = None
        st.session_state["assitant_id"] = 0
        st.session_state["thread_id"] = 0
    if selected_assitant is not None:
        assitant = client.beta.assistants.retrieve(assistant_id=assitant_id)
        st.session_state["assitant_name"] = selected_assitant["name"]
        st.session_state["assitant_id"] = selected_assitant["id"]
        st.session_state["messages"] = []
        st.session_state["instructions"] = selected_assitant["instructions"]
        st.session_state["thread_id"] = None

st.button("Create Assistant", on_click=create_assistant)
st.button("Delete Assitant", on_click=delete_assistant)


with cols[1]:
    st.write("Assitant Name:- ", st.session_state["assitant_name"])
    st.write("Assitant ID:- ", st.session_state["assitant_id"])
    st.write("Assitant Instructions:- ", st.session_state["instructions"])

st.divider()

prompt = st.chat_input(placeholder=" ", max_chars=None)
response = run_assistant(assitant_id=st.session_state["assitant_id"], thread_id=st.session_state["thread_id"] , prompt=prompt)

for message in st.session_state.chat:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state['chat'].append({"role": "user", "content": prompt})

    with st.chat_message("assitant"):
        st.markdown(response)
        st.session_state['chat'].append({"role": "assitant", "content": response})