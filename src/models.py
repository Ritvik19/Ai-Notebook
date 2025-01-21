from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_openai import AzureChatOpenAI

GEMINI_KWARGS = dict(temperature=0, max_tokens=None, api_key=GEMINI_API_KEY)

LLMs = {
    "gemma2": ChatOllama(model="gemma2:9b", temperature=0),
    "llama3": ChatOllama(model="llama3:8b", temperature=0),
    "llama3.1": ChatOllama(model="llama3.1:8b", temperature=0),
    "gemini-flash": ChatGoogleGenerativeAI(model="gemini-1.5-flash", **GEMINI_KWARGS),
    "gemini-pro": ChatGoogleGenerativeAI(model="gemini-1.5-pro", **GEMINI_KWARGS),
    "gemini-2": ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", **GEMINI_KWARGS),
    "gemini-thinking": ChatGoogleGenerativeAI(model="gemini-2.0-flash-thinking-exp", **GEMINI_KWARGS),
}