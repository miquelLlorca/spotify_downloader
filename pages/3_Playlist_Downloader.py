import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import data
import streamlit as st
import plots
import yt_dlp
import zipfile
import io

downloaded_songs = []
def progress_hook(d):
    if d["status"] == "finished":
        url = d["info_dict"]["original_url"]
        downloaded_songs.append(url)  # Store for later



if(__name__=='__main__'):
    st.set_page_config(layout="wide")

    st.title("Playlist downloader")
    st.text('Here you can download the songs using the links previously extracted.')
    st.text('First, you need to download the songs to the server, then you will be able to donwload the whole playlist as a zip to your PC.')

    playlist_name = st.selectbox('Select a playlist', data.get_all_playlist_paths())
    path = f'data/{playlist_name}'
    st.plotly_chart(plots.plot_song_state_pie(data.read_as_df(path)))
    
    if(st.button('Start downloading')):
        folder_path = f'/home/miquel/Descargas/{os.path.basename(path).split(".")[0]}'
        options = {
            "noplaylist": True,
            "outtmpl": f"{folder_path}/%(title)s.%(ext)s",
            "progress_hooks": [progress_hook],
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "256",  # You can change the bitrate
                }
            ],
        }

        with st.spinner("Launching scraper..."):            
            df = data.read_as_df(path)

            if('downloaded' not in df.columns):
                df['downloaded'] = [False for i in range(len(df))]
                
            try:
                urls = df[~ df["downloaded"]]["YouTube_URL"].values
                with yt_dlp.YoutubeDL(options) as ydl:
                    ydl.download(urls)
            except Exception as e:
                st.text(f'{e.__class__.__name__} -> {e}')
            finally:
                df.loc[df["YouTube_URL"].isin(downloaded_songs), "downloaded"] = True
                data.save_df(df, path)

            st.success(f"Downloader finished for {playlist_name}!")
        st.text('Go to the next section to download the playlist to your PC!')

    st.title('Download your playlist!')
    st.text('Once you have the full playlist converted you can download it to your computer.')
    try:
        files_to_zip = [os.path.join(folder_path, song) for song in os.path.listdir(folder_path)]

        # Create zip in-memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for file_path in files_to_zip:
                zip_file.write(file_path, os.path.basename(file_path))
        zip_buffer.seek(0)

        # Download button
        st.download_button(
            label="Download ZIP",
            data=zip_buffer,
            file_name="downloaded_video.zip",
            mime="application/zip",
        )
    except:
        st.text('Not available yet.')