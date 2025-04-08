


from yt_dlp import YoutubeDL

urls = [
    'https://youtu.be/playlist?list=PLkPM73HZcYt03hiFlsLGZdIJdF9pYLFU3'
]


series_name = 'DHMIS'
options = {
    "format": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]",
    "merge_output_format": "mp4",
    "outtmpl": f"/home/miquel/Downloads/{series_name}/%(title)s.%(ext)s",
    "cookiefile": "/home/miquel/Downloads/cookies.txt"
}



with YoutubeDL(options) as ydl:
    ydl.download(urls)