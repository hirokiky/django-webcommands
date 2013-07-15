from django import forms
from django.utils import six

from webcommands import utils as webcommands_utils


def field_for_option(option):
    if option.type == 'string':
        field = forms.CharField(label=str(option), max_length='255')
    elif option.type == 'int':
        field = forms.IntegerField(label=str(option))
    elif option.type == 'long':
        field = forms.IntegerField(label=str(option))
    elif option.type == 'choice':
        choices = zip(map(lambda x: x.upper(), option.choices), option.choices)
        field = forms.ChoiceField(label=str(option),
                                  choices=choices)
    else:
        field = forms.CharField(label=str(option), max_length=255)
    return field


class CommandFormMetaClass(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(CommandFormMetaClass, cls).__new__
        new_class = super_new(cls, name, bases, attrs)

        if 'command_class' in attrs:
            command_class = attrs['command_class']
            fields = {str(option): field_for_option(option)
                      for option in command_class.option_list}
        else:
            fields = {}

        new_class.base_fields = fields

        return new_class


class BaseCommandForm(forms.BaseForm):
    def execute(self):
        pass


class CommandForm(six.with_metaclass(CommandFormMetaClass, BaseCommandForm)):
    pass


def commandform_factory(command_class):
    """Factory to return CommandForm correspond to gotten command instance
    """
    command_name = command_class.__module__.rsplit('.', 1)[-1]
    command_name = webcommands_utils.funcname_to_classname(command_name)

    attrs = {'command_class': command_class}
    return type(command_name + str('CommandForm'), (CommandForm,), attrs)
