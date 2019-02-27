import requests
from datetime import datetime, timedelta


GITHUB_API_URL = "https://api.github.com"
DISPLAY_REPOS = 20


def github_search_repos(query, sort="stars", order="desc", page=1, per_page=20):
    endpoint = "{}{}".format(GITHUB_API_URL, "/search/repositories")
    payload = {
        "q": query,
        "sort": sort,
        "order": order,
        "page": page,
        "per_page": per_page
    }
    search_results = requests.get(endpoint, payload)
    return search_results


def github_get_repo_issues(owner, repo, state="all"):
    endpoint = "{}{}".format(GITHUB_API_URL, "/repos/{}/{}/issues".format(
        owner,
        repo
    ))
    payload = {
        "state": state
    }
    issues = requests.get(endpoint, payload)
    return issues.json()


def get_trending_repositories(top_size):
    last_week = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    query = "created:>={}".format(last_week)
    repos = github_search_repos(query, per_page=top_size)
    return repos.json()["items"]


def get_open_issues_amount(repo_owner, repo_name):
    return len(github_get_repo_issues(repo_owner, repo_name, "open"))


def main():
    repos = get_trending_repositories(DISPLAY_REPOS)
    print("Github trending\n")
    for repo in repos:
        # owner_name = repo["owner"]["login"]
        repo_name = repo["name"]
        desc = repo["description"]
        url = repo["html_url"]
        stars = repo["stargazers_count"]
        # open_issues_count = get_open_issues_amount(owner_name, repo_name)
        open_issues_count = repo["open_issues"]
        print("*{} {}: {} ".format(stars, repo_name, desc))
        print(" URL: {}".format(url))
        print(" Opened issues: {}".format(open_issues_count))


if __name__ == "__main__":
    main()
