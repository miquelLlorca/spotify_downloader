import data
import subprocess
import streamlit as st

Y2MATE = 'y2mate'
NOTUBE = 'notube'

if(__name__=='__main__'):
    st.set_page_config(layout="wide")
    st.title("Song downloader")
    st.text('Here you can download the songs using the links previously extracted.')
    st.text('There are 2 options, the recommended one is y2mate, notube is not working for now as it has captcha verifitcation.')

    playlist_name = st.selectbox('Select a playlist', data.get_all_playlist_paths())
    webpage = st.selectbox('Choose an option:', [Y2MATE, NOTUBE], index=0)

    if(st.button('Start downloading')):
        path = f'data/{playlist_name}'
        with st.spinner("Launching scraper..."):
            subprocess.Popen(
                ["python", "scripts/downloader.py", "--path", path, '--webpage', webpage],
                    stdout=None, # Does not redirect outputs
                    stderr=None,
                    start_new_session=True  # Ensure it runs independently
            )
        st.success(f"Scraper finished for {playlist_name}!")
        st.text('Check the results as errors are not caught here.')