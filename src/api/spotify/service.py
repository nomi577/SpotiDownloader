# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import time

from spotipy import Spotify  # type: ignore[import-untyped]
from spotipy.oauth2 import SpotifyOAuth  # type: ignore[import-untyped]
from api.classes import Artist, Playlist, Track, Tracks
from typing import Any, Optional
from config import config
from api.spotify.types import SpotifyShareURLType


class SpotifyService:
    def __init__(self) -> None:
        self.__spotify: Spotify = Spotify(auth_manager=SpotifyOAuth)

    def __get_pot_id(self, pot_url: str) -> Optional[tuple[str, SpotifyShareURLType]]:
        if "open.spotify.com/playlist/" in pot_url:
            return pot_url.split("playlist/")[-1].split("?")[
                0
            ], SpotifyShareURLType.PLAYLIST

        if "open.spotify.com/track/" in pot_url:
            return pot_url.split("track/")[-1].split("?")[0], SpotifyShareURLType.TRACK

        return None

    def __parse_artist(self, api_track: dict[str, Any]) -> Artist:
        track_head_artist: dict[str, str] = api_track.get(
            "artists",
            [config.SPOTIFY_DEFAULT_ARTIST],
        )[0]

        return Artist(name=track_head_artist["name"])

    def __parse_track(self, api_track: dict[str, Any]):
        artist: Artist = self.__parse_artist(api_track=api_track)

        track_name: str = api_track.get("name", config.SPOTIFY_DEFAULT_TRACK_NAME)

        return Track(name=track_name, artist=artist)

    def __get_track(self, track_id: str) -> Track:
        api_track: dict[str, Any] = self.__spotify.track(track_id=track_id)  # type: ignore[reportUnknownMemberType]

        name: str = api_track.get("name", config.SPOTIFY_DEFAULT_TRACK_NAME)

        # Get artist
        artist: Artist = self.__parse_artist(api_track=api_track)

        return Track(name=name, artist=artist)

    def __get_tracks(
        self,
        playlist_id: str,
        offset: int = 0,
        batch_size: int = config.SPOTIFY_BATCH_SIZE_TRACKS,
    ) -> Tracks:
        tracks: Tracks = []
        current_tracks: dict[str, Any] = self.__spotify.playlist_tracks(  # type: ignore[reportUnknownMemberType]
            playlist_id=playlist_id,
            offset=offset,
            limit=batch_size,
        )

        for api_track in current_tracks.get("items", []):
            track: Track = self.__parse_track(api_track=api_track.get("track", {}))
            tracks.append(track)

        return tracks

    def __get_all_tracks(self, playlist_id: str) -> Tracks:
        tracks: Tracks = []
        next_batch: Tracks = []

        while len(next_batch) > 0 and len(tracks) < config.SPOTIFY_MAX_TRACKS:
            tracks.extend(next_batch)
            time.sleep(config.SPOTIFY_API_DELAY)
            next_batch = self.__get_tracks(playlist_id=playlist_id, offset=len(tracks))

        return tracks

    def get_playlist(self, playlist_id: str) -> Playlist:
        # Fetch api data
        api_playlist: dict[str, Any] = self.__spotify.playlist(  # type: ignore[reportUnknownMemberType]
            playlist_id=playlist_id
        )

        # Get playlist name
        name: str = api_playlist.get("name", config.SPOTIFY_DEFAULT_PLAYLIST_NAME)

        # Get tracks
        tracks: Tracks = self.__get_all_tracks(playlist_id=playlist_id)

        return Playlist(name=name, tracks=tracks)

    def get_pot(self, pot_url: str) -> Optional[Playlist | Track]:
        parsed_pot_id: Optional[tuple[str, SpotifyShareURLType]] = self.__get_pot_id(
            pot_url=pot_url
        )

        if parsed_pot_id is None:
            return None

        pot_id, url_type = parsed_pot_id

        match url_type:
            case SpotifyShareURLType.PLAYLIST:
                return self.get_playlist(playlist_id=pot_id)

            case SpotifyShareURLType.TRACK:
                return self.__get_track(track_id=pot_id)
