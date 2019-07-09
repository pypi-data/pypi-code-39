import click

from girder.models.collection import Collection
from girder.models.file import File
from girder.models.item import Item
from girder.models.user import User
from girder.utility.path import lookUpPath
from geometa.rest import create_geometa


@click.command(name="extract-geospatial",
               short_help='Manually extract geospatial data',
               help='Manually extract geospatial data on all '
                    'items under the provided paths')
@click.option('-p', '--path', multiple=True, default='/', show_default=True,
              help="Used to specify a path under which to extract data.")
def extract(path):
    resources = []

    if '/' in path:
        resources += [x for x in Collection().find({})]
        resources += [x for x in User().find({})]
    elif '/collection' in path:
        resources += [x for x in Collection().find({})]
    elif '/user' in path:
        resources += [x for x in User().find({})]
    else:
        for p in path:
            resources.append(lookUpPath(p)['document'])

    for resource in resources:
        items = [dict(x) for x in Item().find({
            'baseParentId': resource['_id']
        })]

        for item in items:
            files = [dict(x) for x in File().find({
                'itemId': item['_id']
            })]

            for file in files:
                create_geometa(item, file)
