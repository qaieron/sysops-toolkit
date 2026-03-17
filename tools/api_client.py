import requests
import argparse
from requests.exceptions import HTTPError
from requests.exceptions import Timeout
from requests.exceptions import ConnectionError
import sys

def api_client(username):
    try:
        user = requests.get(f"https://api.github.com/users/{username}", timeout=10)
        user.raise_for_status()
        repos = requests.get(f"https://api.github.com/users/{username}/repos", timeout=10)
        repos.raise_for_status()

        data = user.json()
        print(f"User:  {data["login"]}")
        print(f"Bio:  {data["bio"]}")
        print(f"Repos:  {data["public_repos"]}")
        print(f"Followers:  {data["followers"]}\n")

        user_repos = repos.json()
        top5 = sorted(user_repos, key=lambda r: r["stargazers_count"], reverse=True)[:5]
        print("Top 5 Repos:\n")

        for repo in top5:
            print(f"{repo["name"]} - {repo["stargazers_count"]} stars")

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print("User not found")

        elif e.response.status_code == 403:
            print("Rate limited — wait a few minutes and try again")
        sys.exit(1)

    except requests.exceptions.Timeout:
        print("Request timed out")
        sys.exit(1)

    except requests.exceptions.ConnectionError:
        print("Connection error — check your internet")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", required=True)
    args = parser.parse_args()
    api_client(args.user)