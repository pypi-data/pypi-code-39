import os
import sys
from datetime import datetime, timezone, timedelta

from github_release.api import GitHubAPI
from .utils import run_cmd

try:
    import dotenv

    dotenv.load_dotenv()
except ImportError:
    pass


DEFAULT_OPTIONS = {"changelog": False, "git_dir": None, "tag": None}


class GitHubRelease:
    _previous_tag = None
    repo = owner = tag = tag_commit = github_api_key = None

    def __init__(self, options=None):
        """
        Init with some env vars or arguments
        Ref: https://circleci.com/docs/2.0/env-vars/#built-in-environment-variables
        """
        self.options = DEFAULT_OPTIONS
        if options:
            if not isinstance(options, dict):
                options = vars(options)
            self.options.update(options)
            self.tag = self.options["tag"]
        self._set_env_vars()
        self.api = GitHubAPI(self.github_api_key)

    def _set_env_vars(self):
        env_vars = {
            "repo": "CIRCLE_PROJECT_REPONAME",
            "owner": "CIRCLE_PROJECT_USERNAME",
            "tag": "CIRCLE_TAG",
            "github_api_key": "GITHUB_API_KEY",
        }
        missing_attrs = []
        for attr, env_var in env_vars.items():
            if getattr(self, attr) is not None:
                continue  # Do not override
            env_var_value = os.getenv(env_var)
            setattr(self, attr, env_var_value)
            if env_var_value is None:
                missing_attrs.append(env_var)
        if missing_attrs:
            print("Missing attributes from environment:\n- {}".format("\n- ".join(missing_attrs)))
            sys.exit(1)

    def git_cmd(self, args):
        cmd = ["git"]
        if self.options["git_dir"]:
            cmd.append("--git-dir={}".format(self.options["git_dir"]))
        return run_cmd(cmd + args)

    @property
    def previous_tag(self):
        if self._previous_tag:
            return self._previous_tag

        self._previous_tag = self.git_cmd(["describe", "--abbrev=0", "--tags", "{}^".format(self.tag)])

        return self._previous_tag

    def _tag_commit(self, tag):
        return self.git_cmd(["rev-parse", tag])

    def _initial_commit(self):
        return self.git_cmd(["rev-list", "--max-parents=0", "HEAD"])

    def format_release_body(self, pull_requests):
        """ Format a release changelog in markdown """
        if pull_requests:
            pull_requests.sort(key=lambda x: x["mergeCommit"]["authoredDate"], reverse=True)  # sorted by merged date

            pr_lines = []
            for pr in pull_requests:
                author = "@{}".format(pr["author"]["login"])
                merge_commit = pr["mergeCommit"]["abbreviatedOid"]
                pr_lines.append("- #{} {} (by {} in {})".format(pr["number"], pr["title"], author, merge_commit))

            body = "\n".join(pr_lines)
        else:
            body = "No merged pull requests."
        if self.previous_tag:
            base_url = "https://github.com/{}/{}".format(self.owner, self.repo)
            prev_tag_url = "{}/releases/tag/{}".format(base_url, self.previous_tag)
            compare_url = "{}/compare/{}...{}".format(base_url, self.previous_tag, self.tag)
            since = "Compare: [{}...{}]({}). Last release: [{}]({})\n".format(
                self.previous_tag, self.tag, compare_url, self.previous_tag, prev_tag_url
            )
        else:
            since = "Since *first commit*\n"
        return "## Changelog\n{}{}".format(since, body)

    def _set_and_verify_tag_commit(self):
        self.tag_commit = self._tag_commit(self.tag)
        if self.tag_commit is None:
            print("Error: tag '{}' not found in git index".format(self.tag))
            sys.exit(1)

    def ref_or_commit_datetime(self, ref_or_commit):
        date_format = "%Y-%m-%d %H:%M:%S %z"
        date_string = self.git_cmd(["log", "-1", "--format=%ai", ref_or_commit])
        # FIXME: Add 1 minute offset, why?
        dt = datetime.strptime(date_string, date_format).astimezone(timezone.utc) + timedelta(minutes=1)
        return dt.isoformat()

    def datetime_range_since_previous_tag(self):
        if self.previous_tag is None:
            print("No previous tag found, assuming first tag and basing off initial commit")
            # start_ref = 'Initial commit'
            start = self.ref_or_commit_datetime(self._initial_commit())
        else:
            # start_commit = self._tag_commit(self.previous_tag)
            start = self.ref_or_commit_datetime(self.previous_tag)

        end = self.ref_or_commit_datetime(self.tag)
        # refs_range = '{}...{}'.format(start_commit[:8], self.tag_commit[:8])
        # print('Range: {} ({}...{})'.format(refs_range, start_ref, self.tag))
        # print('Range datetimes: {} {}'.format(start, end))
        return start, end

    def prepare_changelog(self):
        self._set_and_verify_tag_commit()
        start, end = self.datetime_range_since_previous_tag()
        pull_requests = []
        if start and end:
            pull_requests = self.api.search_pull_requests(self.owner, self.repo, start, end)
            if not pull_requests and not self.options["changelog"]:
                print("No pull requests found!")

        return self.format_release_body(pull_requests)

    def create_release_from_tag(self):
        body = self.prepare_changelog()
        self.api.create_release(self.owner, self.repo, self.tag, body)

    def changelog(self):
        print(self.prepare_changelog())
