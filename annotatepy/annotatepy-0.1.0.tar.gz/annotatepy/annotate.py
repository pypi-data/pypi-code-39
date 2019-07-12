import ast
import jedi
import os
import subprocess
import logging
import parso

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


class AnnotatingVisitor(ast.NodeVisitor):
    def __init__(self, source, path, project_root):
        self.source = source
        self.path = path
        self.project_root = project_root
        self.annotations = []

    def annotate_Call(self, node):
        # Currently only annotate function calls
        if not isinstance(node.func, ast.Name):
            return

        script = jedi.Script(
            self.source,
            node.lineno,
            node.col_offset,
            self.path,
        )

        definitions = script.goto_definitions()
        if not definitions:
            return

        definition = definitions[0]

        # Skip builtin functions
        if definition.module_name == 'builtins':
            return

        # Only link to functions withing the project
        if not (
            definition.module_path and
            definition.module_path.startswith(self.project_root)
        ):
            return

        to_path = os.path.relpath(definition.module_path, self.project_root)
        to_link = f"{to_path}#L{definition.line}"

        self.annotations.append({
            "type": "link",
            "lineno": node.lineno,
            "colno": node.col_offset,
            "len": len(node.func.id),
            "to": to_link,
            "title": definition.full_name,
        })

    def visit_Call(self, node):
        # self.annotate_Call(node)
        self.generic_visit(node)

    def visit_Name(self, node):
        print(node.__dict__)
        # self.annotate_Call(node)
        self.generic_visit(node)


def visit(node):
    if not isinstance(node, parso.python.tree.Name):
        return
    import pudb; pu.db
    print(node)


def walk(node, fn):
    fn(node)
    if hasattr(node, "children"):
        for child in node.children:
            walk(child, fn)


def generate_annotations(project_root, code_paths):
    annotations = {}

    for path in sorted(get_python_files(code_paths)):
        with open(path, "r") as f:
            source = f.read()

        node = parso.parse(source)
        walk(node, visit)


        # tree = ast.parse(source, path)

        # blob_id = get_blob_id(path)
        # if not blob_id:
        #     continue

        # logger.info(f"Processing: {path}")

        # visitor = AnnotatingVisitor(source, path, project_root)
        # visitor.visit(tree)

        # if visitor.annotations:
        #     annotations[blob_id] = visitor.annotations

    return annotations
