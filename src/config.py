# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import os


class Config:
    # Spotify
    SPOTIFY_CLIENT_ID: str = str(os.getenv(key="SPOTIPY_CLIENT_ID"))
    SPOTIFY_CLIENT_SECRET: str = str(os.getenv(key="SPOTIPY_CLIENT_SECRET"))
    SPOTIFY_DEFAULT_ARTIST: dict[str, str] = {"name": "<No Artist>"}
    SPOTIFY_DEFAULT_TRACK_NAME: str = "<UNKNOWN_TRACK>"
    SPOTIFY_DEFAULT_PLAYLIST_NAME: str = "<UNKNOWN_PLAYLIST>"
    SPOTIFY_DEFAULT_PLAYLIST_DESCRIPTION: str = ""
    SPOTIFY_MAX_TRACKS: int = 1000
    SPOTIFY_API_DELAY: float = 0.3
    SPOTIFY_BATCH_SIZE_TRACKS: int = 25

    # Youtube
    YOUTUBE_DATA_API_V3_API_KEY: str = str(os.getenv("YOUTUBE_DATA_API_V3_API_KEY"))


config = Config()
