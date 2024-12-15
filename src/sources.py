import os
import re
import pandas as pd
import requests
import streamlit as st

from utils_pdf import process_pdf
from utils_youtube import download_subtitles, load_transcript, get_video_title



SOURCES_FILE = "sources.jsonl"

def read_sources():
    return (
        pd.read_json(SOURCES_FILE, lines=True)
        if os.path.exists(SOURCES_FILE)
        else pd.DataFrame(columns=["timestamp", "title", "text"])
    )


def add_source(sources_display, sources_selection_display, **sources):
    if copied_text := sources.get("copied_text"):
        add_text(copied_text)
    if uploaded_file := sources.get("uploaded_file"):
        add_file(uploaded_file)
    if url := sources.get("url"):
        add_web(url)
    display_sources(sources_display, sources_selection_display)


def remove_sources(indices_to_delete, sources_display_manage, sources_display_converse):
    sources = read_sources()
    indices = [int(i) for i in indices_to_delete.split(",") if i != ""]
    sources = sources.drop(indices)
    sources.to_json(SOURCES_FILE, lines=True, orient="records")
    display_sources(sources_display_manage, sources_display_converse)


def clear_sources(sources_display, sources_selection_display):
    if os.path.exists(SOURCES_FILE):
        os.remove(SOURCES_FILE)
    display_sources(sources_display, sources_selection_display)


def display_sources(sources_display_manage, sources_display_converse):
    sources = read_sources()
    sources_display_manage.write(sources)
    sources_display_converse.write(sources)


def append_sources(new_sources):
    sources = read_sources()
    sources = pd.concat([sources, new_sources])
    sources.to_json(SOURCES_FILE, lines=True, orient="records")


def add_text(text):
    append_sources(pd.DataFrame({"timestamp": [pd.Timestamp.now()], "title": ["Copied Text"], "text": [text]}))


def add_file(files):
    text_files = [file for file in files if file.name.endswith((".txt", ".md"))]
    text_sources = text_files_to_sources(text_files)

    csv_files = [file for file in files if file.name.endswith((".csv", ".tsv"))]
    csv_sources = csv_files_to_sources(csv_files)

    excel_files = [file for file in files if file.name.endswith((".xls", ".xlsx", ".xlsb", ".xlsm", ".ods"))]
    excel_sources = excel_files_to_sources(excel_files)

    pdf_files = [file for file in files if file.name.endswith(".pdf")]
    pdf_sources = pdf_files_to_sources(pdf_files)

    append_sources(pd.concat([text_sources, csv_sources, excel_sources, pdf_sources]))    

def add_web(url):
    if "youtu.be" in url or "youtube.com" in url:
        append_sources(youtube_to_sources(url))
    elif requests.get(url).headers.get("Content-Type") == "application/pdf":
        append_sources(web_pdf_to_sources(url))
    else:
        append_sources(web_page_to_sources(url))

def text_files_to_sources(text_files):
    return pd.DataFrame(
        {
            "timestamp": [pd.Timestamp.now() for _ in text_files],
            "title": [file.name for file in text_files],
            "text": [file.getvalue().decode("utf-8") for file in text_files],
        }
    )

def csv_files_to_sources(csv_files):
    sources = []
    for file in csv_files:
        df = pd.read_csv(file, sep="\t" if file.name.endswith(".tsv") else ",")
        sources.append(
            {
                "timestamp": pd.Timestamp.now(),
                "title": file.name,
                "text": df.to_markdown(),
            }
        )   
    return pd.DataFrame(sources) 

def excel_files_to_sources(excel_files):
    sources = []
    for file in excel_files:
        excel_data = pd.read_excel(file, sheet_name=None, engine="odf" if file.name.endswith(".ods") else "openpyxl")
        sources.extend(
            [
                {
                    "timestamp": pd.Timestamp.now(),
                    "title": f"{file.name} - {sheet_name}",
                    "text": df.to_markdown(),
                }
                for sheet_name, df in excel_data.items()
            ]
        )
    return pd.DataFrame(sources)

def pdf_files_to_sources(pdf_files):
    sources = []
    for file in pdf_files:
        pdf_data = process_pdf(file=file)
        sources.extend(pdf_data)
    return pd.DataFrame(sources)    

def web_page_to_sources(url):
    res = requests.get(f"https://r.jina.ai/{url}")
    if res.status_code == 200:
        content = res.text
        title_match = re.search(r"Title:\s*(.*)", content)
        title = title_match.group(1) if title_match else "Untitled"

        markdown_match = re.search(r"Markdown Content:\s*([\s\S]*)", content)
        markdown = markdown_match.group(1).strip() if markdown_match else ""

        return pd.DataFrame({"timestamp": [pd.Timestamp.now()], "title": [title], "text": [markdown]})

def youtube_to_sources(youtube_url):
    download_subtitles(youtube_url)
    formatted_text = load_transcript()
    title = get_video_title(youtube_url)
    return pd.DataFrame({"timestamp": [pd.Timestamp.now()], "title": [title], "text": [formatted_text]})

def web_pdf_to_sources(url):
    document_snippets = process_pdf(url=url)
    return pd.DataFrame(document_snippets)
