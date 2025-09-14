# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


from typing import NewType
from typing import TypedDict


YTVideoUrl = NewType("YTVideoUrl", str)


class YDLOptions(TypedDict):
    outtmpl: str
    quiet: bool
    noplaylist: bool
    restrictfilenames: bool
