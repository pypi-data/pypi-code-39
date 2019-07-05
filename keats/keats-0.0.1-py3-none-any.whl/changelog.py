import datetime
from os.path import isfile, join, abspath, dirname, isdir
from os import mkdir, remove
import json

from collections import OrderedDict


ENTRY_TEMPLATE = """
## {version}

**{date}**
{description}

{changes}
"""


def new_entry(d, changes):
    now = datetime.datetime.now()
    return {"description": d, "date": now.isoformat(), "changes": changes}


def to_markdown(data, title=""):
    if not title:
        s = "# change log"
    else:
        s = "# {} change log".format(title)

    entries = []
    for k, d in data.items():
        changes = "\n".join([" - " + c for c in d["changes"]])
        entry = ENTRY_TEMPLATE.format(
            version=k, date=d["date"], description=d["description"], changes=changes
        )
        entries.append(entry)
    s += "\n".join(entries)
    return s


def load(changelogpath):
    if isfile(changelogpath):
        with open(changelogpath, "r") as f:
            text = f.read()
            if text.strip() == "":
                changelog = []
            else:
                changelog = json.loads(text)
    else:
        changelog = {}

    sorted_entries = sorted(
        [(k, v) for k, v in changelog.items()], key=lambda x: x[1]["date"], reverse=True
    )
    return OrderedDict(sorted_entries)


def update(version, description, changes, changelogpath):
    changelog = load(changelogpath)

    if version in changelog:
        entry = changelog[version]
        entry["description"] = description

        now = datetime.datetime.now()
        entry["date"] = now.isoformat()
        unique_changes = []
        for e in entry["changes"] + changes:
            if e not in unique_changes:
                unique_changes.append(e)
        entry["changes"] = unique_changes
    else:
        entry = new_entry(description, changes)
    changelog[version] = entry
    with open(changelogpath, "w") as f:
        json.dump(changelog, f, indent=2)


def save_to_markdown(changelogpath, path, title=""):
    with open(path, "w") as f:
        f.write(to_markdown(load(changelogpath), title=title))


def update_changelog_interactive(version, changelogpath, markdownpath, title=""):
    description = input("Add a description: ")
    change_input = None
    changes = []
    while change_input != "":
        if change_input is not None:
            changes.append(change_input)
        change_input = input("List a change (ENTER to finish): ").strip()
    update(version, description, changes, changelogpath)
    save_to_markdown(changelogpath, markdownpath, title=title)


class ChangeLog(object):
    def __init__(self, keats):
        self._keats = keats
        log_dir = join(keats._directory, ".keats")
        if not isdir(log_dir):
            mkdir(log_dir)
        self._directory = log_dir

    def _json(self):
        return join(self._directory, "changelog.json")

    def _markdown(self):
        return join(self._directory, "changelog.md")

    def up(self):
        save_to_markdown(self._json(), self._markdown())

    def clear(self):
        if isfile(self._json()):
            remove(self._json())
        if isfile(self._markdown()):
            remove(self._markdown())

    def add(self):
        update_changelog_interactive(
            self._keats.version(), self._json(), self._markdown(), self._keats.package()
        )
