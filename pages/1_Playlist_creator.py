import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import os
import streamlit as st
import shutil
from datetime import datetime
import unicodedata
import re


def get_playlist_data(sp, playlist_id):
    all_tracks = []
    offset = 0
    limit = 100

    while True:
        try:
            response = sp.playlist_items(playlist_id, offset=offset, limit=limit)
            items = response['items']
            if not items:  # Stop if no more tracks
                break
            
            st.text(f'Gotten first {offset+len(items)} songs!')
            for item in items:
                track = item['track']
                if track:  # Check if track is not None
                    # Fetch artist genres
                    artist_ids = [artist['id'] for artist in track['artists']]
                    genres = []
                    for artist_id in artist_ids:
                        artist_info = sp.artist(artist_id)
                        genres.extend(artist_info.get('genres', []))
                    
                    track_info = {
                        'name': track['name'],
                        'artist': ', '.join(artist['name'] for artist in track['artists']),
                        'album': track['album']['name'],
                        'release_date': track['album']['release_date'],
                        'duration_ms': track['duration_ms'],
                        'popularity': track['popularity'],
                        'genres': list(set(genres))  # Remove duplicates
                    }
                    all_tracks.append(track_info)
            
            offset += limit
        except Exception as e:
            print(f"Error: {e}")
            break

    return pd.DataFrame(all_tracks)

def clean_genres(genres):
    if(type(genres)==list):
        genres = str(genres)
    if(type(genres)==str):
        return genres.replace('"','').replace("'",'').replace('[', '').replace(']', '')
    return genres

def clean_data(data):
    if(type(data)!=str):
        data = str(data)
    normalized = unicodedata.normalize('NFKD', data)
    # Remove diacritical marks (e.g., accents, umlauts)
    without_accents = ''.join(c for c in normalized if not unicodedata.combining(c))
    # Remove other "weird" characters (non-alphanumeric, except spaces, dashes, and underscores)
    cleaned = re.sub(r'[^a-zA-Z0-9 _-,]', '', without_accents)
    return cleaned.strip()

st.set_page_config(layout="wide")
st.title("Playlist creator")
st.text('Here you can get the data from any playlist on spotify, you can also update already downloaded playlists.')
    
# Set your Spotify API credentials
CLIENT_ID = "d125d6339f6d4a7da8b304c605bf20b6"
CLIENT_SECRET = "0258ebafe0b2402ea990eade3499e7cf"

# Get url
playlist_id = st.text_input('playlist_id', value="6cR4y6y6ExPNk93BodOG56")
playlist_name = st.text_input('playlist_name', value="techno_flow_state" )
df = st.session_state.get('df')

if(st.button('Create or update playlist')):
    # # Authenticate with Spotify API
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri="http://localhost:8888/callback",  # Redirect URI set in the Spotify Developer Dashboard
        scope="playlist-read-private playlist-read-collaborative"
    ))

    path = f'data/{playlist_name}-{playlist_id}.csv'
    if(os.path.exists(path)):
        st.text('Updating playlist data...')
        shutil.copy(path, f'data/backups/{playlist_name}-{playlist_id}-{datetime.now().strftime("%m-%d_%H-%M-%S")}.csv')
        df = pd.read_csv(path, sep=';')
        updated_df = get_playlist_data(sp, playlist_id)
        df.drop(columns=['genres', 'name', 'artist', 'album'], errors='ignore', inplace=True)
        df = pd.merge(df, updated_df, on=['release_date', 'duration_ms', 'popularity'], how='left')
    else:
        st.text('Creating new playlist...')
        df = get_playlist_data(sp, playlist_id)
    st.session_state.df = df


if(st.session_state.get('df') is not None):
    if(len(df)>0):
            
        # Cleans data
        df['YouTube_Title'] = [None for i in range(len(df))]
        df['YouTube_URL'] = [None for i in range(len(df))]
        df['downloaded'] = [False for i in range(len(df))]
        st.text('Cleaning data...')
        if('genres' in df.columns):
            df['genres'] = df['genres'].apply(clean_genres)
            df['genres'] = df['genres'].apply(clean_data)
        columns = ['artist', 'name', 'album']
        for col in columns:
            df[col] = df[col].apply(clean_data)
            
        st.session_state.df = df
        st.dataframe(st.session_state.df)
        path = f'data/{playlist_name}-{playlist_id}.csv'
        if(st.button('Save playlist')):
            df.to_csv(path, sep=';', index=False)
    else:
        st.text('NO DATA FOUND')


