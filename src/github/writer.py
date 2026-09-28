"""Bounded GitHub writer for explicit Knowledge Governance operations.

This client is intentionally separate from the read-only GitHubClient.
It only supports branch creation, file writes and Pull Request creation.
"""

from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.parse
import urllib.request


class GitHubWriteError(RuntimeError):
    """Raised when a controlled GitHub write cannot be completed."""


class GitHubWriteClient:
    PROTECTED_REFS = {"main", "master"}

    def __init__(self, owner: str, repo: str, token: str | None = None, api_version: str = "2026-03-10") -> None:
        self.owner = owner
        self.repo = repo
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.api_version = api_version

    def _request(self, method: str, path: str, payload: dict | None = None) -> object:
        if not self.token:
            raise GitHubWriteError("GITHUB_TOKEN is not configured")
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/{path.lstrip('/')}"
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": self.api_version,
            "User-Agent": "agenteSAP/0.1",
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                raw = response.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise GitHubWriteError(
                f"GitHub API returned HTTP {exc.code} for {method} {path}: {detail[:500]}"
            ) from exc
        except urllib.error.URLError as exc:
            raise GitHubWriteError(
                f"GitHub API unavailable for {method} {path}: {exc.reason}"
            ) from exc

    def get_branch_sha(self, ref: str) -> str:
        encoded = urllib.parse.quote(ref, safe="")
        data = self._request("GET", f"git/ref/heads/{encoded}")
        try:
            return str(data["object"]["sha"])
        except (KeyError, TypeError) as exc:
            raise GitHubWriteError(f"Could not resolve branch SHA for {ref}") from exc

    def create_branch(self, branch: str, *, base_ref: str) -> str:
        branch = branch.strip()
        if not branch:
            raise ValueError("branch must not be empty")
        if branch in self.PROTECTED_REFS:
            raise GitHubWriteError("Protected branch cannot be used as a change branch")
        base_sha = self.get_branch_sha(base_ref)
        data = self._request(
            "POST",
            "git/refs",
            {"ref": f"refs/heads/{branch}", "sha": base_sha},
        )
        try:
            return str(data["object"]["sha"])
        except (KeyError, TypeError) as exc:
            raise GitHubWriteError("GitHub did not return the created branch SHA") from exc

    def get_file(self, path: str, *, ref: str) -> dict | None:
        encoded_path = urllib.parse.quote(path, safe="/")
        encoded_ref = urllib.parse.quote(ref, safe="")
        try:
            data = self._request("GET", f"contents/{encoded_path}?ref={encoded_ref}")
        except GitHubWriteError as exc:
            if "HTTP 404" in str(exc):
                return None
            raise
        if not isinstance(data, dict):
            raise GitHubWriteError(f"Invalid GitHub file response for {path}")
        return data

    def put_file(self, path: str, content: str, *, branch: str, message: str, sha: str | None = None) -> str:
        if not path.strip():
            raise ValueError("path must not be empty")
        payload = {
            "message": message,
            "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
            "branch": branch,
        }
        if sha:
            payload["sha"] = sha
        data = self._request("PUT", f"contents/{path.lstrip('/')}", payload)
        try:
            return str(data["commit"]["sha"])
        except (KeyError, TypeError) as exc:
            raise GitHubWriteError("GitHub did not return the commit SHA") from exc

    def create_pull_request(self, *, title: str, body: str, head: str, base: str) -> dict:
        if head.strip() == base.strip():
            raise GitHubWriteError("Pull Request head must differ from base")
        data = self._request(
            "POST",
            "pulls",
            {"title": title, "body": body, "head": head, "base": base},
        )
        if not isinstance(data, dict):
            raise GitHubWriteError("Invalid Pull Request response")
        return data
