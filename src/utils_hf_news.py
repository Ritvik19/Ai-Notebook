import os
import time
from datetime import datetime, timedelta

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

from models import LLMs
from prompts import PAPER_SUMMARY_PROMPT as prompt

article_template = """
## {index}: {title}
![{title}]({image})

{summary}

{abstract}

[Read Paper]({url})
"""


def summarise_abstract(abstract, model, retries=10, delay=30):
    for attempt in range(retries):
        try:
            response = model.invoke([
                {"role": "system", "content": prompt},
                {"role": "user", "content": abstract},
            ])
            return "\n".join([f"* {line}" for line in response.content.strip().split(". ")])
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
                delay = int(delay * 1.1)
            else:
                raise TimeoutError("Request timed out after multiple attempts")

def fetch_page_content(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def extract_article_data(article):
    title = article.select_one("h3 > a").text
    relative_url = article.select_one("h3 > a").get("href")
    hf_url = f"https://huggingface.co{relative_url}"
    archive_url = relative_url.replace("/papers", "https://arxiv.org/abs")
    try:
        image_url = article.select_one("img.object-cover").get("src")
    except AttributeError:
        image_url = None
    return title, archive_url, hf_url, image_url

def fetch_and_summarize_abstract(hf_url, model):
    article_content = fetch_page_content(hf_url)
    abstract = article_content.select_one("p").text
    summary = summarise_abstract(abstract, model)
    return abstract, summary

def generate_newsletter(date, data):
    newsletter = f"# ML Newsletter: {date}\n"
    for idx, row in enumerate(data, start=1):
        newsletter += article_template.format(
            index=idx,
            title=row["title"],
            image=row["image"],
            summary=row["summary"],
            abstract=row["abstract"],
            url=row["url"]
        )
    return newsletter

def hf_news(date, session_state, model_name):
    date = date.strip()
    if date == "-r":
        end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        beg_date = "2023-05-04"
        letters = []
        for date in pd.date_range(beg_date, end_date).strftime('%Y-%m-%d'):
            if f"newsletter-{date}.jsonl" not in os.listdir("../newsletters"):
                print(f"Fetching newsletter for {date}")
                letters.append(hf_news(date, session_state, model_name))
        return "\n\n".join(letters)
    
    if date == "":
        date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    print(date)
    url = f"https://huggingface.co/papers?date={date}"
    content = fetch_page_content(url)
    model = LLMs[model_name]

    articles = content.select("article")
    print(len(articles))
    data = []
    for article in tqdm(articles):
        try:
            title, archive_url, hf_url, image_url = extract_article_data(article)
            abstract, summary = fetch_and_summarize_abstract(hf_url, model)
            
            data.append({
                "title": title,
                "url": archive_url,
                "image": image_url,
                "abstract": abstract,
                "summary": summary
            })
        except:
            print(f"Failed to process article: {article}")
    pd.DataFrame(data).to_json(f"../newsletters/newsletter-{date}.jsonl", lines=True, orient="records")

    newsletter = generate_newsletter(date, data)
    session_state["messages"].extend([
        {"role": "user", "content": f"Fetch me the Hugging Face newsletter, dated: {date}"},
        {"role": "assistant", "content": newsletter}
    ])    
    
    return newsletter
