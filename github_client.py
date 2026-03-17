import requests

from models import GitHubUser, GitHubRepo


class GitHubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self):
        self.headers = {"Accept": "application/vnd.github+json"}

    def get_user(self, username):
        response = requests.get(
            f"{self.BASE_URL}/users/{username}", headers=self.headers, timeout=10
        )

        if response.status_code == 404:
            raise ValueError("User not found.")

        if response.status_code != 200:
            raise Exception(f"Error fetching user: {response.status_code}")

        data = response.json()

        return GitHubUser(
            login=data["login"],
            name=data.get("name") or "Not provided",
            bio=data.get("bio") or "No bio",
            location=data.get("location") or "Not provided",
            followers=data["followers"],
            following=data["following"],
            public_repos=data["public_repos"],
        )

    def get_repositories(self, username):
        response = requests.get(
            f"{self.BASE_URL}/users/{username}/repos",
            headers=self.headers,
            params={"per_page": 100},
            timeout=10,
        )

        if response.status_code != 200:
            raise Exception(f"Error fetching repositories: {response.status_code}")

        repositories = []
        data = response.json()

        for repo in data:
            repositories.append(
                GitHubRepo(
                    name=repo["name"],
                    language=repo.get("language") or "Unknown",
                    stars=repo["stargazers_count"],
                    description=repo.get("description") or "",
                )
            )

        return repositories
