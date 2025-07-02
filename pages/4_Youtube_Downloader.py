import data
import subprocess
import streamlit as st
import plots
from yt_dlp import YoutubeDL
import os

AUDIO = 'Audio'
VIDEO = 'Video'

if(__name__=='__main__'):
    st.set_page_config(layout="wide")
    st.title("Youtube video downloader")
    st.text('Here you can download single youtube videos using the URL directly.')
    st.text('Choose audio or video and leave the rest unchanged if you dont know what you are doing.')

    yt_dlt_options = {
        "cookiefile": "/home/miquel/Descargas/cookies.txt"
    }


    url = st.text_input(label = 'Input your URL:')
    download_type = st.selectbox(label='Select the format you want:', options=[AUDIO, VIDEO])



    if(download_type==VIDEO):
        video_quality = st.selectbox('Choose video quality:', ['2160', '1440', '1080', '720', '480', '360', '240'], index=2)
        folder_name = st.text_input(label='Input the folder to save it:', value='Youtube_Videos')

        yt_dlt_options['download_type'] = download_type.lower()
        yt_dlt_options['format'] = (
            f"bestvideo[height<={video_quality}][ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/"
            f"bestvideo[height<={video_quality}][vcodec^=avc1]+bestaudio/best[height<={video_quality}]"
        )
        # f"bestvideo[height<={video_quality}][ext=mp4]+bestaudio[ext=m4a]/best[height<={video_quality}][ext=mp4]"
        
        yt_dlt_options["merge_output_format"] = "mp4"

    elif(download_type==AUDIO):
        audio_quality = st.selectbox('Choose audio quality:',['320', '256', '192', '128'], index=1)
        folder_name = st.text_input(label='Input the folder to save it:', value='Youtube_Music')
        
        yt_dlt_options['download_type'] = download_type.lower()
        yt_dlt_options["format"] = "bestaudio"
        yt_dlt_options['postprocessors'] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": audio_quality,
            }
        ]

    yt_dlt_options['outtmpl'] = f"/home/miquel/Descargas/{folder_name}/%(title)s.%(ext)s"





    if(st.button('Start downloading')):

        with st.spinner("Converting video..."):

            with YoutubeDL(yt_dlt_options) as ydl:
                info = ydl.extract_info(url)
                file_path = str(ydl.prepare_filename(info))

        if(download_type==AUDIO):
            file_path = file_path.replace('webm', 'mp3')


        st.text('Video converted! Download it from below:')
        with open(file_path, "rb") as f:
            file_bytes = f.read()

        st.download_button(
            label=f"Download {download_type}: {os.path.basename(file_path).split('.')[0]}",
            data=file_bytes,
            file_name=os.path.basename(file_path), 
            mime='video/mp4' if download_type==VIDEO else 'audio/mp3'
        )