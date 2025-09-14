# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


from dotenv import load_dotenv
from api.spotify.service import SpotifyService
from api.youtube.service import YTService


def main() -> None:
    load_dotenv()

    spotify_service: SpotifyService = SpotifyService()
    yt_service: YTService = YTService()


if __name__ == "__main__":
    main()
