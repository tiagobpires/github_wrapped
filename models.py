class GitHubUser:
    def __init__(self, login, name, bio, location, followers, following, public_repos):
        self.login = login
        self.name = name
        self.bio = bio
        self.location = location
        self.followers = followers
        self.following = following
        self.public_repos = public_repos


class GitHubRepo:
    def __init__(self, name, language, stars, description=""):
        self.name = name
        self.language = language
        self.stars = stars
        self.description = description
