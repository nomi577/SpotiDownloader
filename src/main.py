# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import flet as ft  # type: ignore[import-untyped]

from dotenv import load_dotenv

# Load env variables before everything else
load_dotenv()

from app.service import APP


def main(page: ft.Page) -> None:
    app = APP(page=page)

    app.setup_page()


if __name__ == "__main__":
    ft.app(target=main)  # type: ignore[reportUnknownMemberType]
