from typing import List, Optional

import attr
from attr import attrs

from cortex_common.types import ProfileSchema, ProfileTaxonomySchema
from cortex_common.utils.attr_utils import describableAttrib
from cortex_common.utils.object_utils import head, unique_id

__all__ = [
    "ProfileAttributeSchemaQuery",
    "RecursiveProfileHierarchyGroup",
]


@attrs(frozen=True)
class ProfileAttributeSchemaQuery(object):
    """
    """
    # ---------------
    attributesWithNames = describableAttrib(type=Optional[List[str]], default=None, description="...?")
    attributesWithAnyTags = describableAttrib(type=Optional[List[str]], default=None, description="...?")
    attributesWithAllTags = describableAttrib(type=Optional[List[str]], default=None, description="...?")
    attributesInAnyGroups = describableAttrib(type=Optional[List[str]], default=None, description="...?")
    attributesInAllGroups = describableAttrib(type=Optional[List[str]], default=None, description="...?")
    none = describableAttrib(type=Optional[bool], default=None, description="Should any attributes be queried?")
    all = describableAttrib(type=Optional[bool], default=None, description="Should all attributes be queried?")
    # ---------------
    intersection = describableAttrib(
        type=Optional[List['ProfileAttributeSchemaQuery']], default=None,
        description="Should this query intersect with another query?"
    )
    union = describableAttrib(
        type=Optional[List['ProfileAttributeSchemaQuery']], default=None,
        description="How do I combine the results of multiple queries?"
    )
    inverse = describableAttrib(
        type=Optional['ProfileAttributeSchemaQuery'], default=None,
        description="How do I invert the results of a query?"
    )
    # ----------------
    intersection_as_default = describableAttrib(
        type=bool, default=True,
        description="If multiple options of the query are provided, will they be intersected by default?"
    )


def prepare_to_be_flattened(parentNode:'RecursiveProfileHierarchyGroup', childNode:'RecursiveProfileHierarchyGroup') -> 'RecursiveProfileHierarchyGroup':
    oldChildName = childNode.name
    # Update the name of the child to have the parents name ...
    e1 = attr.evolve(childNode, name="{}/{}".format(parentNode.name, childNode.name))
    # Update all the children of the child node to point to the child nodes new name
    e2 = attr.evolve(e1, children=[
        attr.evolve(
            child_of_e1,
            parents=[attr.evolve(p, name=e1.name) if p.name == oldChildName else p for p in child_of_e1.parents]
        )
        for child_of_e1 in e1.children
    ])
    # Repeat process for all the children of the node ..
    e3 = attr.evolve(e2, children=[prepare_to_be_flattened(e2, child_of_e2) for child_of_e2 in e2.children])
    return e3


@attr.attrs(frozen=True)
class RecursiveProfileHierarchyGroup(object):
    name = describableAttrib(type=str, description="What is the name of the profile hierarchy node?")
    label = describableAttrib(type=str, description="What is the label of the profile hierarchy node?")
    description = describableAttrib(type=str, description="What is the essential meaning of this group?")
    includedAttributes = describableAttrib(type=ProfileAttributeSchemaQuery, description="What attributes are included in this group?")
    tags = describableAttrib(type=List[str], factory=list, description="What list of tags is applied to this group?")
    parents = describableAttrib(type=List['RecursiveProfileHierarchyGroup'], factory=list, description="What are the parents of this group of attributes ...?")
    children = describableAttrib(type=List['RecursiveProfileHierarchyGroup'], factory=list, description="What are the children of this group of attributes ...?")
    id = describableAttrib(type=str, factory=unique_id, description="What is the unique identifier for this group ...?")

    # Traversal method to help construct a recusive data structure
    def append_children(self, nodes:List['RecursiveProfileHierarchyGroup']) -> 'RecursiveProfileHierarchyGroup':
        """
        Children are to be associated later ...
        :param node:
        :return:
        """
        # The children are all siblings of the parent ...
        if not nodes:
            return self
        head, tail = nodes[0], nodes[1:]
        return self.append_child(head).append_children(tail)

    def append_child(self, node:'RecursiveProfileHierarchyGroup') -> 'RecursiveProfileHierarchyGroup':
        """
        Children are to be associated later ...
        :param node:
        :return:
        """
        return attr.evolve(self, children=self.children+[attr.evolve(node, tags=self.tags+node.tags, parents=node.parents+[self])])

    def to_profile_hierarchy_schema(self, schema:ProfileSchema) -> ProfileTaxonomySchema:
        return ProfileTaxonomySchema(
            name=self.name,
            label=self.label,
            description=self.description,
            tags=self.tags,
            parent=head([x.name for x in self.parents]),
            # attributes=query_attributes(self.includedAttributes, schema),
            # parents=[x.name for x in self.parents],
            # children=[x.name for x in self.children],
            id=self.id
        )

    def flatten(self, schema:ProfileSchema) -> List[ProfileTaxonomySchema]:
        schema_to_flatten = attr.evolve(self, children=[prepare_to_be_flattened(self, c) for c in self.children])
        return schema_to_flatten._flatten(schema)

    def _flatten(self, schema:ProfileSchema) -> List[ProfileTaxonomySchema]:
        hierarchical_schema = self.to_profile_hierarchy_schema(schema)
        return [hierarchical_schema] + [x for child in self.children for x in child._flatten(schema)]
