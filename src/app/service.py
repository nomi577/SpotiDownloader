# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import flet as ft  # type: ignore[import-untyped]

from config import config
from api.spotify.service import SpotifyService
from api.classes import Tracks, Track
from api.youtube.service import YTService
from downloader import Downloader
from api.spotify.types import PotUrl
from typing import Optional
from utils.pot_url import validate_pot_url


class APP:
    def __init__(self, page: ft.Page) -> None:
        self.__page: ft.Page = page

        # Define app ui tweaks
        self.__page.title = config.APP_TITLE
        self.__page.window.resizable = config.APP_RESIZABLE
        self.__page.window.width = config.APP_WIDTH
        self.__page.window.height = config.APP_HEIGHT

        # Create Spotify, YouTube and Downloader instances
        self.__spotify_service: SpotifyService = SpotifyService()
        self.__yt_service: YTService = YTService()
        self.__downloader: Downloader = Downloader(
            spotify_service=self.__spotify_service,
            yt_service=self.__yt_service,
            on_set_tracks=self.__set_download_tracks_list,
            on_mark_downloaded=self.__mark_downloaded,
            on_mark_downloading=self.__mark_downloading,
            on_mark_error=self.__mark_error,
        )

        # Create widgets
        self.__download_tracks: dict[str, ft.Icon] = {}
        self.__download_tracks_list: ft.ListView = ft.ListView(
            controls=[],
            padding=ft.Padding(left=50, top=50, right=50, bottom=50),
            expand=True,
            spacing=10,
        )
        self.__url_entry: ft.TextField = ft.TextField(label="Spotify URL")
        self.__download_button: ft.ElevatedButton = ft.ElevatedButton(
            text="Download",
            on_click=lambda _: self.__download_pot(),
        )

    def __get_track_widget(self, track: Track) -> tuple[ft.Container, ft.Icon]:
        track_status_icon: ft.Icon = ft.Icon(name=ft.Icons.HOURGLASS_EMPTY)

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text(
                                value=f"{track.name} by {track.artist.name}",
                                expand=True,
                            )
                        ],
                        expand=True,
                    ),
                    ft.Column(
                        controls=[track_status_icon],
                    ),
                ],
                expand=True,
            ),
            expand=True,
        ), track_status_icon

    def __set_download_tracks_list(self, tracks: Tracks) -> None:
        for track in tracks:
            track_widget, icon = self.__get_track_widget(track=track)

            self.__download_tracks[track.id] = icon
            self.__download_tracks_list.controls.append(track_widget)

        self.__download_tracks_list.update()

    def __update_track_status_icon(
        self, track_id: str, icon: ft.IconValue, hint: Optional[str] = None
    ) -> None:
        status_icon = self.__download_tracks[track_id]

        status_icon.name = icon
        status_icon.tooltip = hint

        status_icon.update()

    def __mark_downloaded(self, track_id: str) -> None:
        self.__update_track_status_icon(
            track_id=track_id,
            icon=ft.Icons.DOWNLOAD_DONE_OUTLINED,
        )

    def __mark_downloading(self, track_id: str) -> None:
        self.__update_track_status_icon(
            track_id=track_id,
            icon=ft.Icons.DOWNLOADING_OUTLINED,
        )

    def __mark_error(self, track_id: str, error: str) -> None:
        self.__update_track_status_icon(
            track_id=track_id,
            icon=ft.Icons.ERROR_OUTLINE,
            hint=error,
        )

    def __update_entry_status(self, valid: bool) -> None:
        self.__url_entry.border_color = None if valid else ft.Colors.ERROR
        self.__url_entry.update()

    def __download_pot(self) -> None:
        try:
            entry_value: Optional[str] = self.__url_entry.value

            if entry_value is None:
                self.__update_entry_status(valid=False)
                self.__page.open(
                    control=ft.SnackBar(content=ft.Text(value="Spotify URL required!"))
                )
                return

            pot_url: PotUrl = PotUrl(entry_value)

            if not validate_pot_url(pot_url=pot_url):
                self.__update_entry_status(valid=False)
                self.__page.open(
                    control=ft.SnackBar(content=ft.Text(value="Invalid Spotify URL!"))
                )
                return

            self.__update_entry_status(valid=True)
            self.__downloader.download_pot(pot_url=pot_url)
        except Exception as e:
            self.__page.open(control=ft.SnackBar(content=ft.Text(value=str(e))))

    def setup_page(self) -> None:
        page: ft.Row = ft.Row(
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Column(controls=[self.__url_entry], expand=True),
                                ft.Column(controls=[self.__download_button]),
                            ],
                        ),
                        ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[self.__download_tracks_list],
                                    expand=True,
                                )
                            ],
                            expand=True,
                        ),
                    ],
                )
            ],
        )

        self.__page.add(page)
