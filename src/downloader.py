# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import os
import math

from api.spotify.service import SpotifyService
from api.youtube.service import YTService
from api.youtube.types import YTVideoUrl
from api.classes import Track, Playlist
from config import config
from typing import Optional
from api.spotify.types import PotUrl


class Downloader:
    def __init__(self, spotify_service: SpotifyService, yt_service: YTService) -> None:
        self.__spotify_service: SpotifyService = spotify_service
        self.__yt_service: YTService = yt_service

    def __download_track(self, track: Track, file_path: Optional[str] = None) -> None:
        print(f"Downloading track '{track.name}' by '{track.artist.name}'...")
        video_url: YTVideoUrl = self.__yt_service.search_video(
            query=config.YOUTUBE_QUERY_TEMPLATE.format(
                title=track.name,
                artist=track.artist.name,
            )
        )

        if file_path is None:
            file_path = os.path.join(
                config.YOUTUBE_DOWNLOAD_DIRECTORY,
                config.FILES_NAME_TEMPLATE_NO_IDX.format(
                    title=track.name,
                ),
            )

        self.__yt_service.download_audio(url=video_url, file_path=file_path)

    def __download_playlist(self, playlist: Playlist) -> None:
        idx_num_digits: int = math.floor(math.log10(abs(len(playlist.tracks)))) + 1

        for idx, track in enumerate(playlist.tracks):
            file_path: str = os.path.join(
                config.YOUTUBE_DOWNLOAD_DIRECTORY,
                playlist.name,
                config.FILES_NAME_TEMPLATE.format(
                    title=track.name,
                    artist=track.artist.name,
                    index=f"{idx:>0{idx_num_digits}}",
                ),
            )

            self.__download_track(track=track, file_path=file_path)

    def download_pot(self, pot_url: PotUrl) -> None:
        pot: Optional[Track | Playlist] = self.__spotify_service.get_pot(
            pot_url=pot_url
        )

        if pot is None:
            print(f"No track or playlist found for Spotify URL '{pot_url}'")

        elif isinstance(pot, Track):
            self.__download_track(track=pot)

        else:
            self.__download_playlist(playlist=pot)
