import os
import data
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from collections import Counter
import plotly.graph_objects as go
from plots import *


###################################################################################################################################################################
###################################################################################################################################################################
###################################################################################################################################################################

if(__name__=='__main__'):
    ALL = 'All of them'
    st.set_page_config(layout="wide")
    playlist_name = st.selectbox('Select a playlist', [ALL]+data.get_all_playlist_paths())
    df = st.session_state.get('df')

    if(st.button('Load data')):
        if(playlist_name == ALL):
            paths = [f'data/{file}' for file in os.listdir('data/') if file.endswith('.csv')]
            dfs = []
        
            for path in paths:
                df = data.read_as_df(path)
                df['playlist'] = os.path.basename(path).split('-')[0]
                dfs.append(df)

            df = pd.concat(dfs, axis=0)
            st.session_state.df = df
        else:
            path = f'data/{playlist_name}'
            df = data.read_as_df(path)
            st.session_state.df = df
        
        df['duration_mins'] = df['duration_ms'].apply(lambda x: round(x/1000/60,4))
        df['downloaded'] = df['downloaded'].apply(lambda x: x if type(x)==bool else False)
        df['release_year'] = pd.to_datetime(df['release_date'], format='mixed', errors='coerce').dt.year
        print('Data loaded')


    if(df is not None):
        n = len(df)
        genres = np.unique(np.array(data.flatten_genres(df)))
        artists = np.unique(np.array(data.flatten_artists(df)))
        st.text(f'{n} songs in your playlists. With {len(artists)} artists and {len(genres)} genres')
        
        
        # GRAPHS
        st.title('ARTISTS')
        with(st.expander('Click to show/hide')):
            st.text(f'There are {len(artists)} different artists in your playlists.')
            top_n_artists = int(st.text_input('Show top N artists', value=10))
            st.plotly_chart(plot_top_artists_histogram(df, top_n_artists))

        st.title('GENRES')
        with(st.expander('Click to show/hide')):
            st.text(f'There are {len(genres)} different subgenres in your playlists.')
            top_n_genres = int(st.text_input('Show top N genres', value=10))
            st.plotly_chart(plot_top_genres_histogram(df, top_n_genres))

        st.title('POPULARITY')
        with(st.expander('Click to show/hide')):
            st.plotly_chart(plot_popularity_histogram(df))

        st.title('DURATION')
        with(st.expander('Click to show/hide')):
            st.text(f'You have a total time of {round(np.sum(df["duration_mins"])/60,2)} hours of music!')
            st.plotly_chart(plot_duration_histogram(df))

        st.title('RELEASE DATE')
        with(st.expander('Click to show/hide')):
            st.plotly_chart(plot_release_year_histogram(df))
            st.plotly_chart(plot_mean_release_year(df))
            

        st.title('SONG STATE')
        with(st.expander('Click to show/hide')):
            st.plotly_chart(plot_song_state_pie(df))
            if(playlist_name==ALL):
                n_cols = 4
                columns = st.columns(n_cols)
                for i, playlist in enumerate(df['playlist'].unique()):
                    columns[i%n_cols].plotly_chart(plot_song_state_pie(df[df['playlist']==playlist], playlist))  
