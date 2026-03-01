"""Tests for github_fetcher module."""

from unittest.mock import MagicMock, patch

import pytest

from github_fetcher import build_github_context, fetch_user_profile, fetch_user_repos


MOCK_PROFILE = {
    "login": "NannaOlympicBroadcast",
    "name": "Nanna",
    "bio": "本人忙于考研",
    "location": "China",
    "blog": "https://haiyanfl.cn",
    "public_repos": 2,
}

MOCK_REPOS = [
    {
        "name": "clawdbot-wechat-plugin",
        "description": "WeChat bot plugin",
        "language": "TypeScript",
        "stargazers_count": 23,
    },
    {
        "name": "gdocs2feishu",
        "description": "Sync Google Docs to Feishu",
        "language": "Python",
        "stargazers_count": 0,
    },
]


def _mock_response(json_data):
    resp = MagicMock()
    resp.json.return_value = json_data
    resp.raise_for_status.return_value = None
    return resp


@patch("github_fetcher.requests.get")
def test_fetch_user_profile(mock_get):
    mock_get.return_value = _mock_response(MOCK_PROFILE)
    profile = fetch_user_profile("NannaOlympicBroadcast")
    assert profile["login"] == "NannaOlympicBroadcast"
    mock_get.assert_called_once()


@patch("github_fetcher.requests.get")
def test_fetch_user_repos(mock_get):
    mock_get.return_value = _mock_response(MOCK_REPOS)
    repos = fetch_user_repos("NannaOlympicBroadcast")
    assert len(repos) == 2
    assert repos[0]["name"] == "clawdbot-wechat-plugin"


@patch("github_fetcher.fetch_user_repos", return_value=MOCK_REPOS)
@patch("github_fetcher.fetch_user_profile", return_value=MOCK_PROFILE)
def test_build_github_context(mock_profile, mock_repos):
    ctx = build_github_context("NannaOlympicBroadcast")
    assert "NannaOlympicBroadcast" in ctx
    assert "clawdbot-wechat-plugin" in ctx
    assert "TypeScript" in ctx
    assert "考研" in ctx
