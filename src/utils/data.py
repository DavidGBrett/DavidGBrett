"""Data utilities for loading and processing stats."""

import json
import os
from datetime import datetime, timedelta
from typing import NamedTuple

try:
    from src.constants import config
except ImportError:
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from constants import config


class DownloadsDataPoint(NamedTuple):
    date: datetime
    downloads: int

def filter_last_n_days(points: list[DownloadsDataPoint], days: int = config.DOWNLOADS_DAYS_FILTER) -> list[DownloadsDataPoint]:
    cutoff = datetime.now() - timedelta(days=days)
    return [DownloadsDataPoint(dt, total) for dt, total in points if dt >= cutoff]

def load_stats() -> dict:
    """Load stats data from the configured stats file."""
    path = os.path.join(config.STATS_DIR, config.DOWNLOADS_STATS_FILENAME)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Stats file not found: {path}")
    with open(path, "r") as f:
        data = json.load(f)
    return data
