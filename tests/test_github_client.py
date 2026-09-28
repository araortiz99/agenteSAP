from src.github.client import GitHubClient


def test_github_client_caches_tree_and_files():
    client = GitHubClient("owner", "repo")
    calls = []

    def fake_request(path):
        calls.append(path)
        if path.startswith("git/trees/"):
            return {"tree": [{"path": "knowledge/a.md", "type": "blob"}]}
        return {
            "type": "file",
            "content": "aGVsbG8=",
        }

    client._request = fake_request

    assert client.get_tree(ref="feature/test") == client.get_tree(ref="feature/test")
    assert client.get_file("knowledge/a.md", ref="feature/test") == "hello"
    assert client.get_file("knowledge/a.md", ref="feature/test") == "hello"

    assert calls == [
        "git/trees/feature%2Ftest?recursive=1",
        "contents/knowledge/a.md?ref=feature%2Ftest",
    ]


def test_github_client_cache_is_scoped_by_ref():
    client = GitHubClient("owner", "repo")
    calls = []

    def fake_request(path):
        calls.append(path)
        if path.startswith("git/trees/"):
            return {"tree": [{"path": path, "type": "blob"}]}
        return {"type": "file", "content": "aGVsbG8="}

    client._request = fake_request

    client.get_tree(ref="main")
    client.get_tree(ref="feature/agent-mvp-search")
    client.get_tree(ref="main")

    assert calls == [
        "git/trees/main?recursive=1",
        "git/trees/feature%2Fagent-mvp-search?recursive=1",
    ]


def test_github_client_get_files_deduplicates_and_uses_cache():
    client = GitHubClient("owner", "repo")
    calls = []

    def fake_request(path):
        calls.append(path)
        return {"type": "file", "content": "aGVsbG8="}

    client._request = fake_request

    result = client.get_files(
        ["a.md", "b.md", "a.md"],
        ref="feature/test",
        max_workers=2,
    )

    assert result == {"a.md": "hello", "b.md": "hello"}
    assert sorted(calls) == [
        "contents/a.md?ref=feature%2Ftest",
        "contents/b.md?ref=feature%2Ftest",
    ]
