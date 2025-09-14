# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import os


class Config:
    SPOTIFY_CLIENT_ID: str = str(os.getenv(key="SPOTIPY_CLIENT_ID"))
    SPOTIFY_CLIENT_SECRET: str = str(os.getenv(key="SPOTIPY_CLIENT_SECRET"))


config = Config()
