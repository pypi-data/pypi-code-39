# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyppl-report']

package_data = \
{'': ['*'],
 'pyppl-report': ['resources/filters/*',
                  'resources/templates/bootstrap/*',
                  'resources/templates/bootstrap/static/*']}

install_requires = \
['cmdy',
 'panflute>=1.0.0,<2.0.0',
 'pyppl>=2.0.0,<3.0.0',
 'pyyaml>=5.0.0,<6.0.0']

setup_kwargs = {
    'name': 'pyppl-report',
    'version': '0.0.1',
    'description': 'A report generating system for PyPPL',
    'long_description': '# pyppl-report\n\nA report generating system for [PyPPL][1]\n\n## Installation\n```shell\npip install pyppl-report\n```\n\n## Usage\n### Specifiation of template\n\n````python\npPyClone.report = """\n## {{proc.desc}}\n\nPyClone[1] is a tool using Probabilistic model for inferring clonal population structure from deep NGS sequencing.\n\n![Similarity matrix]({{path.join(job.o.outdir, "plots/loci/similarity_matrix.svg")}})\n\n```table\ncaption: Clusters\nfile: "{{path.join(job.o.outdir, "tables/cluster.tsv")}}"\nrows: 10\n```\n\n[1]: Roth, Andrew, et al. "PyClone: statistical inference of clonal population structure in cancer." Nature methods 11.4 (2014): 396.\n"""\n\n# or use a template file\n\npPyClone.report = "file:/path/to/template.md"\n````\n\n### Generating report\n```python\nPyPPL().start(pPyClone).run().report(\'/path/to/report\', title = \'Clonality analysis using PyClone\')\n```\n\n![Snapshort](./snapshot.png)\n\n### Extra data for rendering\nYou can generate a `YAML` file named `job.report.data.yaml` under `<job.outdir>` with extra data to render the report template. Beyond that, `proc` attributes and `args` can also be used.\n\nFor example:\n`job.report.data.yaml`:\n```yaml\ntitle: \'A awesome report for job 1\'\n```\nThen in your template, you can use it:\n```markdown\n## {{jobs[0].title}}\n```\n\n### Showing tables with csv/tsv file\n\n````markdown\n```table\ncaption    : An awesome table\nfile       : /path/to/csv/tsv/file\nheader     : true\nwidth      : 1   # width of each column\ntotal_width: .8  # total width of the table\nalign      : default # alignment of each column\nrows       : 10  # max rows to show\ncols       : 0   # max cols to show, default: 0 (show all)\ncsvargs    : # csvargs for `csv.read`\n\tdialect: unix\n\tdelimiter: "\\t"\n````\n\nYou may also specify `width` and `align` for individual columns:\n```yaml\nwidth:\n  - .1\n  - .2\n  - .1\n```\n\n### References\n\nWe use `[1]`, `[2]` ... to link to the references, so HTML links have to be in-place (in the format of `[text](link)` instead of `[text][link-index]`). All references from different processes will be re-ordered and combined.\n\n[1]: https://github.com/pwwang/PyPPL\n',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'url': 'https://github.com/pwwang/pyppl-report',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
