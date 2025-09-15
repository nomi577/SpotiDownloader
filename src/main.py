# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import flet as ft  # type: ignore[import-untyped]

from dotenv import load_dotenv

# Load env variables before everything else
load_dotenv()

from app.service import APP
from config import config


def main(page: ft.Page) -> None:
    print(
        f"{config.SPOTIFY_CLIENT_ID=}, {config.SPOTIFY_CLIENT_SECRET=}, {config.YOUTUBE_DATA_API_V3_API_KEY=}"
    )

    app = APP(page=page)

    app.setup_page()


if __name__ == "__main__":
    ft.app(target=main)  # type: ignore[reportUnknownMemberType]
