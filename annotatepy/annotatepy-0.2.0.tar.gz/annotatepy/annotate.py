import jedi
import logging
import os
import subprocess

from datetime import datetime


logger = logging.getLogger("annotatepy")


def get_python_files(paths):
    for path in paths:
        if os.path.isfile(path) and path.endswith(".py"):
            yield path
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith(".py"):
                        yield os.path.join(root, file)


def get_blob_id(path):
    res = subprocess.run(
        ["git", "ls-tree", "-r", "HEAD", path], stdout=subprocess.PIPE)
    stdout = res.stdout.decode()
    if stdout:
        return stdout.split()[2]


def def_title(definition):
    try:
        if definition.full_name:
            return definition.full_name
    except Exception:
        # TODO: handle this, explore why it happens, report upstream
        pass

    return ""


def annotate_node(node, source, path, project_root):
    rel_path = os.path.relpath(path, project_root)
    str_node = f"{rel_path}:{node.line} `{node.name}`"

    script = jedi.Script(source, node.line, node.column, path)
    definitions = script.goto_definitions()
    if not definitions:
        logger.debug(f"{str_node} skipped (no definition)")
        return
    definition = definitions[0]

    if definition.module_name == 'builtins':
        # TODO: For Python builtin functions link to docs
        logger.debug(f"{str_node} skipped (builtin)")
        return None

    if not definition.module_path:
        # TODO: handle this
        logger.debug(f"{str_node} skipped (no module_path)")
        return None

    # Don't annotate instances
    if definition.type == "instance":
        # TODO: this may skip some things that should be annotated
        logger.debug(f"{str_node} skipped (instance)")
        return None

    # Skip definitions outside of the project root
    if not definition.module_path.startswith(project_root):
        logger.debug(f"{str_node} skipped (outside of project root)")
        return None

    # Skip self-references
    if node.line == definition.line and node.column == definition.column:
        logger.debug(f"{str_node} skipped (self-reference)")
        return None

    to_link = os.path.relpath(definition.module_path, project_root)
    if definition.type != "module":
        to_link += f"#L{definition.line}"

    logger.debug(f"{str_node} => {to_link}")

    return {
        "type": "link",
        "lineno": node.line,
        "colno": node.column + 1,
        "len": len(node.name),
        "to": to_link,
        "title": def_title(definition),
    }


def annotate_file(path, project_root):
    with open(path, "r") as f:
        source = f.read()

    for name in jedi.names(source, definitions=True, references=True, all_scopes=True):
        annotation = annotate_node(name, source, path, project_root)
        if annotation:
            yield annotation


def generate_annotations(project_root, code_paths):
    annotations = {}

    for path in sorted(get_python_files(code_paths)):
        blob_id = get_blob_id(path)
        if not blob_id:
            continue

        rel_path = os.path.relpath(path, project_root)
        start = datetime.now()
        file_annotations = list(annotate_file(path, project_root))
        duration = datetime.now() - start
        logger.info(f"Annotated {rel_path}: {len(file_annotations)} annotations, {duration}")
        annotations[blob_id] = file_annotations

    return annotations
