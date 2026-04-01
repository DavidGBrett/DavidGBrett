"""Configuration constants for GitHub Profile scripts."""

# GitHub API Configuration
GITHUB_USERNAME = "DavidGBrett"
GITHUB_REPOS_API_URL = "https://api.github.com/users/{username}/repos"
GITHUB_RELEASES_API_URL = "https://api.github.com/repos/{username}/{repo_name}/releases"

# Directory Paths
STATS_DIR = "gen/stats"
CHARTS_DIR = "gen/charts"

# File Names
DOWNLOADS_STATS_FILENAME = "repo_downloads.json"
TOTAL_DOWNLOADS_CHART_FILENAME = "total_downloads_chart.svg"
TOP_REPOS_CHART_FILENAME = "top_repos_downloads_chart.svg"

# Other
DOWNLOADS_DAYS_FILTER = 14
TOP_REPOS_COUNT = 3
