

import data
from yt_dlp import YoutubeDL
import pandas as pd
import argparse
import data
import os

def download_playlist(path):
    downloaded_songs = []
    def progress_hook(d):
        if d["status"] == "finished":
            url = d["info_dict"]["original_url"]
            downloaded_songs.append(url)  # Store for later


    options = {
        "outtmpl": f"/home/miquel/Descargas/{os.path.basename(path).split('.')[0]}/%(title)s.%(ext)s",
        "progress_hooks": [progress_hook],
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "256",  # You can change the bitrate
            }
        ],
    }



    df = data.read_as_df(path)

    if('downloaded' not in df.columns):
        df['downloaded'] = [False for i in range(len(df))]
        
    try:
        urls = df[~ df["downloaded"]]["YouTube_URL"].values
        with YoutubeDL(options) as ydl:
            ydl.download(urls)

        df.loc[df["YouTube_URL"].isin(downloaded_songs), "downloaded"] = True
        data.save_df(df, path)

    except:
        df.loc[df["YouTube_URL"].isin(downloaded_songs), "downloaded"] = True
        data.save_df(df, path)



if(__name__=='__main__'):
    parser = argparse.ArgumentParser(description="Scraper script.")
    parser.add_argument("--path", type=str, required=True, help="Path to playlist")
    args = parser.parse_args()
    download_playlist(args.path)