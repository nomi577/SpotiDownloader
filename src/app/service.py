# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import flet as ft  # type: ignore[import-untyped]

from config import config
from api.spotify.service import SpotifyService
from api.youtube.service import YTService
from downloader import Downloader
from api.spotify.types import PotUrl
from typing import Optional


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
        )

        # Create widgets
        self.__url_entry: ft.TextField = ft.TextField(label="Spotify URL")

    def __update_entry_status(self) -> None: ...

    def download_pot(self) -> None:
        pot_url: Optional[str] = self.__url_entry.value

        if pot_url is None:
            self.__update_entry_status()

        # self.__downloader.download_pot(pot_url=PotUrl(str(self.__url_entry.value)))

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
                        ft.Text(value="Hello World!"),
                    ],
                )
            ],
        )

        self.__page.add(page)
