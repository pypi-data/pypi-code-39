import re

import pandas as pd

from seeq.sdk import *

from . import _common
from . import _login
from . import _push


def search(query, all_properties=False, workbook=_common.DEFAULT_WORKBOOK_PATH):
    """
    Issues a query to the Seeq Server to retrieve metadata for signals,
    conditions, scalars and assets. This metadata can be used to retrieve
    samples, capsules for a particular time range.
    :param query: A dictionary of property / match-criteria pairs. Match
    criteria uses the same syntax as the Data tab in Seeq.
    :type query: dict
    :param workbook: A path string (with >> delimiters) to indicate a workbook
    for which to scope the search to. Note that globally scoped items will
    still be returned.
    :type workbook: str
    :param all_properties: True if all item properties should be retrieved.
    This currently makes the search operation much slower as retrieval of
    properties for an item requires a separate call.
    :return: A DataFrame with rows for each item found and columns for each
    property.
    :rtype: pd.DataFrame
    """
    items_api = ItemsApi(_login.client)
    trees_api = TreesApi(_login.client)

    if isinstance(query, pd.DataFrame):
        queries = query.to_dict(orient='records')
        comparison = '=='
    else:
        queries = [query]
        comparison = '~='

    data = list()
    columns = list()

    for query in queries:
        allowed_properties = ['Type', 'Name', 'Description', 'Path', 'Asset', 'Datasource Class', 'Datasource ID',
                              'Datasource Name', 'Cache Enabled', 'Archived', 'Scoped To']

        for key, value in query.items():
            if key not in allowed_properties:
                print('Property "%s" is not an indexed property and will be ignored. Use any of the '
                      'following searchable properties and then filter further using DataFrame '
                      'operations:\n"%s"' % (key, '", "'.join(allowed_properties)))

        item_types = list()
        clauses = list()

        if _common.present(query, 'Type'):
            item_type_specs = list()
            if isinstance(query['Type'], list):
                item_type_specs.extend(query['Type'])
            else:
                item_type_specs.append(query['Type'])

            for item_type_spec in item_type_specs:
                if item_type_spec == 'Signal':
                    item_types.extend(['StoredSignal', 'CalculatedSignal'])
                elif item_type_spec == 'Condition':
                    item_types.extend(['StoredCondition', 'CalculatedCondition'])
                elif item_type_spec == 'Scalar':
                    item_types.extend(['StoredScalar', 'CalculatedScalar'])
                else:
                    item_types.append(item_type_spec)

            del query['Type']

        if _common.present(query, 'Datasource Name'):
            datasource_results = items_api.search_items(filters=['Name == %s' % _common.get(query, 'Datasource Name')],
                                                        types=['Datasource'],
                                                        limit=100000)  # type: ItemSearchPreviewPaginatedListV1

            if len(datasource_results.items) > 1:
                raise RuntimeError('Multiple datasources found that match "%s"' % _common.get(query, 'Datasource Name'))
            elif len(datasource_results.items) == 0:
                raise RuntimeError('No datasource found that matches "%s"' % _common.get(query, 'Datasource Name'))
            else:
                datasource = datasource_results.items[0]  # type: ItemSearchPreviewV1
                query['Datasource ID'] = items_api.get_property(id=datasource.id, property_name='Datasource ID').value
                query['Datasource Class'] = items_api.get_property(id=datasource.id,
                                                                   property_name='Datasource Class').value

            del query['Datasource Name']

        if _common.present(query, 'Asset') and not _common.present(query, 'Path'):
            raise RuntimeError('"Path" query parameter must be present when "Asset" parameter present')

        asset_id = None
        if _common.present(query, 'Path'):
            path = re.split(r'\s*>>\s*', query['Path'])
            if _common.present(query, 'Asset'):
                path.append(query['Asset'])
                del query['Asset']

            for part in path:
                if not asset_id:
                    tree_output = trees_api.get_tree_root_nodes()  # type: AssetTreeOutputV1
                else:
                    tree_output = trees_api.get_tree(id=asset_id)  # type: AssetTreeOutputV1

                found = False
                for child in tree_output.children:  # type: TreeItemOutputV1
                    if child.name == part:
                        found = True
                        asset_id = child.id
                        break

                if not found:
                    print('Could not found asset "%s"' % query['Path'])
                    return

            del query['Path']

        for prop_name in ['Name', 'Description', 'Datasource Class', 'Datasource ID', 'Data ID']:
            if prop_name in query and query[prop_name] is not None:
                clauses.append(prop_name + comparison + query[prop_name])
                del query[prop_name]

        filters = [' && '.join(clauses)] if len(clauses) > 0 else []

        kwargs = {
            'filters': filters,
            'types': item_types,
            'limit': _common.DEFAULT_SEARCH_PAGE_SIZE
        }

        if asset_id:
            kwargs['asset'] = asset_id

        if workbook:
            workbook_id = _push.reify_workbook(workbook, create=False)
            if workbook_id:
                kwargs['scope'] = workbook_id

        if 'Scoped To' in query and query['Scoped To'] is not None:
            kwargs['scope'] = query['Scoped To']
            kwargs['filters'].append('@excludeGloballyScoped')

        def _do_search(offset):
            kwargs['offset'] = offset
            if offset > 0:
                print('Retrieved %d items...' % offset)
            return items_api.search_items(**kwargs)

        def _gather_results(result):
            result = result  # type: ItemSearchPreviewV1
            prop_dict = dict()

            def _add_to_dict(key, val):
                prop_dict[key] = _common.none_to_nan(val)

                # We want the columns to appear in a certain order (the order we added them in) for readability
                if key not in columns:
                    columns.append(key)

            _add_to_dict('ID', result.id)
            if len(result.ancestors) > 0:
                _add_to_dict('Path', ' >> '.join([a.name for a in result.ancestors[0:-1]]))
                _add_to_dict('Asset', result.ancestors[-1].name)
            _add_to_dict('Name', result.name)
            _add_to_dict('Description', result.description)
            _add_to_dict('Type', result.type)
            uom = result.value_unit_of_measure if result.value_unit_of_measure else result.source_value_unit_of_measure
            _add_to_dict('Value Unit Of Measure', uom)
            datasource_item_preview = result.datasource  # type: ItemPreviewV1
            _add_to_dict('Datasource Name', datasource_item_preview.name if datasource_item_preview else None)
            if all_properties:
                item = items_api.get_item_and_all_properties(id=result.id)  # type: ItemOutputV1
                for prop in item.properties:  # type: PropertyOutputV1
                    _add_to_dict(prop.name, prop.value)

            data.append(prop_dict)

        _iterate_over_output(_do_search, 'items', _gather_results)

    print('Returned %d result(s).' % len(data))

    return pd.DataFrame(data=data, columns=columns)


def _iterate_over_output(output_func, collection_name, action_func):
    offset = 0
    while True:
        output = output_func(offset)

        collection = getattr(output, collection_name)

        for item in collection:
            action_func(item)

        if len(collection) != output.limit:
            break

        offset += output.limit
