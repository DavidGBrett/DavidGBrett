from datetime import datetime, timedelta
import os

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

try:
    from src.constants import config, theme
    from src.utils.data import load_stats, filter_last_n_days, DownloadsDataPoint
    from src.utils.time import round_to_nearest_date_at_midnight
except ImportError:
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from constants import config, theme
    from utils.data import load_stats, filter_last_n_days, DownloadsDataPoint
    from utils.time import round_to_nearest_date_at_midnight

def extract_total_downloads_datapoints(stats_data) -> list[DownloadsDataPoint]:
    # convert timestamps to datetime and extract totals
    points:list[DownloadsDataPoint] = []
    for ts, info in stats_data.items():
        dt = datetime.fromisoformat(ts)
        total = info.get("total", 0)
        points.append(DownloadsDataPoint(dt, total))
    points.sort(key=lambda x: x[0])
    return points


def generate_total_downloads_chart(points: list[DownloadsDataPoint]):
    # ensure directory exists
    os.makedirs(config.CHARTS_DIR, exist_ok=True)

    output_path = os.path.join(config.CHARTS_DIR, config.TOTAL_DOWNLOADS_CHART_FILENAME)

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

    
    # style the major and minor ticks for the x axis
    ax.tick_params(axis='x', which='major', colors=theme.Colors.text, length=6, labelsize=theme.Typography.tick_fontsize)
    ax.tick_params(axis='x', which='minor', colors=theme.Colors.text, length=3, width=1)

    # style y axis ticks
    ax.tick_params(axis='y', colors=theme.Colors.text)

    # grid lines for y axis on major ticks
    ax.grid(True, which='major', axis='y', linestyle=theme.Grid.linestyle,
            alpha=theme.Grid.alpha, color=theme.Colors.structural)

    # grid lines for x axis on both major and minor ticks
    ax.grid(True, which='both', axis='x', linestyle=theme.Grid.linestyle,
            alpha=theme.Grid.alpha, color=theme.Colors.structural)
    

    # fill from line to x axis
    ax.fill_between(dates, totals, 
                    alpha=theme.Fill.alpha, 
                    color=theme.Colors.primary)

    # make y axis start and end around the range of the totals
    ax.set_ylim(bottom=min(totals) * theme.Axis.y_min_margin, 
                top=max(totals) * theme.Axis.y_max_margin)
    
    if len(dates) > 1:
        start_date:datetime = dates[0]
        end_date:datetime = dates[-1]

        # show major ticks at nearest date at midnight to first and last datapoint
        start_edge = round_to_nearest_date_at_midnight(start_date)
        end_edge = round_to_nearest_date_at_midnight(end_date)
        ax.set_xticks([start_edge,end_edge]) # type: ignore

        # show minor ticks for each day
        ax.xaxis.set_minor_locator(mdates.DayLocator())

    # ugly but passable for just one date edge case
    else:
        ax.set_xticks(dates)

    # show day number and abbreviated month on date labels
    formatter = mdates.DateFormatter(theme.Axis.date_format)
    ax.xaxis.set_major_formatter(formatter)    

    # Auto-adjusts subplot spacing to prevent overlapping labels/titles etc
    plt.tight_layout()

    # Save as SVG
    plt.savefig(output_path, format='svg', bbox_inches='tight',
               facecolor='none', edgecolor='none')
    plt.close()


def run():
    data = load_stats()
    points = extract_total_downloads_datapoints(data)
    recent = filter_last_n_days(points)
    generate_total_downloads_chart(recent)

if __name__ == "__main__":
    run()
