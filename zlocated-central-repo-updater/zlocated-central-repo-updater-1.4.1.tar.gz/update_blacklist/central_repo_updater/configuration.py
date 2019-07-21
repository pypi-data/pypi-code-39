"""
The tool to update the central repository of the Ultimate-Hosts-Blacklist project.

Provide the configurations data.

License:
::


    MIT License

    Copyright (c) 2019 Ultimate-Hosts-Blacklist
    Copyright (c) 2019 Nissar Chababy
    Copyright (c) 2019 Mitchell Krog

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
# pylint: disable=line-too-long, anomalous-backslash-in-string
from os import environ, getcwd, path
from os import sep as directory_separator
from time import strftime, time


class GitHub:  # pylint: disable=too-few-public-methods
    """
    Provide the configuration related to the GitHub communication.
    """

    # This is the username we are going to use when communicating with the
    # GitHub API.
    username = "zlocated"

    try:
        # DO NOT edit this line.
        api_token = environ["GH_TOKEN"]
    except KeyError:
        # You can edit this line.
        api_token = ""

    # Set the GitHub repository slug.
    org_slug = "Ultimate-Hosts-Blacklist"

    # Set the list of URL we are working with.
    # Note: Every URL should ends with /.
    urls = {
        "api": "https://api.github.com/",
        "raw": "https://raw.githubusercontent.com/",
    }

    # We partially construct the RAW link.
    partial_raw_link = "{0}{1}/%s/master/".format(urls["raw"], org_slug)

    # We construct the complete link to the ORGS api page.
    complete_api_orgs_url = "{0}orgs/{1}".format(urls["api"], org_slug)


class Infrastructure:  # pylint: disable=too-few-public-methods
    """
    Provide the configuration related to our infrastructure,
    """

    # Set the list of repository we are going to ignore.
    repositories_to_ignore = [
        "cleaning",
        "dev-center",
        "repository-structure",
        "whitelist",
    ]

    try:
        # We construct the version.
        version = "V1.%s.%s.%s.%s" % (
            environ["TRAVIS_BUILD_NUMBER"],
            strftime("%Y"),
            strftime("%m"),
            strftime("%d"),
        )
    except KeyError:
        version = str(int(time()))


class Output:  # pylint: disable=too-few-public-methods
    """
    Provide teh configuration related to everything we are going to create.
    """

    current_directory = getcwd() + directory_separator

    max_file_size_in_bytes = 5_242_880

    template_dir = "templates"

    if path.isdir("{0}{1}".format(current_directory, template_dir)):
        templates_dir = "{0}{1}".format(current_directory, template_dir)
    else:
        templates_dir = None

    etags_file = "{0}etags.json".format(current_directory)
    repos_file = "{0}repos.json".format(current_directory)
    readme_file = "{0}README.md".format(current_directory)

    dotted_directory = "{0}domains-dotted-format{1}".format(
        current_directory, directory_separator
    )
    incomplete_dotted_filename = "domains-dotted-format{}.list"

    plain_text_domains_directory = "{0}domains{1}".format(
        current_directory, directory_separator
    )
    incomplete_plain_text_domains_filename = "domains{0}.list"

    plain_text_ips_directory = "{0}ips{1}".format(
        current_directory, directory_separator
    )
    incomplete_plain_text_ips_filename = "ips{0}.list"


class Templates:  # pylint: disable=too-few-public-methods
    """
    Provide the different templates
    """

    # The UNIX hosts templaste.

    # The windows hosts template.

    # The hosts.deny template.
 
    # The superhosts.deny template.
    
    # The README template.
    readme_md = """# DNSMasq BlackList - personal dnsmasq blacklist generator (fork of Ultimate Hosts File blacklist)

| Updated | Fueled By |
| :-----: | :------: |
| Daily :heavy_check_mark: | [<img src="https://github.com/mitchellkrogza/Ultimate.Hosts.Blacklist/blob/master/.assets/ultimate-hosts-org-small.png" alt="Hosts File - Ultimate Hosts Blacklist"/>](https://github.com/Ultimate-Hosts-Blacklist) |
| [![Build Status](https://travis-ci.org/mitchellkrogza/Ultimate.Hosts.Blacklist.svg?branch=master)](https://travis-ci.org/mitchellkrogza/Ultimate.Hosts.Blacklist) | [![DUB](https://img.shields.io/dub/l/vibe-d.svg)](https://github.com/mitchellkrogza/Ultimate.Hosts.Blacklist/blob/master/LICENSE.md) |

---

- Version: **%%version%%**
- Total Bad Hosts in hosts file: **%%lenHosts%%**
- Total Bad IP's in hosts.deny file: **%%lenIPs%%**
- Total Bad Hosts and IP's in superhosts.deny file: **%%lenHostsIPs%%**

  :exclamation: **Yes you did indeed read those numbers correctly** :exclamation:

---
"""
