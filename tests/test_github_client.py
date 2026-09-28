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
            "content": "aGVsbG8=",  # "hello"
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
