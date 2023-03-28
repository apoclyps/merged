import os
import pathlib
from datetime import datetime, timedelta

import humanize
from github import Github, IssueEvent
from polars import DataFrame

TOKEN = os.environ["GITHUB_TOKEN"]

g = Github(TOKEN)


def get_repository_statistics(repository_config: dict) -> list[dict[str, str]]:
    repository_statistics = []

    repository: str = f"{repository_config['org']}/{repository_config['name']}"

    repo = g.get_repo(repository)

    for pr in repo.get_pulls(state="closed", sort="created", direction="desc", base=repository_config["base"]):
        if pr.created_at < datetime.now() - timedelta(days=14):
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
                "name": name,
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


def build_dataframe(repository_statistics: list[dict[str, str]]) -> DataFrame:
    pull_request_repositories = []
    pull_request_titles = []
    pull_request_numbers = []
    pull_request_created_ats = []
    pull_request_ready_for_review_at = []
    pull_request_merged_ats = []
    pull_request_durations = []
    pull_request_authors = []

    for repository in repository_statistics:
        pull_request_repositories.append(repository["name"])
        pull_request_titles.append(repository["title"])
        pull_request_numbers.append(repository["number"])
        pull_request_created_ats.append(repository["created_at"])
        pull_request_ready_for_review_at.append(repository["ready_for_review_at"])
        pull_request_merged_ats.append(repository["merged_at"])
        pull_request_authors.append(repository["author"])
        pull_request_durations.append(repository["duration"])

    data: dict = {
        "Repository": pull_request_repositories,
        "Number": pull_request_numbers,
        "Title": pull_request_titles,
        "Author": pull_request_authors,
        "Created At": pull_request_created_ats,
        "Ready For Review At": pull_request_ready_for_review_at,
        "Merged At": pull_request_merged_ats,
        "Duration": pull_request_durations,
    }

    dataframe: DataFrame = DataFrame(data)

    return dataframe


def output_dataframe(dataframe: DataFrame) -> None:
    print(dataframe)

    path: pathlib.Path = "durations.csv"
    dataframe.write_csv(path, separator=",")


if __name__ == "__main__":
    repository_configurations = [
        {"org": "slicelife", "name": "ros-service", "base": "master"},
        {"org": "slicelife", "name": "third-party-orders-service", "base": "main"},
        # {"org": "slicelife", "name": "owners-portal-analytics-service", "base": "main"},
    ]

    repository_statistics = []

    for repository_config in repository_configurations:
        print(f"Processing {repository_config['name']}")
        repository_statistics += get_repository_statistics(repository_config=repository_config)

    print("Building dataframe")
    dataframe = build_dataframe(repository_statistics=repository_statistics)
    output_dataframe(dataframe)
