#!/usr/bin/env python
# _____  _              _       _____       _    _  _
#|   __||_| _____  ___ | | _ _ |   __| _ _ | |_ | ||_| _____  ___
#|__   || ||     || . || || | ||__   || | || . || || ||     || -_|
#|_____||_||_|_|_||  _||_||_  ||_____||___||___||_||_||_|_|_||___|
#                 |_|     |___|

import click
import pyperclip
import json
from subprocess import run
from getpass import getuser
from os import path

import upload
import shorten
import haste
import screen


########## Config ##########
u = getuser()
configFile = "/home/" + u + "/" + "subshare.json"


def createConfig():
    createConfig = {
        "nc_url": "",
        "nc_dir": "",
        "nc_username": "",
        "nc_password": "",
        "polr_url": "",
        "polr_api_key": "",
        "hb_url": "",
        "screenshot_save_dir": ""
    }
    run(["touch", "~/subshare.json"])
    with open(configFile, "w") as f:
        json.dump(createConfig, f, indent=4)


if not path.isfile(configFile):
    createConfig()
    print("Config file created at: ~/.subshare.json")

else:
    with open(configFile, 'r', encoding="utf8") as f:
        config = json.load(f)

    nc_url = config["nc_url"]
    nc_dir = config["nc_dir"]
    nc_username = config["nc_username"]
    nc_password = config["nc_password"]
    polr_url = config["polr_url"]
    polr_api_key = config["polr_api_key"]
    hb_url = config["hb_url"]
    screenshot_save_dir = config["screenshot_save_dir"]

with open(configFile, 'r', encoding="utf8") as f:
    config = json.load(f)

nc_url = config["nc_url"]
nc_dir = config["nc_dir"]
nc_username = config["nc_username"]
nc_password = config["nc_password"]
polr_url = config["polr_url"]
polr_api_key = config["polr_api_key"]
hb_url = config["hb_url"]


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def subshare():
    pass

########## Files ##########


@subshare.command()
@click.option("-f", required=True, help="The file to share to Nextcloud.")
def file(f):
    pyperclip.copy(shorten.Link(upload.File(
        f, nc_username, nc_password, nc_url, nc_dir), polr_url, polr_api_key))
    click.echo("File uploaded to NextCloud\n" + pyperclip.paste())

########## Screenshots ##########


@subshare.command()
@click.option("-t", required=False, default="fullscreen", type=click.Choice(["selection", "fullscreen"]), show_default=True, help="Takes a screenshot and shares to Nextcloud")
def screenshot(t):
    if t is "selection":
        pyperclip.copy(shorten.Link(upload.File(screen.screenShot(t, screenshot_save_dir),
                                                nc_username, nc_password, nc_url, nc_dir) + "/preview", polr_url, polr_api_key))
        run(["notify-send", "Screenshot Captured", "-t", "3000"])
        click.echo(
            "Screenshot region captured: Copied to clipboard\n" + pyperclip.paste())
    else:
        pyperclip.copy(shorten.Link(upload.File(screen.screenShot(t, screenshot_save_dir),
                                                nc_username, nc_password, nc_url, nc_dir) + "/preview", polr_url, polr_api_key))
        run(["notify-send", "Screenshot Captured", "-t", "3000"])
        click.echo("Screenshot captured: Copied to clipboard\n" +
                   pyperclip.paste())

########## Text ##########


@subshare.command()
@click.option("-f", required=True, help="The file to paste to Hastebin")
def text(f):
    pyperclip.copy(shorten.Link(haste.Post(f, hb_url), polr_url, polr_api_key))
    click.echo("Text uploaded to hastebin\n" + pyperclip.paste())

########## Links ##########


@subshare.command()
@click.option("-f", required=True, help="The link to shorten.")
def link(f):
    pyperclip.copy(shorten.Link(f, polr_url, polr_api_key))
    click.echo("Link shortened\n" + pyperclip.paste())


if __name__ == '__main__':
    subshare()
