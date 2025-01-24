import streamlit as st
import os
import pandas as pd


def find_playlists():
    return 


def main():
    st.set_page_config(layout="wide")

    st.title("Spotify downloader")
    st.text("Here you can check the state of your playlists, for more actions check the other pages")
    playlist_name = st.selectbox('Select a playlist', [file for file in os.listdir('data/') if file.endswith('.csv')])
    
    if(st.button('Load dataset')):
        st.session_state.df = pd.read_csv(f'data/{playlist_name}', sep=';')
        
    if(st.session_state.get('df') is not None):
        st.dataframe(st.session_state.df)
        
if(__name__=="__main__"):
    main()