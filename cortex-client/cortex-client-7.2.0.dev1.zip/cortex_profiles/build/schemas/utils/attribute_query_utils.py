from functools import reduce
from typing import List, Optional

import attr
from objectpath import Tree

from cortex_common.types import ProfileSchema
from cortex_profiles.types import ProfileAttributeSchemaQuery


def run_list_producing_query(schemaTree:Tree, query):
    results = schemaTree.execute(query)
    return list(results) if results is not None else []


def query_inverse_of_attributes(schemaTree:Tree, attributes:List[str]):
    if not attributes:
        return attributes
    return run_list_producing_query(schemaTree, "$.attributes[ @.name not in {} ].name".format(attributes))


def query_all_attributes(schemaTree:Tree):
    return run_list_producing_query(schemaTree, "$.attributes.*.name")


def query_attributes_with_names(schemaTree:Tree, names:List[str]):
    if not names:
        return names
    return run_list_producing_query(schemaTree, "$.attributes[ @.name in {} ].name".format(names))


def query_attributes_with_any_tags(schemaTree:Tree, tags:List[str]):
    if not tags:
        return tags
    return list(
        reduce(
            lambda setA, setB: setA.union(setB),
            [
                set(run_list_producing_query(schemaTree, f"$.attributes[ '{tag}' in @.tags ].name"))
                for tag in tags
            ]
        )
    )


def query_attributes_with_all_tags(schemaTree:Tree, tags:List[str]):
    if not tags:
        return tags
    return list(
        reduce(
            lambda setA, setB: setA.intersection(setB),
            [
                set(run_list_producing_query(schemaTree, f"$.attributes[ '{tag}' in @.tags ].name"))
                for tag in tags
            ]
        )
    )


def tags_in_group(schemaTree:Tree, group:str):
    return [ y for x in run_list_producing_query(schemaTree, f"$.groups[ '{group}' is @.id].tags") for y in x]


def query_attributes_in_any_groups(schemaTree:Tree, groups:List[str]):
    if not groups:
        return groups
    return list(
        reduce(
            lambda setA, setB: setA.union(setB),
            [
                set(query_attributes_with_any_tags(schemaTree, tags_in_group(schemaTree, group)))
                for group in groups
            ]
        )
    )

def query_attributes_in_all_groups(schemaTree:Tree, groups:List[str]):
    if not groups:
        return groups
    return list(
        reduce(
            lambda setA, setB: setA.intersection(setB),
            [
                set(query_attributes_with_any_tags(schemaTree, tags_in_group(schemaTree, group)))
                for group in groups
            ]
        )
    )

def query_attributes(query: ProfileAttributeSchemaQuery, schema:ProfileSchema, tree:Optional[Tree]=None) -> List[str]:
    tree = Tree(attr.asdict(schema)) if tree is None else tree
    query_result_sets = [
        [] if query.none else None,
        query_all_attributes(tree) if query.all is not None else None,
        query_attributes_with_names(tree, query.attributesWithNames) if query.attributesWithNames is not None else None,
        query_attributes_with_any_tags(tree, query.attributesWithAnyTags) if query.attributesWithAnyTags is not None else None,
        query_attributes_with_all_tags(tree, query.attributesWithAllTags) if query.attributesWithAllTags is not None else None,
        query_attributes_in_any_groups(tree, query.attributesInAnyGroups) if query.attributesInAnyGroups is not None else None,
        query_attributes_in_all_groups(tree, query.attributesInAllGroups) if query.attributesInAllGroups is not None else None,
        reduce(
            lambda setA, setB: setA.intersection(setB),
            [set(query_attributes(inner_query, schema, tree)) for inner_query in query.intersection]
        ) if query.intersection is not None else None,
        reduce(
            lambda setA, setB: setA.union(setB),
            [set(query_attributes(inner_query, schema, tree)) for inner_query in query.union]
        ) if query.union is not None else None,
        query_inverse_of_attributes(tree, query_attributes(query.inverse, schema, tree)) if query.inverse is not None else None

    ]
    results = reduce(
        lambda setA, setB: setA.intersection(setB) if query.intersection_as_default else setA.union(setB),
        [set(x) for x in query_result_sets if x is not None ]
    )
    return list(results)
