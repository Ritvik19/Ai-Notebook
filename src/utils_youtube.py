import os
import json
import subprocess
import pandas as pd

SUBTITLES_JSON_FILE = "temp.en.json3"

def download_subtitles(youtube_url):
    if os.path.exists(SUBTITLES_JSON_FILE):
        os.remove(SUBTITLES_JSON_FILE)
    command = f"yt-dlp --write-auto-subs --sub-format json3 --skip-download --output temp {youtube_url}".split()
    subprocess.run(command, check=True, capture_output=True, text=True)

def load_transcript():
    if not os.path.exists(SUBTITLES_JSON_FILE):
        return ""
    with open(SUBTITLES_JSON_FILE) as file:
        json3_data = json.load(file)
    transcript = [
        seg["utf8"].strip()
        for event in json3_data.get("events", [])
        if "segs" in event
        for seg in event["segs"]
        if "utf8" in seg
    ]
    os.remove(SUBTITLES_JSON_FILE)
    return " ".join(transcript)

def get_video_title(youtube_url):
    command = ["yt-dlp", "--get-title", "--skip-download", youtube_url]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return result.stdout.strip()