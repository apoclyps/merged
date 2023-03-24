import click
from rich.console import Console

from merged.environment_configuration.view import EnvironmentConfigurationView

from ..version import __version__

CONTEXT_SETTINGS: dict[str, list[str]] = {"help_option_names": ["-h", "--help"]}


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__, "-v", "--version", message="version %(version)s")
def cli() -> None:
    """Merged - A terminal UI Dashboard for monitoring dependencies across multiple repositories.\n

    For feature requests or bug reports: https://github.com/apoclyps/merged/issues
    """


@cli.command(help="Show the current configuration used by Merged")
@click.option("-show", "--show/--hide", default=False, is_flag=True)
def config(show: bool) -> None:
    """
    Command:\n
        merged config
    Usage:\n
        merged config --show \n
        merged config --hide \n
    """
    console = Console()
    EnvironmentConfigurationView(console=console).render(show=show)


def main() -> None:
    """Entry point to CLI"""
    cli()
