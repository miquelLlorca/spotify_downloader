import data
import pandas as pd
import plotly.express as px
from collections import Counter
import plotly.graph_objects as go
from plots import *


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

