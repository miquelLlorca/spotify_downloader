import streamlit as st

# Path to the MP3 file on your disk
file_path = "/home/miquel/Downloads/Niko\ B\ -\ Whys\ this\ dealer\ -\ Bouncing\ Yaris\ edition.mp3"
file_path = "/home/miquel/Downloads/Niko B - Whys this dealer - Bouncing Yaris edition.mp3"

st.title("My Personal Music Player")

# Read and play the MP3 file
with open(file_path, "rb") as audio_file:
    st.audio(audio_file.read(), format="audio/mp3")