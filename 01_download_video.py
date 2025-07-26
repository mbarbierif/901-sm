import sys
import yt_dlp
from pathlib import Path

Path("downloads").mkdir(exist_ok=True)

yt_dlp.YoutubeDL({"outtmpl": "downloads/%(id)s"}).download([sys.argv[1]])

"""
Ejemplos:
uv run python 01_download_video.py "https://www.youtube.com/watch?v=KTDen9ooazo"
uv run python 01_download_video.py "https://www.youtube.com/watch?v=p_sOLAtXY44"
uv run python 01_download_video.py "https://www.youtube.com/watch?v=1gi5qn1khVk"
uv run python 01_download_video.py "https://www.youtube.com/watch?v=ms-Q3t5IqNM"
uv run python 01_download_video.py "https://www.youtube.com/watch?v=V3QMrftx3cQ"
"""