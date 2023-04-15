from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any

from rich.console import Console
from rich.table import Table

from merged.config import GITHUB_BRANCH, GITHUB_ORG, GITHUB_REPOSITORY
from merged.pull_requests.resolver import MergedPullRequestResolved


@dataclass
class MergedView:
    """Responsible for rendering a table of all dependencies grouped by service"""

    console: Console
    merged_pull_requests_by_service: dict
    resolver: MergedPullRequestResolved

    def __init__(self, console: Console) -> None:
        """Initialize the view"""

        self.merged_pull_requests_by_service = {}
        self.console = console
        self.resolver = MergedPullRequestResolved()

    def _retrieve(self, repository_configuration: dict) -> dict:
        merged_pull_requests_by_service: dict = {}

        repository_configuration = {"org": GITHUB_ORG, "name": GITHUB_REPOSITORY, "base": GITHUB_BRANCH}

        service: str = f"{repository_configuration['org']}/{repository_configuration['name']}"
        merged_pull_requests_by_service[service] = self.resolver.retrieve_merged_pull_requests(
            repository_configuration=repository_configuration
        )

        return merged_pull_requests_by_service

    def render(self) -> None:
        """Render the view"""

        with ThreadPoolExecutor(max_workers=1) as executor:
            merged_pull_requests_by_services: list[dict] = list(executor.map(self._retrieve, GITHUB_REPOSITORY))

        for merged_pull_requests_by_service in merged_pull_requests_by_services:
            if merged_pull_requests_by_service:
                self.merged_pull_requests_by_service = (
                    self.merged_pull_requests_by_service | merged_pull_requests_by_service
                )

        if self.merged_pull_requests_by_service:
            for service_name, pull_requests in self.merged_pull_requests_by_service.items():
                table = self.render_merged(
                    service_name=service_name,
                    pull_requests=pull_requests,
                )
                self.console.print(table, justify="center")

        self.console.print("No pull requests found")

    def render_merged(self, service_name: str, pull_requests: list[dict[Any, Any]]) -> Table:
        """Render the service dependencies"""
        table: Table = Table(title=service_name, title_style="bold white", title_justify="center")

        table.add_column("Repository", style="white", no_wrap=True)
        table.add_column("Number", style="white")
        table.add_column("Title", style="white")
        table.add_column("Author", style="white")
        table.add_column("Ready to Review", style="white")
        table.add_column("Merged At", style="white")
        table.add_column("Duration", style="white")

        for pull_request in pull_requests:
            repository: str = pull_request["repository"]
            number: str = pull_request["number"]
            title: str = pull_request["title"]
            author: str = pull_request["author"]
            ready_for_review_at: str = pull_request["ready_for_review_at"]
            merged_at: str = pull_request["merged_at"]
            duration: str = pull_request["duration"]

            if "hour" in duration or "minute" in duration:
                duration = f"[green]{duration}[/green]"
            if "a day" in duration:
                duration = f"[yellow]{duration}[/yellow]"
            elif "days" in duration:
                duration = f"[red]{duration}[/red]"

            table.add_row(
                repository,
                number,
                title,
                author,
                ready_for_review_at,
                merged_at,
                duration,
            )

        return table
