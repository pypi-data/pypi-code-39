# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dfa']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.1,<20.0', 'funcy>=1.12,<2.0']

setup_kwargs = {
    'name': 'dfa',
    'version': '0.3.2',
    'description': 'Python library for modeling DFAs.',
    'long_description': '# DFA\n\nA simple python implementation of a DFA. \n\n[![Build Status](https://cloud.drone.io/api/badges/mvcisback/dfa/status.svg)](https://cloud.drone.io/mvcisback/dfa)\n[![codecov](https://codecov.io/gh/mvcisback/dfa/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/dfa)\n[![PyPI version](https://badge.fury.io/py/dfa.svg)](https://badge.fury.io/py/dfa)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n<!-- markdown-toc start - Don\'t edit this section. Run M-x markdown-toc-generate-toc again -->\n**Table of Contents**\n\n- [Installation](#installation)\n- [Usage](#usage)\n    - [Membership Queries](#membership-queries)\n    - [Transitions and Traces](#transitions-and-traces)\n    - [Non-boolean output alphabets](#non-boolean-output-alphabets)\n    - [Moore Machines](#moore-machines)\n    - [DFA <-> Dictionary](#dfa---dictionary)\n    - [Computing Reachable States](#computing-reachable-states)\n\n<!-- markdown-toc end -->\n\n\n\n**Features:**\n\n1. State can be any Hashable object.\n2. Alphabet can be any finite sequence of Hashable objects.\n3. Designed to be immutable and hashable (assuming components are\n   immutable and hashable).\n4. Design choice to allow transition map and accepting set to be\n   given as functions rather than an explicit `dict` or `set`.\n\n# Installation\n\nIf you just need to use `dfa`, you can just run:\n\n`$ pip install dfa`\n\nFor developers, note that this project uses the\n[poetry](https://poetry.eustace.io/) python package/dependency\nmanagement tool. Please familarize yourself with it and then\nrun:\n\n`$ poetry install`\n\n# Usage\n\nThe `dfa` api is centered around the `DFA` object. \n\nBy default, the `DFA` object models a `Deterministic Finite Acceptor`,\ne.g., a recognizer of a Regular Language. \n\n**Example Usage:**\n```python\nfrom dfa import DFA\n\ndfa1 = DFA(\n    start=0,\n    inputs={0, 1},\n    label=lambda s: (s % 4) == 3,\n    transition=lambda s, c: (s + c) % 4,\n)\n\ndfa2 = DFA(\n    start="left",\n    inputs={"move right", "move left"},\n    label=lambda s: s == "left",\n    transition=lambda s, c: "left" if c == "move left" else "right",\n)\n```\n\n## Membership Queries\n\n```python\nassert dfa1.label([1, 1, 1, 1])\nassert not dfa1.label([1, 0])\n\nassert dfa2.label(["move right"]*100 + ["move left"])\nassert not dfa2.label(["move left", "move right"])\n```\n\n## Transitions and Traces\n\n```python\nassert dfa1.transition([1, 1, 1]) == 3\nassert list(dfa1.trace([1, 1, 1])) == [0, 1, 2, 3]\n```\n\n## Non-boolean output alphabets\n\nSometimes, it is useful to model an automata which can label a word\nusing a non-Boolean alphabet. For example, `{True, False, UNSURE}`.\n\nThe `DFA` object supports this by specifying the output alphabet.\n\n```python\nUNSURE = None\n\ndef my_labeler(s):\n    if s % 4 == 2:\n       return None\n    return (s % 4) == 3\n\n\ndfa3 = DFA(\n    start=0,\n    inputs={0, 1},\n    label=my_labeler,\n    transition=lambda s, c: (s + c) % 4,\n    outputs={True, False, UNSURE},\n)\n```\n\n**Note:** If `outputs` is set to `None`, then no checks are done that\nthe outputs are within the output alphabet.\n\n```python\ndfa3 = DFA(\n    start=0,\n    inputs={0, 1},\n    label=my_labeler,\n    transition=lambda s, c: (s + c) % 4,\n    outputs=None,\n)\n```\n\n## Moore Machines\n\nFinally, by reinterpreting the structure of the `DFA` object, one can\nmodel a Moore Machine. For example, in 3 state counter, `dfa1`, the\nMoore Machine can output the current count.\n\n```python\nassert dfa1.transduce(()) == ()\nassert dfa1.transduce((1,)) == (False,)\nassert dfa1.transduce((1, 1, 1, 1)) == (False, False, False, True)\n```\n\n## DFA <-> Dictionary\n\nNote that `dfa` provides helper functions for going from a dictionary\nbased representation of a deterministic transition system to a `DFA`\nobject and back.\n\n```python\nfrom dfa import dfa2dict, dict2dfa\n\n# DFA encoded a nested dictionaries with the following\n# signature.\n#     <state>: (<label>, {<action>: <next state>})\n\ndfa_dict = {\n    0: (False, {0: 0, 1: 1}),\n    1: (False, {0: 1, 1: 2}),\n    2: (False, {0: 2, 1: 3}), \n    3: (True, {0: 3, 1: 0})\n}\n\n# Dictionary -> DFA\ndfa = dict2dfa(dfa_dict, start=0)\n\n# DFA -> Dictionary\ndfa_dict2, start = dfa2dict(dfa)\n\nassert (dfa_dict, 0) == (dfa_dict2, start)\n```\n\n## Computing Reachable States\n\n```python\n# Perform a depth first traversal to collect all reachable states.\nassert dfa1.states() == {0, 1, 2, 3}\n```\n',
    'author': 'Marcell Vazquez-Chanlatte',
    'author_email': 'marcell.vc@eecs.berkeley.edu',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
