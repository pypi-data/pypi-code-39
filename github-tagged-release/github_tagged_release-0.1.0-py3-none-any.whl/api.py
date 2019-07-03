import requests

BASE_URL = "https://api.github.com"


class GitHubAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def _send_request(self, url, **kwargs):
        return requests.post(url, headers={"Authorization": "Bearer {}".format(self.api_key)}, **kwargs)

    def create_release(self, owner, repo, tag_name, body, target_commitish="master", draft=False, prerelease=False):
        """
            Create a release tied to a tag on GitHub
            Ref: https://developer.github.com/v3/repos/releases/#create-a-release
        """
        data = {
            "tag_name": tag_name,
            "target_commitish": target_commitish,
            "name": tag_name,
            "body": body,
            "draft": draft,
            "prerelease": prerelease,
        }
        url = "{}/repos/{}/{}/releases".format(BASE_URL, owner, repo)
        res = self._send_request(url, json=data)
        try:
            res.raise_for_status()
        except requests.HTTPError:
            print("Create release failed:", res.status_code, res.text)
            return False

        return res.status_code == 201

    def search_pull_requests(self, owner, repo, start, end):
        # TODO: Add pagination
        """ Search a repository for PR's between start and end datetimes """
        query = {"merged": "{}..{}".format(start, end), "repo": "{}/{}".format(owner, repo)}
        search_query = " ".join(["{}:{}".format(key, val) for key, val in query.items()])
        query = (
            """
            {
              search(query: "%s", type: ISSUE, first: 100) {
                nodes {
                  ... on PullRequest {
                    number
                    title
                    author {
                      login
                    }
                    mergeCommit {
                      abbreviatedOid
                      authoredDate
                    }
                  }
                }
              }
            }
        """
            % search_query
        )

        res = self._send_request("{}/graphql".format(BASE_URL), json={"query": query})
        if res.status_code == 200:
            data = res.json()

            if "errors" in data:
                print("query", query, "errors", data)
                return []
            return data["data"]["search"]["nodes"]

        return []
