import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import logging
logging.basicConfig(level=logging.DEBUG)


CLIENT_ID = "d125d6339f6d4a7da8b304c605bf20b6"
CLIENT_SECRET = "0258ebafe0b2402ea990eade3499e7cf"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri="http://localhost:8888/callback",  # Redirect URI set in the Spotify Developer Dashboard
    scope="playlist-read-private playlist-read-collaborative user-library-read"
))
sp.trace = True


playlists = sp.current_user_playlists()
for playlist in playlists['items']:
    print(f"Name: {playlist['name']}, ID: {playlist['id']}")


print()
print()
print()

def search_top_songs_playlists(sp, year):
    search_query = f"Your Top Songs {year}"
    results = sp.search(q=search_query, type='playlist', limit=5)
    for playlist in results['playlists']['items']:
        print(playlist)
        #print(f"Name: {playlist['name']}, ID: {playlist['id']}")

search_top_songs_playlists(sp, 2024)



# playlist_info = sp.playlist('37i9dQZF1FoyQGyinuuvRu')
# print(f"Playlist Name: {playlist_info['name']}")
