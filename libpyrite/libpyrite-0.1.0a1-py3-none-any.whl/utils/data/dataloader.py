from collections import deque
import os
import sys


class _ClassDirectoryTree:
    def __init__(self, root):
        if root.endswith("/"):
            root = root[:-1]
        self.root = _TreeNode(root)

    def add(self, path, class_dir, missing_ok=True):
        subset = path.replace(self.root.name, "")
        parts = [p for p in subset.split(os.path.sep) if p]

        node = self.root
        for part in parts:
            if missing_ok:
                node = node.put_if_absent(part)
            else:
                node = node.get_child(part)
        node.add_child(class_dir)

    def generate_indices(self):
        nodes_to_explore = deque([self.root])
        while nodes_to_explore:
            current = nodes_to_explore.popleft()
            children = sorted(current.children, key=lambda c: c.name)
            for i, c in enumerate(children):
                c.key = i
            nodes_to_explore.extend(children)

    def get_classes_from_path(self, path):
        subset = path.replace(self.root.name, "")
        parts = [p for p in subset.split(os.path.sep) if p]

        class_names = []
        class_indices = []

        node = self.root
        for part in parts:
            node = node.get_child(part)
            class_names.append(node.name)
            class_indices.append(node.key)

        return class_names, class_indices

    def to_dict(self):
        root_dict = {"children": {}}

        nodes_to_explore = deque([(self.root, root_dict)])
        while nodes_to_explore:
            node, d = nodes_to_explore.popleft()
            children = sorted(node.children, key=lambda c: c.name)
            for c in children:
                d["children"][c.name] = {"key": c.key, "children": {}}
            nodes_to_explore.extend([(c, d["children"][c.name]) for c in children])

        return root_dict["children"]


class _TreeNode:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.key = None
        self._children = {}

    def __contains__(self, key):
        return key in self._children

    def __getitem__(self, key):
        return self._children[key]

    def __repr__(self):
        return "_TreeNode(name={!r}, parent={!r})".format(self.name, self.parent)

    def __str__(self):
        return "_TreeNode: name={}, key={}\n\tparent={}\n\tchildren={}".format(
            self.name,
            self.key,
            self.parent.name if self.parent else None,
            sorted(self._children.keys()),
        )

    @property
    def children(self):
        return list(self._children.values())

    @property
    def siblings(self):
        return list(node for node in self.parent.children if node.name != self.name)

    def get_child(self, name, default=None):
        return self._children.get(name, default)

    def add_child(self, name):
        if name not in self._children:
            self._children[name] = _TreeNode(name, self)

    def put_if_absent(self, name):
        node = self.get_child(name)
        if node is None:
            node = _TreeNode(name, self)
            self._children[name] = node
        return node

    def remove_child(self, name):
        del self._children[name]

    def is_leaf(self):
        return len(self.children) == 0


class HierarchicalDatasetFolder:
    def __init__(self, root, loader, extensions, transform=None, target_transform=None):
        class_tree = self._find_classes(root, extensions)
        samples = _make_hierarchical_dataset(class_tree, extensions)
        if not samples:
            raise RuntimeError(
                "Found 0 files in subfolders of: {}\nSupported extensions are: {}".format(
                    root, ", ".join(extensions)
                )
            )

        self.loader = loader
        self.extensions = extensions
        self.class_tree = class_tree.to_dict()
        self.samples = samples
        self.targets = [s[1] for s in samples]
        self.transform = transform
        self.target_transform = target_transform

    def _find_classes(self, root, extensions):
        # Build up the directory tree structure
        tree = _ClassDirectoryTree(root)
        for current_dir, dirs, files in sorted(os.walk(root)):
            if files and dirs:
                if any([has_file_allowed_extension(f, extensions) for f in files]):
                    raise ValueError(
                        "All files must be must be leave nodes in the hierarchy"
                    )

            if dirs:
                for d in sorted(dirs):
                    tree.add(current_dir, d)
        tree.generate_indices()
        return tree

    def __getitem__(self, idx):
        path, targets = self.samples[idx]
        sample = self.loader(path)

        if self.transform is not None:
            sample = self.transform(sample)

        if self.target_transform is not None:
            targets = self.target_transform(targets)

        return sample, targets

    def __len__(self):
        return len(self.samples)


def has_file_allowed_extension(filename, extensions):
    filename = filename.lower()
    return any(filename.endswith(ext) for ext in extensions)


def _make_hierarchical_dataset(class_tree, extensions):
    root_dir = class_tree.root.name
    samples = []

    for current_dir, dirs, files in sorted(os.walk(root_dir)):
        if files and dirs:
            if any([has_file_allowed_extension(f, extensions) for f in files]):
                raise ValueError(
                    "All files must be must be leave nodes in the hierarchy"
                )

        if files:
            for fname in sorted(files):
                if has_file_allowed_extension(fname, extensions):
                    _, class_indices = class_tree.get_classes_from_path(current_dir)
                    path = os.path.join(current_dir, fname)
                    samples.append((path, class_indices))

    return samples


__all__ = ["HierarchicalDatasetFolder"]
