from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_openai import AzureChatOpenAI

LLMs = {
    "gemma2": ChatOllama(model="gemma2:9b", temperature=0),
    "granite3": ChatOllama(model="granite3-dense:8b", temperature=0),
    "hermes3": ChatOllama(model="hermes3:8b", temperature=0),
    "llama3": ChatOllama(model="llama3:8b", temperature=0),
    "llama3.1": ChatOllama(model="llama3.1:8b", temperature=0),
    "ministral": ChatOllama(model="hf.co/Ritvik19/Ministral-8B-Instruct-2410-Q4_K_M-GGUF:latest", temperature=0),
    "mistral": ChatOllama(model="mistral:7b", temperature=0),
    "nemo": ChatOllama(model="mistral-nemo:12b", temperature=0),
    "phi3": ChatOllama(model="phi3:14b", temperature=0),
    "phi3.5": ChatOllama(model="phi3.5:3.8b", temperature=0),
    "gemini-flash": ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        max_tokens=None,
        api_key="API_KEY",
    )
}