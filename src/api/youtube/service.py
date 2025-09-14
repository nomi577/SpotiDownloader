# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


from api.youtube.types import YTVideoUrl
from googleapiclient.discovery import build  # type: ignore[import-untyped]
from config import config


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
