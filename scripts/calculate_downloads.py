from datetime import datetime
import json
import os
import requests

def get_public_repos_names():
    repo_names = []

    url = "https://api.github.com/users/DavidGBrett/repos"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    for repo in data:
        repo_names.append(repo["name"])

    return repo_names

def get_sum_of_release_downloads(repo_name:str):
    total_downloads = 0

    url = f"https://api.github.com/repos/DavidGBrett/{repo_name}/releases"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    for release in data:
        if "assets" not in release: continue

        for asset in release["assets"]:
            total_downloads += asset["download_count"]

    return total_downloads

def update_download_stats_file(repos_to_downloads:dict[str,int], total_profile_downloads:int):
    stats_dir = "stats/"
    os.makedirs(stats_dir, exist_ok=True)
    
    filepath = os.path.join(stats_dir, "repo_downloads.json")
    current_timestamp = datetime.now().isoformat()
    
    # load stats data from stats file
    data = {}
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

        # if it doesn't exist or a bad file we will just write a new file later
        except (json.JSONDecodeError, IOError):
            data = {}
    
    # add new stats
    data[current_timestamp] = {
        "repos": repos_to_downloads,
        "total": total_profile_downloads
    }
    
    # write changes
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, sort_keys=True)    


def run():
    repo_names = get_public_repos_names()

    total_profile_downloads = 0
    repos_to_downloads = {}

    for repo in repo_names:
        repo_downloads = get_sum_of_release_downloads(repo_name=repo)

        print(repo,repo_downloads)
        repos_to_downloads[repo] = repo_downloads

        total_profile_downloads += repo_downloads

    print(total_profile_downloads)

    update_download_stats_file(repos_to_downloads, total_profile_downloads)

if __name__ == "__main__":
    run()