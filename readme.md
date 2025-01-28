# SPOTIFY DOWNLOADER
This project aims to make music more accesible. In recent years subscription models have been on the rise, we have gotten to a point where **buying isn't owning, so piracy isn't stealing**. If you are like me you may be worried about a future where entertainment is increasingly more expensive or even inaccesible, so better start preparing as early as possible.

I used to manually download my music, but during the last years I have been using free spotify and I have many playlists with a ton of music, so i thought i should download it all, but i was not going to do that manually, of course. 

The downloading pipeline is not fully automatic, you will need to manually launch the following steps:
1. **Get playlist data** using the Spotify API.
2. **Search for the songs** on youtube to get their links.
3. **Download the songs**.
These will be describe more in detail in _pages/readme.md_ and inside the pages where you can launch each of the processes.

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

### ChromeDriver
The scrapers work using Google Chrome, so you will need to install it and ChromeDriver. You can follow any online tutorial on it (e.g: _https://skolo.online/documents/webscrapping/_), there shouldn't be any problem regarding versions as the scraping done uses basic functions.