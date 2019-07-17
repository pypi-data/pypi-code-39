# Copyright 2017 Octobus <contact@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
"""help dealing with code source reformating

The extension provides a way to run code-formatting tools in a way that avoids
conflicts related to this formatting when merging/rebasing code across the
reformatting.

A new `format-source` command is provided, to apply code formatting tool on
some specific files. This information is recorded into the repository and
reused when merging. The client doing the merge needs the extension for this
logic to kick in.

Code formatting tools have to be registered in the configuration. The tool
"name" will be used to identify a specific command accross all repositories.
It is mapped to a command line that must output the formatted content on its
standard output.

For each tool a list of files affecting the result of the formatting can be
configured with the "configpaths" suboption, which is read and registered at
"hg format-source" time.  Any change in those files should trigger
reformatting.

Example::

    [format-source]
    json = python -m json.tool
    clang = clang-format -style=Mozilla
    clang:configpaths = .clang-format, .clang-format-ignore

We do not support specifying the mapping of tool name to tool command in the
repository itself for security reasons.

The formatting tools are given the input source code as stdin and should sends
back the results in stdout. This is the default behavior and it can be tweaked
by configuration::

    [format-source]
    clang = clang-format -style=Mozilla
    clang:mode = pipe

There is two possible values for the mode config knob:

    * "pipe": the source code will be provided for the formatter tool in stdin
      and the formatted code will be read from the formatter tool stdout.
    * "file": the formatter tool will be called with the filepath as argument
      and the formatted code will be read from the original file, this is
      often called inplace modification.

There is also configuration for input mode and output mode, the high-level
mode actually set both input mode and output mode to the same value if set:

Input mode values:

    * "pipe": the source code will be provided for the formatter tool in stdin.
    * "file": the formatter tool will be called with the filepath as argument.

Output mode values:

    * "pipe": the formatted code will be read from the formatter tool stdout.
    * "file": the formatted code will be read from the original file, this is
      often called inplace modification.

The code formatting information is tracked in a .hg-format-source file at the
root of the repository.

The format-source extension also tracks the version of the tool when the
initial `hg format-source` was done. For the officially supported tools, the
command that returns the tool version is already configured. For other tools,
it need to be manually configured as follow::

    [format-source]
    mytool = mytool --args
    mytool:version-command = mytool --version
    mytool:version-regex = (\\d\\.\\d\\.\\d)

Format-source will use the configured version-regex to extract the version
number from the output of the version command. The version-regex needs to have
at least one capturing group and format-source will use the first capturing
group matching value as version number.

You can force or disable formatter running during merge using the following config::

  [format-source]
  run-mode = auto # default behavior
  run-mode = on # always run when merging formatted file
  run-mode = off # rever run when merging formatted file

Warning: There is no special logic handling renames so moving files to a
directory not covered by the patterns used for the initial formatting will
likely fail.
"""

from __future__ import absolute_import

import inspect
import json
import os
import re
import subprocess
import tempfile

from mercurial import (
    commands,
    cmdutil,
    encoding,
    error,
    extensions,
    filemerge,
    match,
    merge,
    pycompat,
    localrepo,
    registrar,
    scmutil,
    util,
)


try:
    from mercurial.util import procutil

    procutil.shellquote

    from mercurial.utils import stringutil
    parsebool = stringutil.parsebool
except ImportError:
    procutil = util  # procutil was not split in <= 4.5
    parsebool = util.parsebool

from mercurial.i18n import _

__version__ = "0.4.0"
testedwith = "4.4 4.5 4.6 4.7 4.8 4.9 5.0"
minimumhgversion = "4.4"
buglink = "https://bitbucket.org/octobus/format-source/issues"

cmdtable = {}

command = registrar.command(cmdtable)

configtable = {}
configitem = registrar.configitem(configtable)
configitem("format-source", "run-mode", default="auto")
configitem("format-source", "^[^:]+$", default=None, generic=True)
configitem("format-source", "^[^:]+:configpaths$", default=None, generic=True)
configitem("format-source", "^[^:]*:mode$", default=None, generic=True)
configitem("format-source", "^[^:]*:mode.input$", default=None, generic=True)
configitem("format-source", "^[^:]*:mode.output$", default=None, generic=True)
configitem(
    "format-source", "^[^:]*:version-command$", default=None, generic=True
)
configitem(
    "format-source", "^[^:]*:version-regex$", default=None, generic=True
)

file_storage_path = ".hg-format-source"

# Default settings for common formatters
DEFAULT_IO_MODE = [
    (
        "clang-format",
        "clang-format -assume-filename=$HG_FILENAME",
        (
            ("mode", "pipe"),
            ("configpaths", ".clang-format, .clang-format-ignore"),
            ("version-command", "clang-format --version"),
            (
                "version_regex",
                "clang-format version (\\d+\\.\\d+\\.\\d+(?:-\\d+)?)",
            ),
        ),
    ),
    (
        "black",
        "black -q -",
        (
            ("mode", "pipe"),
            ("configpaths", "pyproject.toml"),
            ("version-command", "black --version"),
            ("version-regex", "black, version (\\d+\\.\\d+(?:\\w\\d+)?)"),
        ),
    ),
    (
        "yapf",
        "yapf",
        (
            ("mode", "pipe"),
            ("configpaths", ".style.yapf,setup.cfg"),
            ("version-command", "yapf --version"),
            ("version-regex", "yapf (\\d+\\.\\d+\\.\\d+)"),
        ),
    ),
    (
        "gofmt",
        "gofmt -e",
        (
            ("mode", "pipe"),
            ("version-command", "go version"),
            ("version-regex", "go version go(\\d+\\.\\d+\\.\\d+)"),
        ),
    ),
    (
        "rustfmt",
        "rustfmt",
        (
            ("mode", "pipe"),
            ("configpaths", "rustfmt.toml,.rustfmt.toml"),
            ("version-command", "rustfmt --version"),
            ("version-regex", "rustfmt (\\d\\.\\d\\.\\d-\\w+)"),
        ),
    ),
    (
        "prettier",
        "prettier --stdin-filepath $HG_FILENAME",
        (
            ("mode", "pipe"),
            (
                "configpaths",
                ",".join([".prettierrc",
                          "prettier.yaml",
                          ".prettier.yml",
                          ".prettier.json",
                          ".prettier.toml",
                          "prettier.config.js",
                          ".prettierrc.js",
                          "package.json",
                ]),
            ),
            ("version-command", "prettier --version"),
            ("version-regex", "(\\d\\.\\d\\.\\d)"),
        ),
    ),
]


if "uipathfn" in inspect.getargspec(cmdutil.add).args:
    def cmdutiladd(ui, repo, storage_matcher):
        uipathfn = scmutil.getuipathfn(repo, forcerelativevalue=True)
        cmdutil.add(ui, repo, storage_matcher, "", uipathfn, True)
else:
    # hg <=4.9 compat (broken from f8b18583049f)
    def cmdutiladd(ui, repo, storage_matcher):
        cmdutil.add(ui, repo, storage_matcher, "", True)


class ToolAbort(error.Abort):
    """ A custom exception raised when a tool is misconfigured or crashed
    """

@command(
    "debugformatsourcechange",
    [],
    _("BASE TOP"),
)
def cmd_debug_format_change(ui, repo, base, top):
    """report files whose formatting is detected as changed in a range of
    commit
    """
    old_ctx = scmutil.revsingle(repo, base)
    new_ctx = scmutil.revsingle(repo, top)
    pattern_formatting = formattedbetween(repo, old_ctx, new_ctx)
    files_formatting = _formattedfiles(repo, new_ctx, pattern_formatting)
    allfiles = []
    for tool, matcher in files_formatting.iteritems():
        for f in new_ctx:
            if matcher(f):
                allfiles.append((tool, f))
    allfiles.sort()
    for tool, f in allfiles:
        ui.write('[%s] %s\n' % (tool, f))

@command(
    "format-source",
    [
        (
            "",
            "extra-config-file",
            [],
            _("track additional config file"),
            _("CONFIG FILE"),
        ),
        (
            "",
            "current",
            False,
            _("run current formatting on working copy file"),
        )
    ]
    + commands.commitopts
    + commands.commitopts2,
    _("[TOOL FILES+|--current [FILES+]]"),
)
def cmd_format_source(ui, repo, tool=None, *pats, **opts):
    """format source file using a registered tools

    This command run TOOL on FILES and record this information in a commit to
    help with future merge.

    The actual command run for TOOL needs to be registered in the config. See
    :hg:`help -e formatsource` for details.
    """
    if repo.getcwd():
        msg = _("format-source must be run from repository root")
        hint = _("cd %s") % repo.root
        raise error.Abort(msg, hint=hint)

    current = opts['current']

    if current:
        pats = list(pats)
        if tool is not None:
            pats.insert(0, tool)
        return _apply_current(ui, repo, *pats, **opts)

    if tool is None:
        raise error.Abort(_('specifify either a tool or --current'))

    if not pats:
        raise error.Abort(_("no files specified"))

    for i, pattern in enumerate(pats):
        ptype = pattern.partition(":")[0]
        if not ptype:
            # make implicit glob patterns explicit
            ptype = "glob"
            pats[i] = "glob:%s" % pattern

    # lock the repo to make sure no content is changed
    with repo.wlock():
        # formating tool
        if " " in tool:
            raise error.Abort(_("tool name cannot contains space: '%s'") % tool)
        tool_config_files = repo.ui.configlist("format-source", "%s:configpaths" % tool)

        # Track additional config files
        for extra_config_file in opts["extra_config_file"]:
            # TODO show a warning in case the file is not tracked
            # TODO should we check if the file exists on disk?
            tool_config_files.append(extra_config_file)

        cmdutil.bailifchanged(repo)
        cmdutil.checkunfinished(repo, commit=True)
        wctx = repo[None]

        # make sure the tool is known
        shell_tool(repo.ui, tool, raise_on_missing=True)
        # files to be formatted
        matcher = rootedmatch(repo, wctx, pats)
        # perform actual formatting
        for filepath in wctx.matches(matcher):
            _format_filepath(repo, tool, wctx, filepath)

        # update the storage to mark formated file as formatted
        with repo.wvfs(file_storage_path, mode="ab") as storage:
            for pattern in pats:
                # XXX if pattern was relative, we need to reroot it from the
                # repository root. For now we constrainted the command to run
                # at the root of the repository.
                data = {
                    "tool": encoding.unifromlocal(tool),
                    "pattern": encoding.unifromlocal(pattern),
                }
                version = _get_tool_version(repo.ui, tool)
                if version is not None:
                    data["version"] = _get_tool_version(repo.ui, tool)
                if tool_config_files:
                    data["configpaths"] = [
                        encoding.unifromlocal(path) for path in tool_config_files
                    ]
                entry = json.dumps(data, sort_keys=True)
                assert "\n" not in entry
                storage.write("%s\n" % entry)

        if file_storage_path not in wctx:
            storage_matcher = scmutil.match(wctx, ["path:" + file_storage_path])
            cmdutiladd(ui, repo, storage_matcher)

        # commit the whole
        with repo.lock():
            commit_patterns = ["path:" + file_storage_path]
            commit_patterns.extend(pats)
            return commands._docommit(ui, repo, *commit_patterns, **opts)

def _apply_current(ui, repo, *pats, **opts):
    """Run current formatter definition on the working copy file"""
    wctx = repo[None]
    filesformatting = formatted(repo, wctx)

    m = None
    if pats:
        m = rootedmatch(repo, wctx, pats)

    # Iterate on each tracked file or selected files
    for tool, tool_pats in filesformatting.items():
        matcher = rootedmatch(repo, wctx, tool_pats)

        shell_tool(repo.ui, tool, raise_on_missing=True)

        for filepath in wctx.matches(matcher):

            # Check if the filepath is in the given paths
            if m is not None and not m(filepath):
                continue

            _format_filepath(
                repo,
                tool,
                wctx,
                filepath,
            )


def shell_tool(ui, tool, raise_on_missing=False):
    """ Return the shell command for the given formatter tool or abort
    """
    shell_tool = ui.config("format-source", tool)

    if not shell_tool and raise_on_missing:
        msg = _("unknow format tool: %s (no 'format-source.%s' config)")
        raise error.Abort(msg % (tool, tool))

    return shell_tool


def iomode(ui, tool):
    # Read the top-level configuration
    input_mode = None
    output_mode = None

    tool_mode = ui.config("format-source", "%s:mode" % tool)
    if tool_mode is not None:
        input_mode = tool_mode
        output_mode = tool_mode

    # Read the override, we cannot pass the default value as we support
    # Mercurial 4.4 and we need dynamic default for this
    override_input_mode = ui.config("format-source", "%s:mode.input" % tool)
    override_output_mode = ui.config("format-source", "%s:mode.output" % tool)

    if override_input_mode is not None:
        input_mode = override_input_mode

    if override_output_mode is not None:
        output_mode = override_output_mode

    return input_mode, output_mode


def system(cmd, environ=None, cwd=None, stdin=None):
    """ Reimplementation of Mercurial procutil.system (taken from Mercurial
    246b61bfdc2f) with separate streams for stdout and stderr
    """
    environ = environ.copy()
    environ = procutil.shellenviron(environ)
    if util.safehasattr(pycompat, "rapply") and util.safehasattr(
        procutil, "tonativestr"
    ):
        cwd = pycompat.rapply(procutil.tonativestr, cwd)
        environ = procutil.tonativeenv(environ)

    if stdin is None:
        stdin = subprocess.PIPE
    process = subprocess.Popen(
        procutil.quotecommand(cmd),
        shell=True,
        cwd=cwd,
        env=environ,
        close_fds=procutil.closefds,
        stdin=stdin,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    pout, perr = process.communicate()

    return process, pout, perr


def run_tools(
    ui, root, tool, cmd, filepath, filename, input_mode=None, output_mode=None
):
    """Run the a formatter tool on a specific file"""

    # Default mode values
    if input_mode is None:
        input_mode = "file"

    if output_mode is None:
        output_mode = "pipe"

    env = encoding.environ.copy()
    env["HG_FILENAME"] = filename

    format_cmd = cmd
    if input_mode == "file":
        format_cmd = "%s %s" % (cmd, procutil.shellquote(filepath))
    elif input_mode == "pipe":
        format_cmd = cmd
    else:
        errmsg = "Tool %s has an invalid input mode: %s"
        raise ToolAbort(errmsg % (tool, input_mode))

    ui.debug("running %s\n" % format_cmd)

    stdin = None
    try:
        if input_mode == "pipe":
            stdin = open(filepath)
        p, pout, perr = system(format_cmd, env, root, stdin=stdin)
    finally:
        if stdin is not None:
            stdin.close()

    if perr:
        for line in perr.splitlines():
            ui.debug("format-source: [%s] %s\n" % (tool, line))

    if p.returncode:
        errmsg = "%s: %s %s" % (
            tool,
            os.path.basename(format_cmd.split(None, 1)[0]),
            procutil.explainexit(p.returncode),
        )
        raise ToolAbort(errmsg)

    if output_mode == "pipe":
        return pout
    elif output_mode == "file":
        with open(filepath, "rb") as outfile:
            return outfile.read()
    else:
        errmsg = "Tool %s has an invalid output mode: %s"
        raise ToolAbort(errmsg % (tool, output_mode))


def touched(repo, old_ctx, new_ctx, paths):
    matcher = rootedmatch(repo, new_ctx, paths)
    if any(path in new_ctx for path in paths):
        status = old_ctx.status(other=new_ctx, match=matcher)
        return bool(status.modified or status.added)
    return False


def _format_filepath(repo, tool, wctx, filepath):
    """apply the given tool to the given filepath

    It will write the formatted result on disk
    """
    shell_tool_command = shell_tool(repo.ui, tool, raise_on_missing=True)
    input_mode, output_mode = iomode(repo.ui, tool)

    flags = wctx.flags(filepath)
    newcontent = run_tools(
        repo.ui,
        repo.root,
        tool,
        shell_tool_command,
        filepath,
        filepath,
        input_mode=input_mode,
        output_mode=output_mode,
    )

    if newcontent == "":
        # check if the file itself is empty
        if open(filepath).read(1):
            msg = _("tool %r failed to format file, no data returned: %s")
            raise error.Abort(msg % (tool, filepath))
    # XXX we could do the whole commit in memory
    with repo.wvfs(filepath, "wb") as formatted_file:
        formatted_file.write(newcontent)
    wctx.filectx(filepath).setflags("l" in flags, "x" in flags)


def _get_patterns(ctx):
    """read the pattern -> formatter data from a changesets

    Returns a set of lines, each line should be a JSON object.
    """
    if file_storage_path not in ctx:
        return set()
    raw_data = ctx[file_storage_path].data()
    return set(raw_data.splitlines())

def _parse_patterns(patterns):
    """return a dict with the formatting details"""
    for p in patterns:
        yield json.loads(p)

def _add_entries(mapping, entries):
    """update a mapping with entry"""
    for entry in entries:
        tool = encoding.unitolocal(entry["tool"])
        pattern = encoding.unitolocal(entry["pattern"])
        mapping.setdefault(tool, set()).add(pattern)

def formatted(repo, ctx):
    """retrieve the list of formatted patterns as of <ctx>

    return a {'tool': [patterns]} mapping
    """
    formatting = {}
    lines = _get_patterns(ctx)
    _add_entries(formatting, _parse_patterns(lines))
    return formatting

def formattedbetween(repo, old_ctx, new_ctx):
    """retrieve the list of formatted patterns between <old> and <new>

    return a {'tool': [patterns]} mapping
    """
    new_formatting = {}
    if touched(repo, old_ctx, new_ctx, [file_storage_path]):
        # quick and dirty line diffing
        # (the file is append only by contract)

        new_lines = _get_patterns(new_ctx)
        old_lines = set()
        if file_storage_path in old_ctx:
            old_lines = _get_patterns(old_ctx)
        new_lines -= old_lines
        _add_entries(new_formatting, _parse_patterns(new_lines))
    if file_storage_path in old_ctx:

        def configpathfilter(entry):
            if not entry.get("configpaths"):
                return False
            configpaths = [encoding.unitolocal(path) for path in entry["configpaths"]]
            return touched(repo, old_ctx, new_ctx, configpaths)

        entries = _parse_patterns(_get_patterns(old_ctx))
        _add_entries(new_formatting, (e for e in entries if configpathfilter(e)))
    return new_formatting


def allformatted(repo, local, other, ancestor):
    """return a mapping of formatting needed for all involved changeset
    """

    cachekey = (local.node, other.node(), ancestor.node())
    cached = getattr(repo, "_formatting_cache", {}).get(cachekey)

    if cached is not None:
        return cached

    runmode = repo.ui.config("format-source", "run-mode")

    if runmode == 'auto':
        local_formating = formattedbetween(repo, ancestor, local)
        other_formating = formattedbetween(repo, ancestor, other)
    elif parsebool(runmode):
        local_formating = formatted(repo, local)
        other_formating = formatted(repo, other)
    else:
        local_formating = {}
        other_formating = {}

    full_formating = local_formating.copy()
    for key, value in other_formating.iteritems():
        if key in local_formating:
            value = value | local_formating[key]
        full_formating[key] = value

    all = [
        (local, local_formating),
        (other, other_formating),
        (ancestor, full_formating),
    ]
    final = []
    for ctx, formatting in all:
        filesformatting = _formattedfiles(repo, ctx, formatting)
        final.append(filesformatting)

    final = tuple(final)
    getattr(repo, "_formatting_cache", {})[cachekey] = final
    return final

def _formattedfiles(repo, ctx, patterns_formatting):
    """Turn patterns based formatting information into concrete files"""
    files_formatting = {}
    for tool, patterns in patterns_formatting.iteritems():
        files_formatting[tool] = rootedmatch(repo, ctx, patterns)
    return files_formatting


def rootedmatch(repo, ctx, patterns):
    """match patterns agains the root of a repository"""
    # rework of basectx.match to ignore current working directory
    orig = match.match
    try:
        def _rootedmatch(root, cwd, *args, **kwargs):
            return orig(root, root, *args, **kwargs)
        match.match = _rootedmatch

        # Only a case insensitive filesystem needs magic to translate user input
        # to actual case in the filesystem.
        icasefs = not util.fscasesensitive(repo.root)
        return match.match(
            repo.root,
            repo.root,
            patterns,
            default="glob",
            auditor=repo.auditor,
            ctx=ctx,
            icasefs=icasefs,
        )
    finally:
        match.match = orig


def apply_formating(repo, formatting, fctx):
    """apply formatting to a file context (if applicable)

    only called during merging situation"""
    data = None
    for tool, matcher in sorted(formatting.items()):
        # matches?
        if matcher(fctx.path()):
            if data is None:
                data = fctx.data()

            shell_tool_command = shell_tool(repo.ui, tool, raise_on_missing=False)
            if not shell_tool_command:
                msg = _(
                    "format-source, no command defined for '%s',"
                    " skipping formating: '%s'\n"
                )
                msg %= (tool, fctx.path())
                repo.ui.warn(msg)
                continue

            input_mode, output_mode = iomode(repo.ui, tool)

            with tempfile.NamedTemporaryFile(mode="wb") as f:
                olddata = data
                f.write(data)
                f.flush()
                try:
                    data = run_tools(
                        repo.ui,
                        repo.root,
                        tool,
                        shell_tool_command,
                        f.name,
                        fctx.path(),
                        input_mode=input_mode,
                        output_mode=output_mode,
                    )
                except ToolAbort as exc:
                    # Do not abort in those cases
                    msg = _(
                        "format-source: could not help with the merge of %s\n"
                        'format-source:   running tool "%s" failed: %s\n'
                    )
                    msg %= (fctx._path, tool, exc)
                    repo.ui.warn(msg)

                if olddata and not data:
                    msg = _(
                        'format-source: tool "%r" returned empty string,'
                        " skipping formatting for file %r\n"
                    )
                    msg %= (tool, fctx.path())

                    repo.ui.warn(msg)
                    data = None

    if data is not None:
        fctx.data = lambda: data


def wrap_filemerge44(
    origfunc, premerge, repo, wctx, mynode, orig, fcd, fco, fca, *args, **kwargs
):
    """wrap the file merge logic to apply formatting on files that needs them"""
    _update_filemerge_content(repo, fcd, fco, fca)
    return origfunc(premerge, repo, wctx, mynode, orig, fcd, fco, fca, *args, **kwargs)


def wrap_filemerge43(
    origfunc, premerge, repo, mynode, orig, fcd, fco, fca, *args, **kwargs
):
    """wrap the file merge logic to apply formatting on files that needs them"""
    _update_filemerge_content(repo, fcd, fco, fca)
    return origfunc(premerge, repo, mynode, orig, fcd, fco, fca, *args, **kwargs)


def _update_filemerge_content(repo, fcd, fco, fca):
    if fcd.isabsent() or fco.isabsent() or fca.isabsent():
        return
    local = fcd._changectx
    other = fco._changectx
    ances = fca._changectx
    all = allformatted(repo, local, other, ances)
    local_formating, other_formating, full_formating = all
    apply_formating(repo, local_formating, fco)
    apply_formating(repo, other_formating, fcd)
    apply_formating(repo, full_formating, fca)

    if "data" in vars(fcd):  # XXX hacky way to check if data overwritten
        file_path = repo.wvfs.join(fcd.path())
        with open(file_path, "wb") as local_file:
            local_file.write(fcd.data())


def wrap_update(orig, repo, *args, **kwargs):
    """install the formatting cache"""
    repo._formatting_cache = {}
    try:
        return orig(repo, *args, **kwargs)
    finally:
        del repo._formatting_cache


def uisetup(ui):
    pre44hg = filemerge._filemerge.__code__.co_argcount < 9
    if pre44hg:
        extensions.wrapfunction(filemerge, "_filemerge", wrap_filemerge43)
    else:
        extensions.wrapfunction(filemerge, "_filemerge", wrap_filemerge44)
    extensions.wrapfunction(merge, "update", wrap_update)


def reposetup(ui, repo):
    if not isinstance(repo, localrepo.localrepository):
        return

    # Update the config in reposetup as the ui object passed in uisetup is
    # copied without the config set by ui.setupconfig
    for tool_name, tool_command, tool_config in DEFAULT_IO_MODE:
        # Don't overwrite the user-defined config
        if ui.hasconfig("format-source", tool_name):
            continue

        ui.setconfig("format-source", tool_name, tool_command)

        for config_name, config_value in tool_config:
            config_key = "%s:%s" % (tool_name, config_name)
            ui.setconfig("format-source", config_key, config_value)


def _get_tool_version(ui, tool):
    """returns the version of the tool using on the command configured for it
    """
    version_command = ui.config("format-source", "%s:version-command" % tool)
    version_regex = ui.config("format-source", "%s:version-regex" % tool)

    if not version_command:
        return None

    # Try executing the command
    p, pout, perr = system(version_command, environ={})
    if p.returncode:
        msg = "Version command %r for tool %r exited with %r\n"
        ui.warn(msg % (version_command, tool, p.returncode))
        return None

    result = pout.strip()

    if version_regex:
        match = re.search(version_regex, pout.strip())
        if match:
            try:
                result = match.group(1)
            except IndexError:
                # The configured regex might not have any capturing group
                pass

    return result
