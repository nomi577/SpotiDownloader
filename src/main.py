# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import flet as ft  # type: ignore[import-unknown]

from dotenv import load_dotenv

from app.service import APP


def main(page: ft.Page) -> None:
    load_dotenv()

    app = APP(page=page)

    app.setup_page()


if __name__ == "__main__":
    ft.app(target=main)  # type: ignore[reportUnknownMemberType]
