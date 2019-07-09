import os
import errno

class FileManager(object):
    def __init__(self):
        super(FileManager, self).__init__()
        self.managed_files = {}

    def manage(self, path, contents):
        self.managed_files[path] = {
            "mtime" : os.path.getmtime(path),
            "digest": self.digest(contents)
        }

    def read(self, path):
        with open(path, 'r') as f:
            return f.read()

    def digest(self, contents):
        return hash(contents)

    def mkdir_p(self, path):
        if path == "" or os.path.exists(path):
            return
        os.makedirs(path)

    def file_exists(self, path):
        return os.path.exists(path)

    def same_contents(self, path, contents):
        return self.read(path) == contents

    def save(self, path, contents):
        self.mkdir_p(os.path.dirname(path))
        with open(path, "w") as file:
            file.write(contents)
        self.manage(path, contents)

    def file_is_managed(self, path):
        return path in self.managed_files.keys()

    def is_file_in_sync(self, path):
        if not self.file_is_managed(path):
            return False
        managed_file = self.managed_files[path]
        if managed_file["mtime"] == os.path.getmtime(path):
            return True
        return managed_file["digest"] == self.digest(self.read(path))

    def is_new_content(self, path, current_contents):
        managed_file = self.managed_files[path]
        return managed_file["digest"] != self.digest(current_contents)

    def is_file_in_sync_new_content(self, path, current_contents):
        return self.file_exists(path) and \
               self.is_file_in_sync(path) and \
               self.is_new_content(path, current_contents)

    def is_file_in_sync_unchanged_content(self, path, current_contents):
        return self.file_exists(path) and \
               self.is_file_in_sync(path) and \
               not self.is_new_content(path, current_contents)

    def is_new_file(self, path):
        return not self.file_is_managed(path) and \
               not self.file_exists(path)

    def is_file_exists_with_same_contents(self, path, current_contents):
        return not self.file_is_managed(path) and \
               self.file_exists(path) and \
               self.same_contents(path, current_contents)

    def is_overwrite_existing_file(self, path, current_contents):
        return not self.file_is_managed(path) and \
               self.file_exists(path) and \
               not self.same_contents(path, current_contents)

    def is_file_was_changed_by_another_process(self, path, current_contents):
        return self.file_is_managed(path) and \
               self.file_exists(path) and \
               not self.is_file_in_sync(path)

    def is_managed_file_was_deleted(self, path):
        return self.file_is_managed(path) and \
               not self.file_exists(path)

    def is_file_was_deleted(self, path):
        return not self.file_exists(path)

    def is_unmanaged_file_exists(self, path):
        return not self.file_is_managed(path) and \
               self.file_exists(path)

    def get_initial_state(self, path, current_contents):
        if self.is_file_in_sync_new_content(path, current_contents): return "In sync, new content"
        if self.is_file_in_sync_unchanged_content(path, current_contents): return "In sync, unchanged content"
        if self.is_new_file(path): return "New file"
        if self.is_file_exists_with_same_contents(path, current_contents): return "File exists with same contents"
        if self.is_overwrite_existing_file(path, current_contents): return "File exists with different contents"
        if self.is_file_was_changed_by_another_process(path, current_contents): return "File was changed by another process"
        if self.is_managed_file_was_deleted(path): return "File was deleted by another process"
        raise Exception("Unknown State")

    def get_state_change(self, path, current_contents):
        if self.is_file_in_sync_unchanged_content(path, current_contents): return "In sync, unchanged content"
        if self.is_file_was_changed_by_another_process(path, current_contents): return "File was changed by another process"
        if self.is_file_was_deleted(path): return "File was deleted by another process"
        if self.is_unmanaged_file_exists(path): return "File exists at this path"
