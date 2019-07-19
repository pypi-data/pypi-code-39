#
# Copyright (c) 2016, deepsense.io
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import subprocess

from neptune.internal.common.utils.system import IS_WINDOWS
from neptune.generated.swagger_client import GitCommit, GitHistoryParams


def get_git_version():
    try:
        with open(os.devnull, 'w') as devnull:
            return subprocess.check_output(['git', '--version'], stderr=devnull).decode("utf-8").strip()
    except OSError:
        return None
    except BaseException:
        return None


def get_git_info(experiment_ids):
    if not get_git_version():
        return None

    if IS_WINDOWS and r'GIT_PYTHON_GIT_EXECUTABLE' not in os.environ:
        os.environ[r'GIT_PYTHON_GIT_EXECUTABLE'] = os.popen("where git").read().strip()

    import git  # pylint:disable=wrong-import-position
    repository_path = os.getcwd()

    try:
        repo = git.Repo(repository_path, search_parent_directories=True)
        # TODO(mara): Get rid of NoSuchPathError. It is here only because of some unittests
        # feeds this code with non-existing paths, which should not be possible in normal case.
    except (git.InvalidGitRepositoryError, git.NoSuchPathError):
        return None

    git_dir = git.Git(repository_path)
    ids = git_dir.log('--pretty=%H').split('\n')
    commits = [repo.rev_parse(c) for c in ids]

    root_sha = commits[-1].hexsha

    commit_ids = set()
    commit_array = list()

    for commit in commits:
        if commit.hexsha in commit_ids:
            continue
        commit_ids.add(commit.hexsha)
        commit_array.append(
            GitCommit(
                commit_id=commit.hexsha,
                message=commit.message,
                author_name=commit.author.name,
                author_email=commit.author.email,
                commit_date=commit.committed_datetime,
                parents=[c.hexsha for c in commit.parents]))
    return GitHistoryParams(
        repo_id=root_sha,
        current_commit_id=repo.head.commit.hexsha,
        dirty=repo.is_dirty(),
        commits=commit_array,
        experiment_ids=experiment_ids
    )
