import requests
from datetime import datetime, timedelta


GITHUB_API_URL = "https://api.github.com"
DISPLAY_REPOS = 20


def fetch_github_repos(query, sort="stars", order="desc", page=1, per_page=20):
    endpoint = "{}{}".format(GITHUB_API_URL, "/search/repositories")
    payload = {
        "q": query,
        "sort": sort,
        "order": order,
        "page": page,
        "per_page": per_page
    }
    return requests.get(endpoint, payload)


def get_trending_repositories(top_size):
    last_week = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    query = "created:>={}".format(last_week)
    repos = fetch_github_repos(query, per_page=top_size)
    return repos.json()["items"]


def main():
    repos = get_trending_repositories(DISPLAY_REPOS)
    print("Github trending\n")
    for repo in repos:
        repo_name = repo["name"]
        desc = repo["description"]
        url = repo["html_url"]
        stars = repo["stargazers_count"]
        open_issues_count = repo["open_issues"]
        print("*{} {}: {} ".format(stars, repo_name, desc))
        print(" URL: {}".format(url))
        print(" Opened issues: {}".format(open_issues_count))


if __name__ == "__main__":
    main()
