"""Generate a bar chart showing downloads for the top N repositories."""

import os

import matplotlib.pyplot as plt

try:
    from src.constants import config, theme
    from src.utils.data import load_stats
except ImportError:
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from constants import config, theme
    from utils.data import load_stats
    config.TOP_REPOS_COUNT = 3


def get_latest_stats(stats_data: dict) -> dict:
    """Get the latest stats entry from the data."""
    if not stats_data:
        return {}
    # Get the last timestamp (latest entry)
    latest_ts = list(stats_data.keys())[-1]
    return stats_data[latest_ts]


def get_top_repos(repos_data: dict) -> list[tuple[str, int]]:
    """
    Get the top N repositories by download count.
    
    Args:
        repos_data: Dictionary of repo names to download counts
    
    Returns:
        List of (repo_name, download_count) tuples sorted by downloads descending
    """
    # Filter out repos with 0 downloads
    filtered = {name: count for name, count in repos_data.items() if count > 0}
    
    # Sort by downloads descending and take top N
    sorted_repos = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
    return sorted_repos[:config.TOP_REPOS_COUNT]


def generate_top_repos_chart(repos: list[tuple[str, int]]):
    """
    Generate a bar chart showing downloads for top repositories.
    
    Args:
        repos: List of (repo_name, download_count) tuples
    """
    # Ensure directory exists
    os.makedirs(config.CHARTS_DIR, exist_ok=True)

    output_path = os.path.join(config.CHARTS_DIR, config.TOP_REPOS_CHART_FILENAME)

    if not repos:
        # Create empty placeholder image
        plt.figure(figsize=theme.Figure.figsize)
        plt.text(0.5, 0.5, "no data", ha="center", va="center", 
                color=theme.Colors.text)
        plt.savefig(output_path, format='svg', bbox_inches='tight', 
                   facecolor='none', edgecolor='none')
        plt.close()
        return

    repo_names, download_counts = zip(*repos)

    # Create figure
    fig = plt.figure(figsize=theme.Figure.figsize)
    ax = plt.gca()

    fig.patch.set_alpha(theme.Figure.background_alpha)  # Transparent background
    ax.set_facecolor('none')

    # Create bars with faded fill and set URLs
    bars = ax.bar(repo_names, download_counts,
                   color=theme.Colors.primary,
                   alpha=theme.Fill.alpha)
    
    # Add GitHub URLs to each bar
    for bar, repo_name in zip(bars, repo_names):
        github_url = f"https://github.com/{config.GITHUB_USERNAME}/{repo_name}"
        bar.set_url(github_url)

    # Add GitHub URLs to the x-axis labels
    xticklabels = ax.get_xticklabels()
    for label, repo_name in zip(xticklabels, repo_names):
        github_url = f"https://github.com/{config.GITHUB_USERNAME}/{repo_name}"

        # makes the stroke of the text clickable
        label.set_url(github_url)
        # also want a bounding box to be clickable
        label.set_bbox(
            dict(
                url=github_url,
                boxstyle='round,pad=0.5',

                # cant directly set it to be invisible - basically have to trick it or it wont render this
                # though it does seem to round this down to 0 opacity
                facecolor='#00000001',
                edgecolor='#00000001',
                alpha=0.0000000000000000000000000001
            )
        )
        

    # Add solid top line to each bar to match line chart style
    for bar, height in zip(bars, download_counts):
        ax.plot([bar.get_x(), bar.get_x() + bar.get_width()], [height, height],
                color=theme.Colors.primary, linewidth=2)

    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{int(height)}',
                    xy=(bar.get_x() + bar.get_width() / 2., height),
                    xytext=(0, 5),
                    textcoords='offset points',
                    ha='center',
                    color=theme.Colors.text,
                    fontsize=11,
                    fontweight='semibold')

    ax.set_title("Top Repositories by Downloads",
                 color=theme.Colors.title,
                 fontsize=theme.Typography.title_fontsize,
                 fontweight=theme.Typography.title_fontweight,
                 pad=theme.Typography.title_pad)

    ax.set_ylabel("Downloads",
                  color=theme.Colors.text,
                  fontsize=theme.Typography.label_fontsize,
                  fontweight=theme.Typography.label_fontweight)

    # Style axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(theme.Colors.structural)
    ax.spines['left'].set_color(theme.Colors.structural)

    ax.tick_params(axis='both',
                   colors=theme.Colors.text,
                   labelsize=8)

    # Style grid
    ax.grid(True, axis='y',
            linestyle=theme.Grid.linestyle,
            alpha=theme.Grid.alpha,
            color=theme.Colors.structural)

    # Set y-axis limits with margins
    max_downloads = max(download_counts)
    ax.set_ylim(bottom=0, top=max_downloads * theme.Axis.y_max_margin)

    # Auto-adjust layout
    plt.tight_layout()

    # Save as SVG
    plt.savefig(output_path, format='svg', bbox_inches='tight',
               facecolor='none', edgecolor='none')
    plt.close()


def run():
    data = load_stats()
    latest_stats = get_latest_stats(data)
    repos_data = latest_stats.get("repos", {})
    top_repos = get_top_repos(repos_data)
    generate_top_repos_chart(top_repos)


if __name__ == "__main__":
    run()
