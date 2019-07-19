import click
import json
from bson.objectid import ObjectId

from girder.models.collection import Collection


@click.command(name="populate-collection-meta",
               short_help='Populates a collection with the provided metadata',
               help='Populates a collection\'s meta field with '
                    'the provided JSON data')
@click.option('-i', '--id', multiple=True, required=True,
              help="Used to specify a collection ID to extract metadata to.")
@click.option('-d', '--data', required=True,
              help="The metadata to populate the desired collection(s) with.")
def populate(id, data):
    data = json.load(open(data, 'r'))
    success = 0

    for collectionId in id:
        collection = Collection().findOne({
            '_id': ObjectId(collectionId)
        })

        if (collection):
            Collection().setMetadata(collection=collection, metadata=data)
            success += 1
        else:
            click.echo('Warning: No collection found with ID: ' + collectionId)

    click.echo('Successfully set metadata on '
               + str(success) + '/' + str(len(id)) + ' collections')
