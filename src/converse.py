import re

import pandas as pd

from models import LLMs
from prompts import PROMPT_DICT, RAG
from sources import read_sources
from utils_hf_news import hf_news
from datetime import datetime


def parse_sources(sources):
    if sources.strip() == "":
        return []
    return [int(source_id) for source_id in sources.split()]


def parse_string(input_string, default_model="gemma2"):
    res = {"model_name": default_model, "function": None, "query": None}
    if input_string.startswith("@"):
        input_ = input_string[1:].split(" ")
        res["model_name"] = input_[0]
        input_string = " ".join(input_[1:])
    if input_string.startswith("/"):
        input_ = input_string[1:].split(" ")
        res["function"] = input_[0]
        input_string = " ".join(input_[1:])
    res["query"] = input_string
    return res

def call_model(model_name, conversation):
    response = LLMs[model_name].invoke(conversation).content
    return "\n".join(response) if model_name == "gemini-thinking" else response

def get_response(input_string, sources_string, session_state):
    input_string = input_string.strip()
    parsed_string = parse_string(input_string)
    parsed_sources = parse_sources(sources_string)
    context = "\n\n".join(read_sources().loc[parsed_sources]["text"].values)

    if not parsed_string:
        return "Invalid query format"
    
    model_name = parsed_string["model_name"]
    _function = parsed_string["function"]
    query = parsed_string["query"]

    if model_name not in LLMs:
        return "Invalid model name"
    
    if _function:
        return handle_function(_function, query, session_state, model_name, context)
    else:
        return handle_query(query, model_name, context, session_state)


def handle_function(_function, query, session_state, model_name, context):
    if _function == "pin":
        return pin_message(query, session_state)
    elif _function == "unpin":
        return unpin_message(query, session_state)
    elif _function == "save":
        return save_conversation(query, session_state)
    elif _function == "clear":
        return clear_conversation(session_state)
    elif _function == "hf-news":
        return hf_news(query, session_state, model_name)
    elif _function in PROMPT_DICT:
        return generate_response(model_name, _function, query, context, session_state)
    else:
        return "Invalid function"


def pin_message(query, session_state):
    index = int(query) * 2 + 1 if query else len(session_state["messages"]) - 1
    session_state["pinned"].append({
        "query": session_state["messages"][index - 1]["content"],
        "context": session_state["messages"][index - 1].get("context", ""),
        "response": session_state["messages"][index]["content"],
    })
    return "Message pinned"


def unpin_message(query, session_state):
    index = int(query) if query else len(session_state["pinned"]) - 1
    session_state["pinned"].pop(index)
    return "Message unpinned"


def save_conversation(query, session_state):
    for message in session_state.messages:
        message["pinned"] = message.get("pinned", False)
        message["context"] = message.get("context", "")
    
    pd.DataFrame(session_state.messages).to_json(f"../saved-data/{query}-conversation.jsonl", lines=True, orient="records")
    pd.DataFrame(session_state.pinned).to_json(f"../saved-data/{query}-pinned.jsonl", lines=True, orient="records")
    read_sources().to_json(f"../saved-data/{query}-sources.jsonl", lines=True, orient="records")
    
    return "Conversation, Pinned Notes, Sources saved"


def clear_conversation(session_state):
    session_state.messages = []
    return "Conversation will be cleared"


def generate_response(model_name, function, query, context, session_state):
    conversation = [{"role": "user", "content": PROMPT_DICT[function]["prompt"].format(query=query, context=context)}]
    llm_response = call_model(model_name, conversation)
    
    session_state.messages.append({
        "role": "user", "content": PROMPT_DICT[function]["instruction"].format(query=query), "context": context
    })
    session_state.messages.append({"role": "assistant", "content": llm_response})
    pd.DataFrame(session_state.messages).to_json(f"../logs/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.jsonl", lines=True, orient="records")
    return llm_response


def handle_query(query, model_name, context, session_state):
    conversation = [{"role": message["role"], "content": message["content"]} for message in session_state.messages]
    conversation.append({"role": "user", "content": RAG.format(context=context, query=query)})
    
    llm_response = call_model(model_name, conversation)
    session_state.messages.append({"role": "user", "content": query, "context": context})
    session_state.messages.append({"role": "assistant", "content": llm_response})
    pd.DataFrame(session_state.messages).to_json(f"../logs/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.jsonl", lines=True, orient="records") 
    return llm_response
