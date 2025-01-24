import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import streamlit as st
import os
import subprocess

API = 'API'
SCRAPER = 'SCRAPER'


def search_youtube_with_API(song_name, api_key, max_results=1):
    try:
        # Initialize YouTube API client
        youtube = build('youtube', 'v3', developerKey=api_key)

        # Perform the search
        search_response = youtube.search().list(
            q=song_name,
            part='snippet',
            maxResults=max_results,
            type='video'
        ).execute()

        # Extract the first video link and title
        if search_response['items']:
            video_id = search_response['items'][0]['id']['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            video_title = search_response['items'][0]['snippet']['title']
            return video_title, video_url
        return None, None
    except HttpError as e:
        if e.resp.status == 403:
            st.text('Quota exceeded. Come back in 24h.')
            st.session_state.quota_exceeded = True
            return None, None
        else:
            print(f"An error occurred: {e}")
            return None, None


def create_youtube_playlist_from_spotify(spotify_df, api_key):
    youtube_titles = []
    youtube_urls = []
    
    for _, row in spotify_df.iterrows():
        song_name = f"{row['name']} {row['artist']}"
        if(not st.session_state.quota_exceeded and type(row['YouTube_Title'])!=str):
            youtube_title, youtube_url = search_youtube_with_API(song_name, api_key)
            
            if(youtube_url is not None):
                st.text(f"Found: {song_name} -> {youtube_title} -> {youtube_url}")
        else:
            youtube_title, youtube_url = row['YouTube_Title'], row['YouTube_URL']
        
        # Append the data to the lists
        youtube_titles.append(youtube_title)
        youtube_urls.append(youtube_url)
        
    # Add the YouTube columns to the DataFrame
    spotify_df['YouTube_Title'] = youtube_titles
    spotify_df['YouTube_URL'] = youtube_urls

    return spotify_df

# TODO: automatizar la parada cuando se supera la cuota, guardar el estado con temporizador de 24h
st.set_page_config(layout="wide")
st.title("Link extractor")
st.text('Here you can get the links to the songs on your playlists.')
st.text('This uses the Youtube API which has a quota of a 100 requests a day.')

# https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas?inv=1&invt=AblV9w&project=youtube-music-search-446115&pageState=(%22allQuotasTable%22:(%22s%22:%5B(%22i%22:%22currentPercent%22,%22s%22:%221%22),(%22i%22:%22sevenDayPeakPercent%22,%22s%22:%220%22),(%22i%22:%22currentUsage%22,%22s%22:%221%22),(%22i%22:%22sevenDayPeakUsage%22,%22s%22:%220%22),(%22i%22:%22serviceTitle%22,%22s%22:%220%22),(%22i%22:%22displayName%22,%22s%22:%220%22),(%22i%22:%22displayDimensions%22,%22s%22:%220%22)%5D,%22f%22:%22%255B%255D%22))
api_key = 'AIzaSyCUc2-Xr3_OLVSt6Cga60hBmGS4N-hp6Ak'
st.session_state.quota_exceeded = False

# Get url
playlist_name = st.selectbox('Select a playlist', [file for file in os.listdir('data/') if file.endswith('.csv')])
method = st.selectbox('Choose an option:', [API, SCRAPER], index=0)

if(method==SCRAPER):
    st.markdown(
        """
        <div style="background-color: #ff9800; padding: 10px; border-radius: 5px; text-align: center;">
            <strong style="color: #cc0000;">WARNING:</strong> 
            <span style="color: #000; font-size: 16px;">You need to accept the cookies manually so the scraper can work freely.</span>
        </div>
        """, unsafe_allow_html=True
    )
if(st.button('Get links')):
    path = f'data/{playlist_name}'
    if(method==API):
        df = create_youtube_playlist_from_spotify(pd.read_csv(path, sep=';'), api_key, method)
        df.to_csv(path, index=False, sep=';')
    elif(method==SCRAPER):
        with st.spinner("Launching scraper..."):
            # Pass arguments to the scraper
            subprocess.Popen(
                ["python", "scripts/youtube_scraper.py", "--path", path],
                stdout=None,  # Suppress output if not needed
                stderr=None,
                start_new_session=True  # Ensure it runs independently
            )
        st.success(f"Scraper finished for {playlist_name}!")
        st.text('Check the results as errors are not caught here.')
        
