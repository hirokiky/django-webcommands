from webcommands.forms import CommandForm
from webcommands.tests.app.management.commands.app_command import Command


class AppCommandForm(CommandForm):
    command_class = Command
