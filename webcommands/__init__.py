import itertools

from django.conf import settings
from django.core.management import get_commands, load_command_class


def get_available_commands():
    available_commands = getattr(settings, 'WEBCOMMANDS_AVAILBLES', ['*'])

    if '*' in available_commands:
        return get_commands()
    else:
        return {k: v for k, v in get_commands() if k in available_commands}


def groupby_commands_dict(commands_dict):
    return {k: v for k, v in
            itertools.groupby(commands_dict.items(), key=lambda x: x[1])}


def fetch_command(command_name):
    try:
        app_name = get_available_commands()[command_name]
    except KeyError:
        return None
    klass = load_command_class(app_name, command_name)
    return klass
