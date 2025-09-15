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
        )

        # Create widgets
        self.__url_entry: ft.TextField = ft.TextField(label="Spotify URL")
        self.__download_button: ft.ElevatedButton = ft.ElevatedButton(
            text="Download",
            on_click=lambda _: self.__download_pot(),
        )

    def __update_entry_status(self, valid: bool) -> None:
        self.__url_entry.border_color = None if valid else ft.Colors.ERROR
        self.__url_entry.update()

    def __download_pot(self) -> None:
        try:
            entry_value: Optional[str] = self.__url_entry.value

            if entry_value is None:
                self.__update_entry_status(valid=False)
                return

            pot_url: PotUrl = PotUrl(entry_value)

            if not validate_pot_url(pot_url=pot_url):
                print("Invalid URL!")
                self.__update_entry_status(valid=False)
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
                        self.__url_entry,
                        self.__download_button,
                    ],
                )
            ],
        )

        self.__page.add(page)
