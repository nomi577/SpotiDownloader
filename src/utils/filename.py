# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


from api.classes import Track
from config import config


def get_filename(track: Track) -> str:
    return config.FILES_TEMPLATE.format(title=track.name, artist=track.artist.name)
