import os
import time
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def create_assistant():
    """
    You currently cannot set the temperature for Assistant via the API.
    """
    assistant = client.beta.assistants.create(
        name=input("Name of assistant: "),
        instructions=input("Instructions: "),
        tools=[{"type": "retrieval"}],
        model="gpt-3.5-turbo-1106",
    )
    return assistant


def run_assistant(assitant_id, thread_id, prompt):
    """Running the assistant while creating a new thread and run"""
    assitant = client.beta.assistants.retrieve(assistant_id=assitant_id)
    thread = client.beta.threads.create(messages=[{"role": "user", "content": " " if prompt is None else prompt}])
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assitant.id
    ) 

    while run.status != "completed":
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    
    message = client.beta.threads.messages.list(thread_id=thread.id)
    new_message = message.data[0].content[0].text.value
    return new_message


def delete_assistant():
    """Delete the assistant"""
    client.beta.assistants.delete(assistant_id=st.session_state["assitant_id"])
