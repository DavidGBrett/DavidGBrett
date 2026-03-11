"""Data utilities for loading and processing stats."""

import json
import os
from datetime import datetime
from typing import NamedTuple

try:
    from src.constants import config
except ImportError:
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from constants import config


class DataPoint(NamedTuple):
    date: datetime
    downloads: int


def load_stats() -> dict:
    """Load stats data from the configured stats file."""
    path = os.path.join(config.STATS_DIR, config.DOWNLOADS_STATS_FILENAME)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Stats file not found: {path}")
    with open(path, "r") as f:
        data = json.load(f)
    return data
