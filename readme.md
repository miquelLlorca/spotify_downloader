# SPOTIFY DOWNLOADER
This project aims to make music more accesible. In recent years subscription models have been on the rise, we have gotten to a point where **buying isn't owning, so piracy isn't stealing**.

## Running the website
Recommended python version is 3.11 or greater, in the file _requirements.txt_ the dependencies of the project are listed so anyone can easily setup their enviroment. 

The website can be run using the **_launch_** scripts, ._sh_for linux and _.bat_ for windows. Once its running it can be accesed with the link shown in the terminal.

### Spotify API
You will need to get your own API credentials to get your playlists, this is easily done through _https://developer.spotify.com/dashboard_
1. Click on 'Create an App', set name and description as you wish.
2. Set Redirect URL as _http://localhost:8888/callback_
3. Click on 'Create'
4. Click on 'Settings' and get your credentials
5. Copy them to the file _credentials.json_