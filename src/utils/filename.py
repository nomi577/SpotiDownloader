# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


from api.classes import Track
from config import config
from utils.sanitization import sanitize


def get_filename(track: Track) -> str:
    return sanitize(
        config.FILES_NAME_TEMPLATE.format(title=track.name, artist=track.artist.name)
    )
