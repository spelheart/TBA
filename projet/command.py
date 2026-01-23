# This file contains the Command class.
"""Module defining the Command class for game commands."""


class Command:  # pylint: disable=too-few-public-methods
    """Represents a user command and its metadata.

    Attributes:
        command_word (str): The command word.
        help_string (str): The help text shown in help.
        action (function): The function to execute.
        number_of_parameters (int): Expected parameter count.
        category (str): Display grouping for help.

    Examples:
        >>> from actions import go
        >>> cmd = Command("go", "Se déplacer", go, 1)
        >>> cmd.command_word
        'go'
    """

    # The constructor.
    def __init__(
        self,
        command_word,
        help_string,
        action,
        number_of_parameters,
        category="Autre",
    ):  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self.command_word = command_word
        self.help_string = help_string
        self.action = action
        self.number_of_parameters = number_of_parameters
        self.category = category

    # The string representation of the command.
    def __str__(self):
        return self.command_word + self.help_string
