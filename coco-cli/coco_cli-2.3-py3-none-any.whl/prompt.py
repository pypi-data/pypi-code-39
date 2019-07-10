#!/usr/bin/env python3

import json
import subprocess
import re
import sys
from pathlib import Path
from string import Template

from bullet import Bullet, charDef, colors, keyhandler, utils

CHOICES_KEY = 'choices'
PROMPT_KEY = 'prompt'
REGEX_STRING = "\{(.+?)\}"
QUIT_KEY = 113  # ASCII value of 'q'


class CloseableBullet(Bullet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @keyhandler.register(QUIT_KEY)
    @keyhandler.register(charDef.ESC_KEY)
    @keyhandler.register(charDef.INTERRUPT_KEY)
    def force_quit(self):
        utils.moveCursorDown(len(self.choices) - self.pos)
        sys.exit()


class ConfigFile:
    def __init__(self, path):
        with open(path) as file:
            configs = json.load(file)

        self.choices = configs[CHOICES_KEY]
        self.prompt = configs[PROMPT_KEY]


def fetch_args(arguments):
    args = list()
    print("\n")
    for arg in arguments:
        args.append(input(f"{arg}: "))
    return args


def run_shell_command(cmd):
    return subprocess.run(cmd.split(" "))


def contains_variables(command: str) -> bool:
    return bool(re.search(REGEX_STRING, command))


def substitute_variables(command: str, variables: list, args: list) -> str:
    template = Template('{$variable}')

    for variable, arg in zip(variables, args):
        command = command.replace(
            template.substitute(variable=variable), arg)

    return command


def run(config_path, *arguments):
    config = ConfigFile(config_path)

    prompt = config.prompt
    choices = list(config.choices.keys())
    bullet = '> '

    cli = CloseableBullet(prompt=prompt,
                          choices=choices,
                          bullet=bullet,
                          bullet_color=colors.foreground['green'],
                          word_on_switch=colors.bright(
                              colors.foreground['white']),
                          background_on_switch=colors.background['default'],
                          indent=1,
                          shift=1
                          )

    try:
        result = cli.launch()
    except KeyboardInterrupt:
        cli.force_quit()

    command = config.choices[result]

    if contains_variables(command):
        regex = re.compile(REGEX_STRING)
        variables = regex.findall(command)

        args = arguments if len(arguments) > 0 else fetch_args(variables)
        command = substitute_variables(command, variables, args)

    utils.cprint(f"\n\n{command}", color=colors.bright(
        colors.foreground['green']))
    run_shell_command(command)


if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2:])
