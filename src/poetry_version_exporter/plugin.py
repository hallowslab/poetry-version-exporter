from pathlib import Path

from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.console_events import COMMAND
from cleo.events.event_dispatcher import EventDispatcher
from poetry.console.application import Application
from poetry.console.commands.env_command import EnvCommand
from poetry.plugins.application_plugin import ApplicationPlugin

from .exporter import export_version


class VersionExporterPlugin(ApplicationPlugin):
    def activate(self, application: Application) -> None:
        dispatcher = application.event_dispatcher
        assert dispatcher is not None
        dispatcher.add_listener(COMMAND, self.handle_command)  # type: ignore[arg-type]

    def handle_command(
        self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher
    ) -> None:
        command = event.command
        if not isinstance(command, EnvCommand):
            return
        # Only run on specific commands
        if command.name in ("install", "update", "build"):
            # configure your paths
            package_name = ""  # optional
            pyproject_path = Path("pyproject.toml")
            output_path = Path("_version.py")

            export_version(package_name, pyproject_path, output_path)
