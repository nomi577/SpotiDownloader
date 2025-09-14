# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


from dotenv import load_dotenv
from api.spotify.service import SpotifyService
from api.youtube.service import YTService
from downloader import Downloader
from api.spotify.types import PotUrl


def main() -> None:
    load_dotenv()

    spotify_service: SpotifyService = SpotifyService()
    yt_service: YTService = YTService()
    downloader: Downloader = Downloader(
        spotify_service=spotify_service,
        yt_service=yt_service,
    )

    while True:
        user_input: str = input(
            "Enter a playlist or track url to download or type 'exit' to quit > "
        )

        match user_input:
            case "exit":
                break

            case _:
                downloader.download_pot(pot_url=PotUrl(user_input))


if __name__ == "__main__":
    main()
