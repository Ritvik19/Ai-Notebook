import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_openai import AzureChatOpenAI

GEMINI_API_KEY = os.environ.get("GEMINI_KEY")
GEMINI_KWARGS = dict(temperature=0, max_tokens=None, api_key=GEMINI_API_KEY)

LLMs = {
    "gemma2": ChatOllama(model="gemma2:9b", temperature=0),
    "llama3": ChatOllama(model="llama3:8b", temperature=0),
    "llama3.1": ChatOllama(model="llama3.1:8b", temperature=0),
    "gemini-flash": ChatGoogleGenerativeAI(model="gemini-1.5-flash", **GEMINI_KWARGS),
    "gemini-pro": ChatGoogleGenerativeAI(model="gemini-1.5-pro", **GEMINI_KWARGS),
    "gemini-2": ChatGoogleGenerativeAI(model="gemini-2.0-flash", **GEMINI_KWARGS),
    "gemini-thinking": ChatGoogleGenerativeAI(model="gemini-2.0-flash-thinking-exp", **GEMINI_KWARGS),
    "learnlm": ChatGoogleGenerativeAI(model="learnlm-1.5-pro-experimental", **GEMINI_KWARGS),
    "gemini-2.5": ChatGoogleGenerativeAI(model="gemini-2.5-pro-exp-03-25", **GEMINI_KWARGS),
    "gpt4o": AzureChatOpenAI(
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        openai_api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
        deployment_name=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME"),
        openai_api_key=os.environ.get("AZURE_OPENAI_KEY"),
        openai_api_type="azure",
        temperature=0.0,
    )
}