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

Y2MATE = 'y2mate'
NOTUBE = 'notube'

st.set_page_config(layout="wide")
st.title("Song downloader")
st.text('Here you can download the songs using the links previously extracted.')


# Get url
playlist_name = st.selectbox('Select a playlist', [file for file in os.listdir('data/') if file.endswith('.csv')])
webpage = st.selectbox('Choose an option:', [Y2MATE, NOTUBE], index=0)


if(st.button('Start downloading')):
    path = f'data/{playlist_name}'
    with st.spinner("Launching scraper..."):
        # Pass arguments to the scraper
        subprocess.Popen(
            ["python", "scripts/downloader.py", "--path", path, '--webpage', webpage],
            stdout=None,  # Suppress output if not needed
            stderr=None,
            start_new_session=True  # Ensure it runs independently
        )
    st.success(f"Scraper finished for {playlist_name}!")
    st.text('Check the results as errors are not caught here.')