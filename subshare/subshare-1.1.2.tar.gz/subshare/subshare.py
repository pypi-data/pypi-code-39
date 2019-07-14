#!/usr/bin/env python
# _____  _              _       _____       _    _  _
#|   __||_| _____  ___ | | _ _ |   __| _ _ | |_ | ||_| _____  ___
#|__   || ||     || . || || | ||__   || | || . || || ||     || -_|
#|_____||_||_|_|_||  _||_||_  ||_____||___||___||_||_||_|_|_||___|
#                 |_|     |___|

import json
from getpass import getuser
from os import path
from subprocess import run

import click
import pyperclip

from .haste import Post
from .screen import screenShot
from .shorten import Link
from .upload import File

########## Config ##########
u = getuser()
configFile = "/home/" + u + "/.subshare.conf"


def createConfig():
    createConfig = {
        "nextcloud_url": "",
        "nextcloud_dir": "",
        "nextcloud_username": "",
        "nextcloud_password": "",
        "use_polr": "true/false - NO QUOTES",
        "polr_url": "",
        "polr_api_key": "",
        "hastebin_url": "https://hastebin.com",
        "screenshot_save_dir": "/home/USERNAME/screenshots"
    }
    run(["touch", "~/subshare.conf"])
    with open(configFile, "w") as f:
        json.dump(createConfig, f, indent=4)


if not path.isfile(configFile):
    createConfig()
    print("Config file created at: ~/.subshare.conf")

else:
    with open(configFile, 'r', encoding="utf8") as f:
        config = json.load(f)

    nextcloud_url = config["nextcloud_url"]
    nextcloud_dir = config["nextcloud_dir"]
    nextcloud_username = config["nextcloud_username"]
    nextcloud_password = config["nextcloud_password"]
    use_polr = config["use_polr"]
    polr_url = config["polr_url"].upper()
    polr_api_key = config["polr_api_key"]
    hastebin_url = config["hastebin_url"]
    screenshot_save_dir = config["screenshot_save_dir"]

with open(configFile, 'r', encoding="utf8") as f:
    config = json.load(f)

nextcloud_url = config["nextcloud_url"]
nextcloud_dir = config["nextcloud_dir"]
nextcloud_username = config["nextcloud_username"]
nextcloud_password = config["nextcloud_password"]
use_polr = config["use_polr"]
polr_url = config["polr_url"]
polr_api_key = config["polr_api_key"]
hastebin_url = config["hastebin_url"]


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    pass


#####################################
#              Files                #
#####################################
@main.command()
@click.argument("f", help="The file to share to Nextcloud.")
def file(f):
    if use_polr is True:
        pyperclip.copy(Link(File(f, nextcloud_username, nextcloud_password,
                                 nextcloud_url, nextcloud_dir), polr_url, polr_api_key))
        click.echo("File uploaded to NextCloud\n" + pyperclip.paste())
    else:
        pyperclip.copy(File(f, nextcloud_username,
                            nextcloud_password, nextcloud_url, nextcloud_dir))
        click.echo("File uploaded to NextCloud\n" + pyperclip.paste())


#####################################
#           Screenshots             #
#####################################
@main.command()
@click.option("-t", required=False, default="fullscreen", type=click.Choice(["selection", "fullscreen"]), show_default=True, help="Takes a screenshot and shares to Nextcloud")
def screenshot(t):
    if t is "selection":
        if use_polr is True:
            pyperclip.copy(Link(File(screenShot(t, screenshot_save_dir), nextcloud_username,
                                     nextcloud_password, nextcloud_url, nextcloud_dir) + "/preview", polr_url, polr_api_key))
            run(["notify-send", "Screenshot Captured", "-t", "3000"])
            click.echo(
                "Screenshot region captured: Copied to clipboard\n" + pyperclip.paste())
        else:
            pyperclip.copy(File(screenShot(t, screenshot_save_dir), nextcloud_username,
                                nextcloud_password, nextcloud_url, nextcloud_dir) + "/preview")
            run(["notify-send", "Screenshot Captured", "-t", "3000"])
            click.echo(
                "Screenshot region captured: Copied to clipboard\n" + pyperclip.paste())
    else:
        if use_polr is True:
            pyperclip.copy(Link(File(screenShot(t, screenshot_save_dir), nextcloud_username,
                                     nextcloud_password, nextcloud_url, nextcloud_dir) + "/preview", polr_url, polr_api_key))
            run(["notify-send", "Screenshot Captured", "-t", "3000"])
            click.echo(
                "Screenshot captured: Copied to clipboard\n" + pyperclip.paste())
        else:
            pyperclip.copy(File(screenShot(t, screenshot_save_dir), nextcloud_username,
                                nextcloud_password, nextcloud_url, nextcloud_dir) + "/preview")
            run(["notify-send", "Screenshot Captured", "-t", "3000"])
            click.echo(
                "Screenshot captured: Copied to clipboard\n" + pyperclip.paste())


#####################################
#              Text                 #
#####################################
@main.command()
@click.argument("f", help="The file to paste to Hastebin")
def text(f):
    if use_polr is True:
        pyperclip.copy(Link(Post(f, hastebin_url), polr_url, polr_api_key))
        click.echo("Text uploaded to hastebin\n" + pyperclip.paste())
    else:
        pyperclip.copy(Post(f, hastebin_url))
        click.echo("Text uploaded to hastebin\n" + pyperclip.paste())


#####################################
#              Links                #
#####################################
@main.command()
@click.argument("f", help="The link to shorten.")
def link(f):
    if use_polr is True:
        pyperclip.copy(Link(f, polr_url, polr_api_key))
        click.echo("Link shortened\n" + pyperclip.paste())
    else:
        click.echo("Enable Polr from ~/.subshare.json to use Link Shortening")


if __name__ == '__main__':
    main()
