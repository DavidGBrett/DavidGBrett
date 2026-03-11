from datetime import datetime, timedelta
import json
import os

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patheffects as path_effects

from typing import NamedTuple

class DataPoint(NamedTuple):
    date: datetime
    downloads: int

def load_stats(path: str = "gen/stats/repo_downloads.json"):
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


def filter_last_n_days(points: list[DataPoint], days: int = 30) -> list[DataPoint]:
    cutoff = datetime.now() - timedelta(days=days)
    return [DataPoint(dt, total) for dt, total in points if dt >= cutoff]


def make_chart(points: list[DataPoint], output_path: str = "gen/charts/downloads.png"):
    # ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if not points:
        # create empty placeholder image
        plt.figure()
        plt.text(0.5, 0.5, "no data", ha="center", va="center")
        plt.savefig(output_path)
        plt.close()
        return

    dates, totals = zip(*points)

    # create fig
    fig = plt.figure(figsize=(8, 4))
    # get axes
    ax = plt.gca()

    fig.patch.set_alpha(0)  # Transparent figure background
    ax.set_facecolor('none')  # Transparent axes background

    line = ax.plot(dates, totals, 
            linestyle="solid", 
            marker="o",
            color='#4ECDC4',  
            linewidth=2.5,
            markersize=6,
            markeredgewidth=1.5,
            markeredgecolor='white', 
            markerfacecolor='#4ECDC4',
            alpha=0.9)
    
    ax.set_title("Downloads Across My Repositories", 
                color="#9BD1CE", 
                fontsize=14, 
                fontweight='semibold', 
                pad=20,
                )
    
    plt.suptitle(f'Latest Total: {totals[-1]}',
                y = 0.8,
                x = 0.52,
                fontsize=10,
                fontweight='semibold',
                color='#CCCCCC')

    ax.set_ylabel("Downloads", 
                color='#CCCCCC', 
                fontsize=12, 
                fontweight='semibold')
    ax.set_xlabel("Date", 
                color='#CCCCCC', 
                fontsize=12, 
                x = 0.48,
                fontweight='semibold')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#666666')
    ax.spines['left'].set_color('#666666')

    ax.tick_params(axis='both', 
                colors='#CCCCCC', 
                labelsize=10)

    ax.grid(True, 
            linestyle='--', 
            alpha=0.3, 
            color='#666666')

    # fill from line to x axis
    ax.fill_between(dates, totals, 
                    alpha=0.2, 
                    color='#4ECDC4')

    # make y axis start and end around the range of the totals
    ax.set_ylim(bottom=min(totals) * 0.95, top=max(totals)*1.01)
    
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
    formatter = mdates.DateFormatter("%d %b")
    ax.xaxis.set_major_formatter(formatter)

    # tilt date labels
    ax.xaxis.set_tick_params(rotation=45)

    # Auto-adjusts subplot spacing to prevent overlapping labels/titles etc
    plt.tight_layout()

    plt.savefig(output_path)
    plt.close()


def run():
    data = load_stats()
    points = extract_total_downloads_datapoints(data)
    recent = filter_last_n_days(points, days=30)
    make_chart(recent)

if __name__ == "__main__":
    run()