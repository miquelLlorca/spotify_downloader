import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import os
import streamlit as st
import shutil
from datetime import datetime
import data


def get_playlist_data(sp, playlist_id, filename):
    ''' Uses the spotify API to get all data from a playlist.
        If the data is already available locally it skips the call.'''
    
    raw_data_path = f'data/spotify_raw/{filename}'
    if(os.path.exists(raw_data_path) and not data.check_too_old(raw_data_path)):
        st.text('Data already downloaded, skipping API call...')
        return data.read_as_df(raw_data_path)
    
    # if the file does not exist or is older it gets the data again
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
                if(track):  # Check if track is not None
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

    df = pd.DataFrame(all_tracks)
    data.save_df(df, raw_data_path)
    return df



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

    filename = f'{playlist_name}-{playlist_id}.csv'
    path = f'data/{filename}'
    if(os.path.exists(path)):
        st.text('Updating playlist data...')
        data.create_backup(path, playlist_name, playlist_id)
        df = data.read_as_df(path)
        updated_df = get_playlist_data(sp, playlist_id, filename)

        df.drop(columns=['genres', 'name', 'artist', 'album'], errors='ignore', inplace=True)
        updated_df['popularity'] = updated_df['popularity'].astype(float)
        
        df['release_date'] = df['release_date'].apply(data.correct_date_format)
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
        updated_df['release_date'] = updated_df['release_date'].apply(data.correct_date_format)
        updated_df['release_date'] = pd.to_datetime(updated_df['release_date'], errors='coerce')

        df = pd.merge(updated_df, df, on=['release_date', 'duration_ms', 'popularity'], how='left')
    else:
        st.text('Creating new playlist...')
        df = get_playlist_data(sp, playlist_id, filename)
        df['release_date'] = df['release_date'].apply(data.correct_date_format)
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    st.session_state.df = df


if(st.session_state.get('df') is not None):
    if(len(df)>0):
        # If columns already exist they should be kept
        if('YouTube_Title' not in df.columns):
            df['YouTube_Title'] = [None for i in range(len(df))]
        if('YouTube_URL' not in df.columns):
            df['YouTube_URL'] = [None for i in range(len(df))]
        if('downloaded' not in df.columns):
            df['downloaded'] = [False for i in range(len(df))]

        # Cleans the data
        st.text('Cleaning data...')
        columns_to_clean = ['artist', 'name', 'album', 'genres']
        for col in columns_to_clean:
            df[col] = df[col].apply(data.clean_data)
            
        st.session_state.df = df
        st.dataframe(st.session_state.df)
        path = f'data/{playlist_name}-{playlist_id}.csv'
        if(st.button('Save playlist')):
            data.save_df(df, path)
    else:
        st.text('NO DATA FOUND')


