import json
import os
import subprocess
import time
from datetime import datetime, timedelta

import pandas as pd
from tqdm import tqdm

from models import LLMs
from prompts import PROMPT_DICT
from utils_youtube import download_subtitles, load_transcript

ARTICLE_PROMPT = PROMPT_DICT["summary-article"]["prompt"]

def fetch_youtube_channel_data(channel_name):
    metadata_file = f"../youtube_news/{channel_name}/video_metadata.csv"
    command_urls = [
        "yt-dlp",
        "-s",
        "--flat-playlist",
        "--print",
        "%(webpage_url)s",
        f"https://www.youtube.com/@{channel_name}/videos",
    ]

    urls = subprocess.run(command_urls, capture_output=True, text=True).stdout.splitlines()
    print(f"Found {len(urls)} videos for channel {channel_name}.")

    data = []
    if os.path.exists(metadata_file):
        processed_metadata = pd.read_csv(metadata_file)
        processed_urls = processed_metadata["URL"].tolist()
    else:
        processed_metadata = pd.DataFrame()
        processed_urls = []
    print(f"Already fetched metadata of {len(processed_urls)} videos.")

    for url in tqdm(urls):
        if url not in processed_urls:
            command_metadata = [
                "yt-dlp",
                "-s",
                "--print",
                "%(upload_date)s %(title)s %(webpage_url)s",
                url,
            ]
            result = subprocess.run(command_metadata, capture_output=True, text=True).stdout.strip()
            if result:
                upload_date, *title, video_url = result.split(" ")
                title = " ".join(title)
                data.append({"Upload Date": upload_date, "Title": title, "URL": video_url})
        else:
            data.append({
                "Upload Date": processed_metadata[processed_metadata["URL"] == url]["Upload Date"].values[0], 
                "Title": processed_metadata[processed_metadata["URL"] == url]["Title"].values[0], 
                "URL": url
            })

    df_metadata = pd.DataFrame(data)
    df_metadata.to_csv(metadata_file, index=False)
    print(f"Saved metadata for {len(data)} videos to {metadata_file}.")


def backstagewithmillionaires(model, dates):
    fetch_youtube_channel_data("backstagewithmillionaires")
    df = pd.read_csv("../youtube_news/backstagewithmillionaires/video_metadata.csv")
    df = df[df.Title.str.contains("Indian Startup News", case=False)].reset_index(drop=True)
    df["Edition"] = df.Title.str.extract(r"Indian Startup News(?: Ep)? (\d+)", expand=False)

    for i, row in tqdm(df.iterrows(), total=len(df)):
        date = str(row["Upload Date"])  
        date = date[:4] + "-" + date[4:6] + "-" + date[6:]
        if date in dates and (not os.path.exists(f"../youtube_news/backstagewithmillionaires/newsletters/{date}.json")):
            try:
                download_subtitles(row.URL)
                transcript = load_transcript()
                data = {
                    "Edition": row.Edition, 
                    "Title": row.Title,
                    "URL": row.URL, 
                    "Upload Date": date,
                    "Transcript": transcript,
                    "Newsletter": f"# Backstage with millionaires newsletter from {date}" + create_article(transcript, model)
                }
                with open(f"../youtube_news/backstagewithmillionaires/newsletters/{date}.json", "w") as file:
                    json.dump(data, file)
            except Exception as e:
                print(f"Failed to process video {date} due to error: {e}")


CHANNELS = {
    "backstagewithmillionaires": backstagewithmillionaires,
}

def youtube_newsletter(channel, session_state, model_name):
    today = datetime.now()
    past_7_days = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

    model = LLMs[model_name]
    CHANNELS[channel](model, past_7_days)
    for date in past_7_days:
        if os.path.exists(f"../youtube_news/{channel}/newsletters/{date}.json"):
            newsletter = json.load(open(f"../youtube_news/{channel}/newsletters/{date}.json"))["Newsletter"]
            break
        else:
            newsletter = f"No newsletter found for the past 7 days for {channel}."
    session_state["messages"].extend([
        {"role": "user", "content": f"Fetch me the {channel} newsletter from the past 7 days"},
        {"role": "assistant", "content": newsletter}
    ])
    return newsletter

def create_article(transcript, model, retries=10, delay=30):
    for attempt in range(retries):
        try:
            response = model.invoke([
                {"role": "user", "content": ARTICLE_PROMPT.format(context=transcript)},
            ])
            article = response.content
            _, *article = article.split("\n")
            article = "\n".join(article)
            return article
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
                delay = int(delay * 1.1)
            else:
                raise TimeoutError("Request timed out after multiple attempts")