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
import data
from collections import Counter
import plotly.express as px


def flatten_genres(df):
    all_lists = df['genres']
    genres = []

    for genre_list in all_lists:
        if(type(genre_list)==float):
            pass
        else:
            print(genre_list, end='')
            genre_list = genre_list.replace("'","").replace("[","").replace("]","")
            if(',' in genre_list):
                aux = genre_list.split(',')
            else:   
                aux = genre_list.split(' - ')
            for g in aux:
                genres.append(g)
            print('->', aux)
    return genres

def flatten_artists(df):
    all_lists = df['artist']
    artists = []

    for genre_list in all_lists:
        if(type(genre_list)==float):
            pass
        else:
            print(genre_list, end='')
            genre_list = genre_list.replace("'","").replace("[","").replace("]","")
            if(',' in genre_list):
                aux = genre_list.split(',')
            else:   
                aux = genre_list.split(' - ')
            for g in aux:
                artists.append(g)
            print('->', aux)
    return artists


def plot_genre_histogram(df):
    genre_counts = Counter(flatten_genres(df))

    # Create the DataFrame for plotting
    genre_df = pd.DataFrame(genre_counts.items(), columns=['Genre', 'Count'])
    # Sort genres by frequency
    genre_df = genre_df.sort_values(by='Count', ascending=False)
    # Create the Plotly horizontal bar chart
    fig = px.bar(
        genre_df,
        x='Count',
        y='Genre',
        orientation='h',
        title='Genre Distribution in Playlist',
        labels={'Count': 'Frequency', 'Genre': 'Genres'},
        text='Count'
    )
    fig.update_traces(marker_color='skyblue', textposition='outside')
    fig.update_layout(
        yaxis=dict(autorange="reversed"),  # Reverse the y-axis to match your Matplotlib style
        height=1000,  # Adjust height for better readability
        margin=dict(l=150, r=50, t=50, b=50)  # Add padding for better visibility
    )
    return fig

def plot_popularity_histogram(df):
    # Create a histogram for the 'popularity' column
    fig = px.histogram(
        df,
        x='popularity',
        nbins=20,  # Adjust the number of bins as needed
        title='Distribution of Song Popularity',
        labels={'popularity': 'Popularity'},
        color_discrete_sequence=['lightgreen']  # Customize color
    )
    fig.update_layout(
        xaxis_title='Popularity Score',
        yaxis_title='Number of Songs',
        xaxis_range=[0, 100],  # Set x-axis range to 0-100
        margin=dict(l=50, r=50, t=50, b=50)
    )
    median_popularity = df['popularity'].median()
    fig.add_vline(
        x=median_popularity,
        line_dash="dash",  # Dashed line for the median
        line_color="red",
        annotation_text=f"Median: {median_popularity:.1f}",  # Display the median value
        annotation_position="top right"
    )
    return fig

def plot_duration_histogram(df):
    # Create a histogram for the 'popularity' column
    fig = px.histogram(
        df,
        x='duration_mins',
        nbins=20,  # Adjust the number of bins as needed
        title='Distribution of Song Duration in minutes',
        labels={'duration': 'Duration'},
        color_discrete_sequence=['skyblue']  # Customize color
    )
    fig.update_layout(
        xaxis_title='Duration in minutes',
        yaxis_title='Number of Songs',
        margin=dict(l=50, r=50, t=50, b=50)
    )
    median_popularity = df['duration_mins'].median()
    fig.add_vline(
        x=median_popularity,
        line_dash="dash",  # Dashed line for the median
        line_color="red",
        annotation_text=f"Median: {median_popularity:.1f}",  # Display the median value
        annotation_position="top right"
    )
    return fig

def plot_release_year_histogram(df):
    # Extract the release year
    df['release_year'] = pd.to_datetime(df['release_date'], format='mixed', errors='coerce').dt.year

    # Create the histogram
    fig = px.histogram(
        df,
        x='release_year',
        nbins=40,  # Adjust the number of bins as needed
        title='Distribution of Song Release Years',
        labels={'release_year': 'Release Year'},
        color_discrete_sequence=['lightgreen']
    )

    # Update layout with titles and margins
    fig.update_layout(
        xaxis_title='Release Year',
        yaxis_title='Number of Songs',
        margin=dict(l=50, r=50, t=50, b=50)
    )

    return fig

###################################################################################################################################################################
###################################################################################################################################################################
###################################################################################################################################################################

ALL = 'All of them'

playlist_name = st.selectbox('Select a playlist', [ALL]+[file for file in os.listdir('data/') if file.endswith('.csv')])
df = st.session_state.get('df')
if(st.button('Load data')):
    if(playlist_name == ALL):
        paths = [f'data/{file}' for file in os.listdir('data/') if file.endswith('.csv')]
        dfs = []#[pd.read_csv(path, sep=';') for path in paths]
        print(paths)
        for path in paths:
            print(path)
            dfs.append(data.read_as_df(path))
        df = pd.concat(dfs, axis=0)
        st.session_state.df = df
    else:
        path = f'data/{playlist_name}'
        df = data.read_as_df(path)
        st.session_state.df = df
    
    df['duration_mins'] = df['duration_ms'].apply(lambda x: round(x/1000/60,4))
    print('Data loaded')


if(df is not None):
    n = len(df)
    genres = np.unique(np.array(flatten_genres(df)))
    artists = np.unique(np.array(flatten_artists(df)))
    st.text(f'{n} songs in your playlists. With {len(artists)} artists and {len(genres)} genres')
    
    
    # GRAPHS
    
    # st.plotly_chart(plot_top_artist_histogram(df))
    # st.text('')
    # st.text('')

    # st.plotly_chart(plot_top_genre_histogram(df))
    # st.text('')
    # st.text('')

    st.plotly_chart(plot_popularity_histogram(df))
    st.text('')
    st.text('')

    st.plotly_chart(plot_duration_histogram(df))
    st.text(f'Total time of {round(np.sum(df["duration_mins"])/60,2)} hours')
    st.text('')
    st.text('')

    st.plotly_chart(plot_release_year_histogram(df))
    st.text('')
    st.text('')




