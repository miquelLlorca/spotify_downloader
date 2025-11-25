import os
import data
import json
import spotipy
import pandas as pd
import streamlit as st
from spotipy.oauth2 import SpotifyOAuth

PLAYLIST = 'Personal playlist'
ALBUM = 'Album'
ARTIST = 'Artist'

def get_spotify_credentials():
    ''' Loads spotify credentials. Returns [id, secret]'''
    with open('credentials.json', 'r') as file:
        creds = json.loads(file.read())
    return creds['client_id'], creds['client_secret']


def get_playlist_data(sp, playlist_id, filename):
    ''' Uses the spotify API to get all data from a playlist.
        If the data is already available locally it skips the call.'''

    all_tracks = []
    offset = 0
    limit = 100
    raw_data_path = f'data/spotify_raw/{filename}'
    while True:
        try:
            response = sp.playlist_items(playlist_id, offset=offset, limit=limit)
            items = response['items']
            if not items:  # Stop if no more tracks
                break
            
            st.text(f'Gotten first {offset+len(items)} songs!')
            for item in items:
                track = item['track']
                if(track):
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
            st.text(f"Error: {e}")
            break

    df = pd.DataFrame(all_tracks)
    data.save_df(df, raw_data_path)
    return df

def get_album_data(sp, album_id, filename):
    ''' Uses the Spotify API to get all data from an album.
        If the data is already available locally, it skips the call.'''
   
    raw_data_path = f'data/spotify_raw/{filename}'
    try:
        album = sp.album(album_id)
        tracks = album['tracks']['items']
        all_tracks = []

        for track in tracks:
            artist_ids = [artist['id'] for artist in track['artists']]
            genres = []
            #! Removed genres due to spotify's API rate limit
            # for artist_id in artist_ids:
            #     artist_info = sp.artist(artist_id)
            #     genres.extend(artist_info.get('genres', []))

            track_info = {
                'name': track['name'],
                'artist': ', '.join(artist['name'] for artist in track['artists']),
                'album': album['name'],
                'release_date': album['release_date'],
                'duration_ms': track['duration_ms'],
                'popularity': track.get('popularity', None),
                'genres': list(set(genres))  # Remove duplicates
            }
            all_tracks.append(track_info)

        df = pd.DataFrame(all_tracks)
        if(df.empty):
            st.text('No data with this ID')
        else:
            data.save_df(df, raw_data_path)
        return df

    except Exception as e:
        st.text(f"Error: {e}")
        return None
    
def get_data(source, sp, playlist_id, filename):
     
    raw_data_path = f'data/spotify_raw/{filename}'
    if os.path.exists(raw_data_path) and not data.check_too_old(raw_data_path):
        st.text('Data already downloaded, skipping API call...')
        return data.read_as_df(raw_data_path)

    if(source==PLAYLIST):
        return get_playlist_data(sp, playlist_id, filename)
    elif(source==ALBUM):
        return get_album_data(sp, playlist_id, filename)




def get_artist_albums(sp, artist_id):
    albums = {}
    # Get albums, singles, and EPs
    for album_type in ['album', 'single', 'appears_on', 'compilation']:
        albums[album_type] = {}
        results = sp.artist_albums(artist_id, album_type=album_type)
        while results:
            for album in results['items']:
                albums[album_type][album['id']] = {
                    'name': album['name'],
                    'release_date': album['release_date'],
                    'total_tracks': album['total_tracks'],
                }
            results = sp.next(results) if results['next'] else None
    return albums
#####################################################################################################################################################
#####################################################################################################################################################
#####################################################################################################################################################

if(__name__=="__main__"):
    CLIENT_ID, CLIENT_SECRET = get_spotify_credentials()

    st.set_page_config(layout="wide")
    st.title("Playlist creator")
    st.text('Here you can get the data from any playlist on spotify, you can also update already downloaded playlists.')
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri="http://localhost:8888/callback",
        scope="playlist-read-private playlist-read-collaborative"
    ))

    source = st.selectbox(label='source', options=[PLAYLIST, ALBUM, ARTIST])
    spotify_id = st.text_input('playlist_id', value="6cR4y6y6ExPNk93BodOG56")
    playlist_name = st.text_input('playlist_name', value="techno_flow_state" )
    df = st.session_state.get('df')

    filename = f'{playlist_name}-{spotify_id}.csv'
    path = f'data/{filename}'
    
    if(source in [PLAYLIST, ALBUM]):
        if(st.button('Create or update playlist')):
            if(os.path.exists(path)):

                st.text('Updating playlist data...')
                data.create_playlist_backup(path)
                df = data.read_as_df(path)
                updated_df = get_data(source, sp, spotify_id, filename)

                # Prepares data for merge
                df.drop(columns=['genres', 'name', 'artist', 'album', 'popularity'], errors='ignore', inplace=True)
                updated_df['popularity'] = updated_df['popularity'].astype(float)
                df['release_date'] = df['release_date'].apply(data.correct_date_format)
                df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
                updated_df['release_date'] = updated_df['release_date'].apply(data.correct_date_format)
                updated_df['release_date'] = pd.to_datetime(updated_df['release_date'], errors='coerce')

                # Merges on left to make sure new data is added to df
                df = pd.merge(updated_df, df, on=['release_date', 'duration_ms'], how='left')
            else:
                st.text('Creating new playlist...')
                df = get_data(source, sp, spotify_id, filename)
                # Prepares data for possible future merge
                df['release_date'] = df['release_date'].apply(data.correct_date_format)
                df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
            st.session_state.df = df

    else: # ARTIST selected
        if(st.button('Get Albums')):
            st.session_state.albums = get_artist_albums(sp, spotify_id)

        if(st.session_state.get('albums')):
            selected_albums = {}
            
            for album_type, albums in st.session_state.albums.items():
                if(len(albums)>0):
                    st.text(album_type.upper())
                    for album_id, album_data in albums.items():
                        selected_albums[album_id] = st.checkbox(
                            f"{album_data['name']}  -   {album_data['total_tracks']} songs. {album_data['release_date']}", 
                            key=album_id
                        )

            if(any(selected_albums.values())):
                st.text('Selected')
                dfs = []
                albums = {}
                for album_list in st.session_state.albums.values():
                    albums = {**albums, **album_list}
                

                print(albums)
                for album_id, selected in selected_albums.items():
                    if selected:
                        filename = f'{albums[album_id]}-{album_id}.csv'
                        dfs.append(get_album_data(sp, album_id, filename))
                st.session_state.df = pd.concat(dfs, ignore_index=True)
            

    if(st.session_state.get('df') is not None):
        df = st.session_state.get('df')
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
            if(st.button('Save playlist')):
                data.save_df(df, path)
        else:
            st.text('NO DATA FOUND')


