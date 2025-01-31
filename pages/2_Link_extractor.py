import data
import subprocess
import streamlit as st

if(__name__=='__main__'):
    st.set_page_config(layout="wide")
    st.title("Link extractor")
    st.text('Here you can get the links to the songs on your playlists.')
    st.text('This uses a scraper to search on Youtube, originally it used the Google API but it was very limited so that option has been removed.')

    # https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas?inv=1&invt=AblV9w&project=youtube-music-search-446115&pageState=(%22allQuotasTable%22:(%22s%22:%5B(%22i%22:%22currentPercent%22,%22s%22:%221%22),(%22i%22:%22sevenDayPeakPercent%22,%22s%22:%220%22),(%22i%22:%22currentUsage%22,%22s%22:%221%22),(%22i%22:%22sevenDayPeakUsage%22,%22s%22:%220%22),(%22i%22:%22serviceTitle%22,%22s%22:%220%22),(%22i%22:%22displayName%22,%22s%22:%220%22),(%22i%22:%22displayDimensions%22,%22s%22:%220%22)%5D,%22f%22:%22%255B%255D%22))
    api_key = 'AIzaSyCUc2-Xr3_OLVSt6Cga60hBmGS4N-hp6Ak'
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

    if(st.button('Get links')):
        path = f'data/{filename}'
        with st.spinner("Launching scraper..."):
            subprocess.Popen(
                ["python", "scripts/youtube_scraper.py", "--path", path],
                stdout=None, # Does not redirect outputs
                stderr=None,
                start_new_session=True  # Ensure it runs independently
            )
        st.success(f"Scraper finished for {filename}!")
        st.text('Check the results as errors are not caught here.')
            
