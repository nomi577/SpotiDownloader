# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import os
import yt_dlp  # type: ignore[import-untyped]

from api.youtube.types import YTVideoUrl
from googleapiclient.discovery import build  # type: ignore[import-untyped]
from config import config
from typing import Any
from utils.sanitization import sanitize


class YTService:
    def __init__(self) -> None:
        self.__youtube = build(  # type: ignore[reportUnknownMemberType]
            "youtube",
            "v3",
            developerKey=config.YOUTUBE_DATA_API_V3_API_KEY,
        )

    def search_video(self, query: str) -> YTVideoUrl:
        request = self.__youtube.search().list(  # type: ignore[reportUnknownMemberType]
            part="snippet",
            q=query,
            type="video",
        )
        response = request.execute()  # type: ignore[reportUnknownMemberType]

        if not response.get("items"):  # type: ignore[reportUnknownMemberType]
            raise ValueError(f"No videos found using query '{query}'!")

        video_id = response.get("items", [])[0]["id"]["videoId"]  # type: ignore[reportUnknownMemberType]

        return YTVideoUrl(f"https://www.youtube.com/watch?v={video_id}")

    def download_audio(
        self,
        url: YTVideoUrl,
        file_path: str,
    ) -> None:
        os.makedirs(sanitize(os.path.dirname(file_path), allowed=r"\w/"), exist_ok=True)

        ydl_options: dict[str, Any] = {
            # pick best available audio only
            "format": "bestaudio/best",
            "outtmpl": file_path,
            "quiet": True,
            "noplaylist": True,
            "restrictfilenames": True,
            "postprocessors": [
                {  # extract audio and convert to mp3
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                },
                {  # embed thumbnail if available
                    "key": "EmbedThumbnail",
                },
                {  # add metadata
                    "key": "FFmpegMetadata",
                },
            ],
        }

        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            ydl.download([str(url)])  # type: ignore[reportUnknownMemberType]
