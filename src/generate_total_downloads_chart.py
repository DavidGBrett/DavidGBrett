from datetime import datetime, timedelta
import json
import os

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from typing import NamedTuple

try:
    from src.constants import config, theme
except ImportError:
    from constants import config, theme

class DataPoint(NamedTuple):
    date: datetime
    downloads: int

def load_stats():
    path = os.path.join(config.STATS_DIR, config.DOWNLOADS_STATS_FILENAME)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Stats file not found: {path}")
    with open(path, "r") as f:
        data = json.load(f)
    return data

def extract_total_downloads_datapoints(stats_data) -> list[DataPoint]:
    # convert timestamps to datetime and extract totals
    points:list[DataPoint] = []
    for ts, info in stats_data.items():
        dt = datetime.fromisoformat(ts)
        total = info.get("total", 0)
        points.append(DataPoint(dt, total))
    points.sort(key=lambda x: x[0])
    return points


def filter_last_n_days(points: list[DataPoint], days: int = config.DOWNLOADS_DAYS_FILTER) -> list[DataPoint]:
    cutoff = datetime.now() - timedelta(days=days)
    return [DataPoint(dt, total) for dt, total in points if dt >= cutoff]


def make_chart(points: list[DataPoint]):
    # ensure directory exists
    os.makedirs(config.CHARTS_DIR, exist_ok=True)

    output_path = os.path.join(config.CHARTS_DIR, config.DOWNLOADS_CHART_FILENAME)

    if not points:
        # create empty placeholder image
        plt.figure()
        plt.text(0.5, 0.5, "no data", ha="center", va="center")
        plt.savefig(output_path)
        plt.close()
        return

    dates, totals = zip(*points)

    # create fig
    fig = plt.figure(figsize=theme.Figure.figsize)
    # get axes
    ax = plt.gca()

    fig.patch.set_alpha(theme.Figure.background_alpha)  # Transparent figure background
    ax.set_facecolor('none')  # Transparent axes background

    line = ax.plot(dates, totals, 
            linestyle=theme.Line.linestyle, 
            marker="o",
            color=theme.Colors.primary,  
            linewidth=theme.Line.linewidth,
            markersize=theme.Marker.markersize,
            markeredgewidth=theme.Marker.markeredgewidth,
            markeredgecolor=theme.Colors.marker_edge, 
            markerfacecolor=theme.Colors.primary,
            alpha=theme.Line.alpha)
    
    ax.set_title("Downloads Across My Repositories", 
                color=theme.Colors.title, 
                fontsize=theme.Typography.title_fontsize, 
                fontweight=theme.Typography.title_fontweight, 
                pad=theme.Typography.title_pad,
                )
    
    plt.suptitle(f'Latest Total: {totals[-1]}',
                y = 0.8,
                x = 0.52,
                fontsize=theme.Typography.subtitle_fontsize,
                fontweight=theme.Typography.subtitle_fontweight,
                color=theme.Colors.text)

    ax.set_ylabel("Downloads", 
                color=theme.Colors.text, 
                fontsize=theme.Typography.label_fontsize, 
                fontweight=theme.Typography.label_fontweight)
    ax.set_xlabel("Date", 
                color=theme.Colors.text, 
                fontsize=theme.Typography.label_fontsize,
                x = 0.48,
                fontweight=theme.Typography.label_fontweight)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(theme.Colors.structural)
    ax.spines['left'].set_color(theme.Colors.structural)

    ax.tick_params(axis='both', 
                colors=theme.Colors.text, 
                labelsize=theme.Typography.tick_fontsize)

    ax.grid(True, 
            linestyle=theme.Grid.linestyle, 
            alpha=theme.Grid.alpha, 
            color=theme.Colors.structural)

    # fill from line to x axis
    ax.fill_between(dates, totals, 
                    alpha=theme.Fill.alpha, 
                    color=theme.Colors.primary)

    # make y axis start and end around the range of the totals
    ax.set_ylim(bottom=min(totals) * theme.Axis.y_min_margin, 
                top=max(totals) * theme.Axis.y_max_margin)
    
    # place exactly 5 ticks evenly from first to last date to guarantee endpoints
    if len(dates) > 5:
        num_ticks = 5
        tick_dates = [dates[0] + (dates[-1] - dates[0]) * i / (num_ticks - 1) for i in range(num_ticks)]
    # handle edge cases
    elif len(dates) > 1:
        tick_dates = [dates[0],dates[-1]]    
    else:
        tick_dates = dates
    
    ax.set_xticks(tick_dates)

    # show day number and abbreviated month on date labels
    formatter = mdates.DateFormatter(theme.Axis.date_format)
    ax.xaxis.set_major_formatter(formatter)

    # tilt date labels
    ax.xaxis.set_tick_params(rotation=theme.Axis.tick_rotation)

    # Auto-adjusts subplot spacing to prevent overlapping labels/titles etc
    plt.tight_layout()

    plt.savefig(output_path)
    plt.close()


def run():
    data = load_stats()
    points = extract_total_downloads_datapoints(data)
    recent = filter_last_n_days(points)
    make_chart(recent)

if __name__ == "__main__":
    run()