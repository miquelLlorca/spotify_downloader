


from yt_dlp import YoutubeDL

urls = [
    'https://www.youtube.com/watch?v=Q5TdYpS45eo&pp=ygUSZGVwYXJ0YW1lbnRvIGNvc2Fz'
]

series_name = 'departamento_cosas'

options = {
    "format": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]",
    "merge_output_format": "mp4",
    "outtmpl": f"/home/miquel/Downloads/{series_name}/%(title)s.%(ext)s",
    "cookiefile": "/home/miquel/Downloads/cookies.txt"
}



with YoutubeDL(options) as ydl:
    ydl.download(urls)