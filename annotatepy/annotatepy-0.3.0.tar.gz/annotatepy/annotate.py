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
        return definition.full_name or ""
    except Exception:
        # TODO: handle this, explore why it happens, report upstream
        return ""


def annotate_node(script, node, rel_path, project_root):
    str_node = f"{rel_path}:{node.line} `{node.name}`"

    script._pos = node.line, node.column
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


def annotate_file(path, rel_path, project_root):
    with open(path, "r") as f:
        source = f.read()

    script = jedi.Script(source, path=path)
    for name in jedi.names(source, definitions=True, references=True, all_scopes=True):
        annotation = annotate_node(script, name, rel_path, project_root)
        if annotation:
            yield annotation


def generate_annotations(project_root, code_paths):
    logger.info(f"Project root: {project_root}")

    annotations = {}
    total_count = 0
    total_start = datetime.now()

    for path in sorted(get_python_files(code_paths)):
        blob_id = get_blob_id(path)
        if not blob_id:
            continue

        rel_path = os.path.relpath(path, project_root)
        start = datetime.now()

        file_annotations = list(annotate_file(path, rel_path, project_root))
        count = len(file_annotations)
        duration = (datetime.now() - start).total_seconds()
        logger.info(f"{rel_path}: {count} annotations, {duration:.2f}s")

        annotations[blob_id] = file_annotations
        total_count += count

    total_duration = (datetime.now() - total_start).total_seconds()
    logger.info(f"Done. Generated {total_count} annotations in {total_duration:.2f}s")

    return annotations
