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



if __name__ == "__main__":
    repo_names = get_public_repos_names()

    total_profile_downloads = 0

    for repo in repo_names:
        repo_downloads = get_sum_of_release_downloads(repo_name=repo)

        print(repo,repo_downloads)

        total_profile_downloads += repo_downloads

    print(total_profile_downloads)