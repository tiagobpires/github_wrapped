from models import GitHubRepo, GitHubUser
from utils import (
    generate_wrapped_image,
    get_most_used_language,
    get_top_repositories,
    get_total_stars,
)


def main():
    user = GitHubUser(
        login="tiagobpires",
        name="Tiago Barros Pires",
        bio="Desenvolvedor e Educador na Behring com foco em backend e APIs.",
        location="Brasil",
        followers=123,
        following=45,
        public_repos=67,
    )

    repositories = [
        GitHubRepo(
            name="introduction_to_api",
            language="Python",
            stars=42,
            description="Projeto de aula sobre APIs em Python.",
        ),
        GitHubRepo(
            name="behring-backend",
            language="Python",
            stars=31,
            description="Backend principal com foco em escalabilidade.",
        ),
        GitHubRepo(
            name="frontend-labs",
            language="TypeScript",
            stars=17,
            description="Experimentos de UI e integração com APIs.",
        ),
        GitHubRepo(
            name="automation-scripts",
            language="Python",
            stars=8,
            description="Scripts utilitários para automação diária.",
        ),
    ]

    total_stars = get_total_stars(repositories)
    most_used_language = get_most_used_language(repositories)
    top_repositories = get_top_repositories(repositories, limit=3)

    output_path = generate_wrapped_image(
        user=user,
        total_stars=total_stars,
        most_used_language=most_used_language,
        top_repositories=top_repositories,
    )

    print(f"Imagem gerada: {output_path}")


if __name__ == "__main__":
    main()
