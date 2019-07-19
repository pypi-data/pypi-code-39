# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['graphene_pydantic']

package_data = \
{'': ['*']}

install_requires = \
['graphene>=2.1.3,<3', 'pydantic>=0.25,<0.30']

setup_kwargs = {
    'name': 'graphene-pydantic',
    'version': '0.0.2',
    'description': 'Graphene Pydantic integration',
    'long_description': '# ![Graphene Logo](http://graphene-python.org/favicon.png) graphene-pydantic [![Build status](https://circleci.com/gh/upsidetravel/graphene-pydantic.svg?style=svg)](https://circleci.com/gh/upsidetravel/graphene-pydantic) [![PyPI version](https://badge.fury.io/py/graphene-pydantic.svg)](https://badge.fury.io/py/graphene-pydantic) [![Coverage Status](https://coveralls.io/repos/upsidetravel/graphene-pydantic/badge.svg?branch=master&service=github)](https://coveralls.io/github/upsidetravel/graphene-pydantic?branch=master)\n\n\n\nA [Pydantic](https://pydantic-docs.helpmanual.io/) integration for [Graphene](http://graphene-python.org/).\n\n## Installation\n\n```bash\npip install "graphene-pydantic"\n```\n\n## Examples\n\nHere is a simple Pydantic model:\n\n```python\nimport pydantic\n\nclass PersonModel(pydantic.BaseModel):\n    id: uuid.UUID\n    first_name: str\n    last_name: str\n\n```\n\nTo create a GraphQL schema for it you simply have to write the following:\n\n```python\nimport graphene\nfrom graphene_pydantic import PydanticObjectType\n\nclass Person(PydanticObjectType):\n    class Meta:\n        model = PersonModel\n        # only return specified fields\n        only_fields = ("name",)\n        # exclude specified fields\n        exclude_fields = ("id",)\n\nclass Query(graphene.ObjectType):\n    people = graphene.List(Person)\n\n    def resolve_people(self, info):\n        return get_people()  # function returning `PersonModel`s\n\nschema = graphene.Schema(query=Query)\n```\n\nThen you can simply query the schema:\n\n```python\nquery = \'\'\'\n    query {\n      people {\n        firstName,\n        lastName\n      }\n    }\n\'\'\'\nresult = schema.execute(query)\n```\n\n\n### Full Examples\n\nPlease see [the examples directory](./examples) for more. \n\n### License\n\nThis project is under the [Apache License](./LICENSE.md).\n\n### Third Party Code\n\nThis project depends on third-party code which is subject to the licenses set forth in [Third Party Licenses](./THIRD_PARTY_LICENSES.md).\n\n### Contributing\n\nPlease see the [Contributing Guide](./CONTRIBUTING.md). Note that you must sign the [CLA](./CONTRIBUTOR_LICENSE_AGREEMENT.md).\n\n### Caveats\n\nNote that even though Pydantic is perfectly happy with fields that hold mappings (e.g. dictionaries), because [GraphQL\'s type system doesn\'t have them](https://graphql.org/learn/schema/) those fields can\'t be exported to Graphene types. For instance, this will fail with an error `Don\'t know how to handle mappings in Graphene`: \n\n``` python\nimport typing\nfrom graphene_pydantic import PydanticObjectType\n\nclass Pet:\n  pass\n\nclass Person:\n  name: str\n  pets_by_name: typing.Dict[str, Pet]\n  \nclass GraphQLPerson(PydanticObjectType):  \n  class Meta:\n    model = Person\n```\n\nHowever, note that if you use `exclude_fields` or `only_fields` to exclude those values, there won\'t be a problem:\n\n``` python\nclass GraphQLPerson(PydanticObjectType):\n  class Meta:\n    model = Person\n    exclude_fields = ("pets_by_name",)\n```\n',
    'author': 'Rami Chowdhury',
    'author_email': 'rami@upside.com',
    'url': 'https://github.com/upsidetravel/graphene-pydantic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
