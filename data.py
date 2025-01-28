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
from datetime import datetime, timedelta
import unicodedata
import re

# Here are all the functions related to Data treatment


def save_df(df:pd.DataFrame, path):
    df.to_csv(path, index=False, sep=';', encoding='utf-8')
def read_as_df(path):
    return pd.read_csv(path, sep=';', encoding='utf-8')


def create_backup(path, playlist_name, playlist_id):
    shutil.copy(path, f'data/backups/{playlist_name}-{playlist_id}-{datetime.now().strftime("%m-%d_%H-%M-%S")}.csv')

def check_too_old(path):
    ''' Used for checking if the spotify raw data should be updated, so useless API calls can be avoided. '''
    file_stats = os.stat(path)
    last_modified = datetime.fromtimestamp(file_stats.st_mtime)
    return (datetime.now() - last_modified) >= timedelta(days=1)

def correct_date_format(date):
    ''' Corrects dates that only contain the year as these tend to break things. 
        Real date is not really important so it only adds 1st of january to the year.'''
    if(type(date) != str):
        date = str(date)
    if(len(date) == 4):  # If the date is only the year (e.g., '2022')
        return date + '-01-01'  # Add '-01-01' to make it a full date
    return date  # Otherwise, return the original date

def clean_data(data):
    ''' Cleans strings to prepare them for the csv'''
    if(type(data)!=str):
        data = str(data)
    # Only cleaning needed is taking out ; so it does not cause problems with the csv
    # It's important to keep any other chars, as there are songs in other languages
    return data.replace(';','').strip()