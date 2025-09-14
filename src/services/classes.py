# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


from dataclasses import dataclass


@dataclass
class Artist:
    name: str


@dataclass
class Track:
    name: str


Tracks = list[Track]


@dataclass
class Playlist:
    name: str
    tracks: Tracks
