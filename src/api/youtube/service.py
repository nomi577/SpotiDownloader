# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import os
import yt_dlp  # type: ignore[import-untyped]

from api.youtube.types import YTVideoUrl
from typing import Any
from utils.sanitization import sanitize


class YTService:
    def search_video(self, query: str) -> YTVideoUrl:
        ydl_opts: dict[str, Any] = {
            "quiet": True,
            "noplaylist": True,
            "extract_flat": "in_playlist",  # only metadata, no download
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info: dict[str, Any] = ydl.extract_info(f"ytsearch:{query}", download=False)  # type: ignore[reportUnknownMemberType]
            if not info["entries"]:
                raise ValueError(f"No results for query '{query}'")
            video_id: str = info["entries"][0]["id"]
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
