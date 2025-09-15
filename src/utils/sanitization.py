# ============================== #
#  Copyright (c) AJ-Holzer       #
#  SPDX-License-Identifier: MIT  #
# ============================== #


import re


def sanitize(filename: str, allowed: str = r"\w") -> str:
    """
    Remove all characters from filename that are not in the allowed set.

    Args:
        filename: The input filename.
        allowed: Characters to allow (regex-style).

    Returns:
        Sanitized filename with only allowed characters.
    """
    pattern = re.compile(rf"[^{allowed}]")
    return pattern.sub("", filename)
