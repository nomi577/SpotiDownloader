# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import re

from api.spotify.types import PotUrl


def validate_pot_url(pot_url: PotUrl) -> bool:
    return (
        re.fullmatch(
            pattern=r"https://open.spotify.com/(playlist|track)/[A-Za-z0-9]{22}\?si=[A-Za-z0-9]{16,32}",
            string=pot_url,
        )
        is not None
    )
