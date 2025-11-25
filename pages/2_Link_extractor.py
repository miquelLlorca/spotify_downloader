import data
import subprocess
import streamlit as st
import plots

if(__name__=='__main__'):
    st.set_page_config(layout="wide")
    st.title("Link extractor")
    st.text('Here you can get the links to the songs on your playlists.')
    st.text('This uses a scraper to search on Youtube, originally it used the Google API but it was very limited so that option has been removed.')
    st.session_state.quota_exceeded = False

    # Get url
    filename = st.selectbox('Select a playlist', data.get_all_playlist_paths())

    st.markdown(
        """
        <div style="background-color: #ff9800; padding: 10px; border-radius: 5px; text-align: center;">
            <strong style="color: #cc0000;">WARNING:</strong> 
            <span style="color: #000; font-size: 16px;">You need to accept the cookies manually so the scraper can work freely.</span>
        </div>
        """, unsafe_allow_html=True
    )
    path = f'data/{filename}'
    st.plotly_chart(plots.plot_song_state_pie(data.read_as_df(path)))
    
    if(st.button('Get links')):
        with st.spinner("Launching scraper..."):
            subprocess.Popen(
                ["python", "scripts/youtube_scraper.py", "--path", path],
                stdout=None, # Does not redirect outputs
                stderr=None,
                start_new_session=True  # Ensure it runs independently
            )
        st.success(f"Scraper finished for {filename}!")
        st.text('Check the results as errors are not caught here.')
            
