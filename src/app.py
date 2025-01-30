import streamlit as st

st.set_page_config(page_title="AI Notebook", layout="wide")

from converse import get_response
from models import LLMs
from prompts import PROMPT_DICT
from sources import add_source, clear_sources, display_sources, remove_sources

if "messages" not in st.session_state:
    st.session_state.messages = []
if "pinned" not in st.session_state:
    st.session_state.pinned = []

st.title("Ai Notebook")
tab1, tab2, tab3 = st.tabs(["Manage Sources", "Converse", "View Pinned Notes"])

with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write("Add Sources")
        copied_text = st.text_area("Paste your text here")
        uploaded_file = st.file_uploader(
            "Choose a text file",
            accept_multiple_files=True,
            type=["txt", "md", "csv", "tsv", "ods", "xls", "xlsx", "xlsb", "xlsm", "pdf"],
        )
        url = st.text_input("Enter a webpage / youtube / pdf URL")
        l, r = st.columns([1, 1])
        add_source_button = l.button("Add Source")
        clear_sources_button = r.button("Clear Sources")

    with col2:
        st.write("All Sources")
        sources_display_manage = st.empty()
        indices_to_delete = st.text_input("Indices to delete (space separated)", value="")
        sources_delete_button = st.button("Delete")


with tab2:
    col1, col2 = st.columns([1, 2])
    with col1:
        with st.expander("Instructions"):
            st.write("This is a conversational AI assistant that can answer questions based on a given context.")
            st.write("You can interact with the assistant by typing in the chat box.")
            st.write("You can also use the following models and functions")
            st.write("Generic Instruction format:")
            st.code("@model_name /function query")

        with st.expander("Models"):
            models = [f"@{llm}" for llm in list(LLMs.keys())]
            for model in models:
                st.code(model)

        with st.expander("Functions"):
            functions = [f"/{func}" for func in [
                "pin", "unpin", 
                "save", "load", "list", "delete", "clear", 
                "hf-news", "mbz-news", "bwm-news", "news",  
                *PROMPT_DICT.keys()
            ]]
            for function in functions:
                st.code(function)
        sources_display_converse = st.empty()
        selected_sources = st.text_input("Selected sources (space separated)", value="")
    with col2:
        for e, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                if message["role"] == "assistant":
                    st.markdown(f"{e//2}]")
                st.markdown(message["content"])

        if prompt := st.chat_input("What is up?"):
            st.chat_message("user").markdown(prompt)
            response = get_response(prompt, selected_sources, st.session_state)
            with st.chat_message("assistant"):
                st.markdown(response)

with tab3:
    cols = st.columns(3)
    for e, message in enumerate(st.session_state.pinned):
        with cols[e % 3]:
            st.write(f"{e}]")
            st.write(f'{message["response"]}\n\n---')

display_sources(sources_display_manage, sources_display_converse)
if add_source_button:
    add_source(
        sources_display=sources_display_manage,
        sources_selection_display=sources_display_converse,
        copied_text=copied_text,
        uploaded_file=uploaded_file,
        url=url
    )
if clear_sources_button:
    clear_sources(sources_display_manage, sources_display_converse)
if sources_delete_button:
    remove_sources(indices_to_delete, sources_display_manage, sources_display_converse)
