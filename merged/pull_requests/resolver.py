from dataclasses import dataclass
from datetime import datetime, timedelta

import humanize
from github import Github, IssueEvent

from merged.config import DAYS_TO_REVIEW, GITHUB_TOKEN


@dataclass
class MergedPullRequestResolved:
    """Resolves package versions from Pipfile against PyPI"""

    client = None

    def __init__(self) -> None:
        """Initialize the resolver"""
        self.client = Github(GITHUB_TOKEN)

    def retrieve_merged_pull_requests(self, repository_configuration: dict) -> list[dict[str, str]]:
        """Retrieve the Pipfile from GitHub"""

        repository_statistics = []
        repository: str = f"{repository_configuration['org']}/{repository_configuration['name']}"

        repo = self.client.get_repo(repository)

        for pr in repo.get_pulls(
            state="closed", sort="created", direction="desc", base=repository_configuration["base"]
        ):
            if pr.created_at < datetime.now() - timedelta(days=DAYS_TO_REVIEW):
                break

            marked_ready_for_review: list[IssueEvent] = [
                issue for issue in pr.get_issue_events() if issue.event == "ready_for_review"
            ]

            active_review_at: datetime = None
            if len(marked_ready_for_review) > 0:
                active_review_at = marked_ready_for_review[0].created_at
            else:
                active_review_at = pr.created_at

            name: str = repo.name
            title: str = pr.title
            number: int = pr.number
            created_at: datetime = pr.created_at
            merged_at: datetime = pr.merged_at
            author: str = pr.user.login
            active_review_at: datetime = pr.created_at
            duration: str = humanize.naturaldelta((pr.merged_at or pr.closed_at) - active_review_at)

            if author == "dependabot[bot]":
                continue

            if merged_at is None:
                continue

            repository_statistics.append(
                {
                    "repository": name,
                    "title": title,
                    "number": number,
                    "created_at": created_at,
                    "ready_for_review_at": active_review_at,
                    "merged_at": merged_at,
                    "author": author,
                    "active_review_at": active_review_at,
                    "duration": duration,
                }
            )

        return repository_statistics
