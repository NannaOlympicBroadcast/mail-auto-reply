"""Fetch public GitHub repository information for a given user."""

import requests


GITHUB_API_BASE = "https://api.github.com"


def fetch_user_repos(username: str) -> list[dict]:
    """Return a list of public repos for *username* (up to 100)."""
    url = f"{GITHUB_API_BASE}/users/{username}/repos"
    params = {"type": "public", "per_page": 100, "sort": "updated"}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_user_profile(username: str) -> dict:
    """Return public profile information for *username*."""
    url = f"{GITHUB_API_BASE}/users/{username}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def build_github_context(username: str) -> str:
    """Build a concise text summary of *username*'s public GitHub activity."""
    profile = fetch_user_profile(username)
    repos = fetch_user_repos(username)

    name = profile.get("name") or username
    bio = profile.get("bio") or ""
    blog = profile.get("blog") or ""
    location = profile.get("location") or ""
    public_repos = profile.get("public_repos", 0)

    lines = [
        f"GitHub user: {username}",
        f"Name: {name}",
    ]
    if bio:
        lines.append(f"Bio: {bio}")
    if location:
        lines.append(f"Location: {location}")
    if blog:
        lines.append(f"Website: {blog}")
    lines.append(f"Public repositories: {public_repos}")
    lines.append("")
    lines.append("Recent public repositories:")
    for repo in repos[:20]:
        desc = repo.get("description") or ""
        lang = repo.get("language") or "unknown"
        stars = repo.get("stargazers_count", 0)
        line = f"  - {repo['name']} ({lang}, ★{stars})"
        if desc:
            line += f": {desc}"
        lines.append(line)

    return "\n".join(lines)
