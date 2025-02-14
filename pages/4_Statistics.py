import os
import data
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from collections import Counter
import plotly.graph_objects as go


def plot_top_genres_histogram(df, top_n):
    ''' Plots the top N genres in the playlists loaded. '''
    genre_counts = Counter(data.flatten_genres(df))
    genre_df = pd.DataFrame(genre_counts.items(), columns=['Genre', 'Count'])
    genre_df = genre_df.sort_values(by='Count', ascending=False)
    if(top_n>len(genre_df)):
        top_n = len(genre_df)

    fig = px.bar(
        genre_df.head(top_n),
        x='Count',
        y='Genre',
        orientation='h',
        title='Genre Distribution in Playlist',
        labels={'Count': 'Frequency', 'Genre': 'Genres'},
        text='Count'
    )
    fig.update_traces(marker_color='skyblue', textposition='outside')
    fig.update_layout(
        height=1000,
        margin=dict(l=150, r=50, t=50, b=50),
        yaxis=dict(
            autorange="reversed", 
        )
    )
    fig.update_layout(
        dragmode="pan",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
    )
    return fig

def plot_top_artists_histogram(df, top_n):
    ''' Plots the top N artists in the playlists loaded. '''
    artist_counts = Counter(data.flatten_artists(df))
    artist_df = pd.DataFrame(artist_counts.items(), columns=['Artist', 'Count'])
    artist_df = artist_df.sort_values(by='Count', ascending=False)
    if(top_n>len(artist_df)):
        top_n = len(artist_df)

    fig = px.bar(
        artist_df.head(top_n),
        x='Count',
        y='Artist',
        orientation='h',
        title='Artist Distribution in Playlist',
        labels={'Count': 'Frequency', 'artist': 'artists'},
        text='Count'
    )
    fig.update_traces(marker_color='skyblue', textposition='outside')
    fig.update_layout(
        height=1000,
        margin=dict(l=150, r=50, t=50, b=50),
        yaxis=dict(
            autorange="reversed", 
        )
    )
    fig.update_layout(
        dragmode="pan",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
    )
    return fig

def plot_popularity_histogram(df):
    ''' Plots the popularity of songs in the playlists loaded. '''
    fig = px.histogram(
        df,
        x='popularity',
        nbins=20,
        title='Distribution of Song Popularity',
        labels={'popularity': 'Popularity'},
        color_discrete_sequence=['lightgreen']
    )
    fig.update_layout(
        xaxis_title='Popularity Score',
        yaxis_title='Number of Songs',
        xaxis_range=[0, 100],
        margin=dict(l=50, r=50, t=50, b=50)
    )
    median_popularity = df['popularity'].median()
    fig.add_vline(
        x=median_popularity,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Median: {median_popularity:.1f}",
        annotation_position="top right"
    )
    return fig

def plot_duration_histogram(df):
    ''' Plots the duration by song in the playlists loaded. '''
    fig = px.histogram(
        df,
        x='duration_mins',
        nbins=20,
        title='Distribution of Song Duration in minutes',
        labels={'duration': 'Duration'},
        color_discrete_sequence=['skyblue']
    )
    fig.update_layout(
        xaxis_title='Duration in minutes',
        yaxis_title='Number of Songs',
        margin=dict(l=50, r=50, t=50, b=50)
    )
    median_popularity = df['duration_mins'].median()
    fig.add_vline(
        x=median_popularity,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Median: {median_popularity:.1f}",
        annotation_position="top right"
    )
    return fig

def plot_release_year_histogram(df):
    ''' Plots the number of songs released by year in the playlists loaded. '''
    fig = px.histogram(
        df,
        x='release_year',
        nbins=40,
        title='Distribution of Song Release Years',
        labels={'release_year': 'Release Year'},
        color_discrete_sequence=['lightgreen']
    )
    fig.update_layout(
        xaxis_title='Release Year',
        yaxis_title='Number of Songs',
        margin=dict(l=50, r=50, t=50, b=50)
    )
    return fig

def plot_mean_release_year(df):
    # Calculate mean release year for each playlist
    mean_years = df.groupby("playlist")["release_year"].mean().reset_index()
    mean_years["release_year"] = mean_years["release_year"].astype(float)  
    mean_years = mean_years.sort_values(by="release_year").reset_index(drop=True)

    # Create figure
    fig = go.Figure()
    colors = px.colors.qualitative.Plotly  # Can use other color scales like 'Set1', 'Dark24', etc.
    # Add vertical lines and annotations for each playlist
    for i, row in mean_years.iterrows():
        y_position = 0.02+(i * (1/len(mean_years)))  # Moves text higher for each playlist
        fig.add_trace(go.Scatter(
            x=[row["release_year"], row["release_year"]],
            y=[0, 1],  # Fixed y-range for vertical lines
            mode="lines",
            line=dict(color=colors[i % len(colors)], width=3),
            hoverinfo="x+text",
            name=row["playlist"]
        ))

        # Add a separate text label to move it higher
        fig.add_trace(go.Scatter(
            x=[row["release_year"]],
            y=[y_position],  # Move text label higher
            mode="text",
            text=[row["playlist"]],
            textfont=dict(size=16, color=colors[i % len(colors)]),
            showlegend=False
        ))

    # Update layout
    fig.update_layout(
        title="Mean Release Year by Playlist",
        xaxis_title="Release Year",
        yaxis=dict(showticklabels=False),  # Hide y-axis labels
        showlegend=True,
        height=600
    )


    return fig

def plot_song_state_pie(df, playlist=''):
    state_count = pd.DataFrame({
        'State': ['Without link', 'With link but not downloaded', 'Downloaded'],
        'Count': [
            len(df[df['YouTube_URL'].isna()]),
            len(df[~df['YouTube_URL'].isna() & ~df['downloaded']]),
            len(df[df['downloaded']]),
        ]
    })

    # Define a fixed color mapping for consistency
    color_map = {
        'Without link': 'rgb(227, 79, 39)',  # Soft red
        'With link but not downloaded': 'rgb(252, 186, 3)',  # Muted orange
        'Downloaded': 'rgb(86, 204, 82)'  # Soft green
    }

    title = 'Song State Distribution' if playlist=='' else f'Distribution for {playlist}'
    return px.pie(
        state_count,
        names='State',
        values='Count',
        title=title,
        color='State',  # Use the 'State' column for color mapping
        color_discrete_map=color_map  # Apply fixed colors
    )



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
