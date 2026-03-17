from utils import (
    get_total_stars,
    get_most_used_language,
    get_top_repositories,
    generate_wrapped_image,
)
from github_client import GitHubClient


def print_wrapped(user, repositories):
    total_stars = get_total_stars(repositories)
    most_used_language = get_most_used_language(repositories)
    top_repositories = get_top_repositories(repositories, limit=3)

    print("\n=== GITHUB WRAPPED ===\n")
    print(f"Name: {user.name}")
    print(f"Bio: {user.bio}")
    print(f"Location: {user.location}")
    print(f"Followers: {user.followers}")
    print(f"Following: {user.following}")
    print(f"Public Repositories: {user.public_repos}")
    print(f"Total Stars: {total_stars}")
    print(f"Most Used Language: {most_used_language}")

    print("\nTop 3 Repositories:")
    if not top_repositories:
        print("No public repositories found.")
        return

    for index, repo in enumerate(top_repositories, start=1):
        print(f"{index}. {repo.name} - {repo.stars} stars")

    image_path = generate_wrapped_image(
        user=user,
        total_stars=total_stars,
        most_used_language=most_used_language,
        top_repositories=top_repositories,
    )
    print(f"\nImagem gerada: {image_path}")


def main():
    username = input("Enter a GitHub username: ").strip()
    client = GitHubClient()

    try:
        user = client.get_user(username)
        repositories = client.get_repositories(username)
        print_wrapped(user, repositories)
    except ValueError as error:
        print(error)
    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
