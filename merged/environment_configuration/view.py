from dataclasses import dataclass

from rich.console import Console
from rich.table import Table

from merged import config


@dataclass
class EnvironmentConfigurationView:
    """Responsible for rendering a table of all dependencies grouped by service"""

    console: Console

    def __init__(self, console: Console) -> None:
        """Initialize the view"""

        self.console = console

    def render(self, show: bool) -> None:
        """Render the view"""

        configurations = [
            {
                "name": "GITHUB_TOKEN",
                "value": config.GITHUB_TOKEN if show else "".join("*" for _ in range(len(config.GITHUB_TOKEN))),
            },
            {"name": "GITHUB_USER", "value": config.GITHUB_USER},
            {"name": "GITHUB_URL", "value": config.GITHUB_URL},
            {
                "name": "DEPS_PATH_TO_CONFIG",
                "value": f"{config.DEPS_PATH_TO_CONFIG}",
            },
            {
                "name": "GITHUB_DEFAULT_PAGE_SIZE",
                "value": f"{config.GITHUB_DEFAULT_PAGE_SIZE}",
            },
        ]

        table = Table()
        table.add_column("Name", style="white", no_wrap=True)
        table.add_column("Value", style="cyan")

        for configuration in configurations:
            table.add_row(configuration["name"], configuration["value"])

        self.console.print(table)
