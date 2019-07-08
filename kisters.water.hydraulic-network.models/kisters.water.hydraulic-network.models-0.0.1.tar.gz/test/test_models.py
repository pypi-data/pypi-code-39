from unittest import TestCase

from kisters.water.hydraulic_network.models import Links, Nodes

TEST_DATA = {
    "links": [
        {
            "uid": "channel",
            "source_uid": "junction",
            "target_uid": "storage",
            "cross_sections": [
                {
                    "cross_section": [
                        {"width": 10.0, "level": 0},
                        {"width": 10.0, "level": 10},
                    ]
                }
            ],
            "length": 100.0,
            "roughness": 10.0,
            "model": "saint-venant",
            "roughness_model": "chezy",
            "created": "2019-06-27T16:53:05",
            "display_name": "channel",
            "type": "Channel",
        },
        {
            "uid": "delay",
            "source_uid": "junction",
            "target_uid": "storage",
            "transit_time": 10.0,
            "created": "2019-06-27T16:53:05",
            "display_name": "delay",
            "type": "Delay",
        },
        {
            "uid": "flow_controlled_structure",
            "source_uid": "junction",
            "target_uid": "storage",
            "min_flow": -1.0,
            "max_flow": 1.0,
            "created": "2019-06-27T16:53:05",
            "display_name": "flow_controlled_structure",
            "type": "FlowControlledStructure",
        },
        {
            "uid": "orifice",
            "source_uid": "junction",
            "target_uid": "storage",
            "model": "free",
            "coefficient": 1.0,
            "aperture": 10.0,
            "created": "2019-06-27T16:53:05",
            "display_name": "orifice",
            "type": "Orifice",
        },
        {
            "uid": "pipe",
            "source_uid": "junction",
            "target_uid": "storage",
            "diameter": 1.0,
            "length": 10.0,
            "roughness": 10.0,
            "model": "hazen-williams",
            "check_valve": False,
            "created": "2019-06-27T16:53:05",
            "display_name": "pipe",
            "type": "Pipe",
        },
        {
            "uid": "pump",
            "source_uid": "junction",
            "target_uid": "storage",
            "speed": [
                {"flow": 1, "head": 1, "speed": 1},
                {"flow": 3, "head": 3, "speed": 1},
            ],
            "min_speed": 1.0,
            "max_speed": 1.0,
            "created": "2019-06-27T16:53:05",
            "display_name": "pump",
            "type": "Pump",
        },
        {
            "uid": "turbine",
            "source_uid": "junction",
            "target_uid": "storage",
            "speed": [
                {"flow": 1, "head": 1, "speed": 1},
                {"flow": 3, "head": 3, "speed": 1},
            ],
            "min_speed": 1.0,
            "max_speed": 1.0,
            "created": "2019-06-27T16:53:05",
            "display_name": "turbine",
            "type": "Turbine",
        },
        {
            "uid": "valve",
            "source_uid": "junction",
            "target_uid": "storage",
            "diameter": 10.0,
            "model": "prv",
            "coefficient": 1.0,
            "setting": 0.0,
            "created": "2019-06-27T16:53:05",
            "display_name": "valve",
            "type": "Valve",
        },
        {
            "uid": "weir",
            "source_uid": "junction",
            "target_uid": "storage",
            "model": "free",
            "coefficient": 1.0,
            "min_crest_level": 0.0,
            "max_crest_level": 0.0,
            "crest_width": 10.0,
            "created": "2019-06-27T16:53:05",
            "display_name": "weir",
            "type": "Weir",
        },
    ],
    "nodes": [
        {
            "uid": "flow_boundary",
            "location": {"x": 0.0, "y": 0.0, "z": 0.0},
            "created": "2019-06-27T16:53:05",
            "display_name": "flow_boundary",
            "schematic_location": {"x": 0.0, "y": 0.0, "z": 0.0},
            "type": "FlowBoundary",
        },
        {
            "uid": "junction",
            "location": {"x": 0.0, "y": 1.0, "z": 0.0},
            "created": "2019-06-27T16:53:05",
            "display_name": "junction",
            "schematic_location": {"x": 0.0, "y": 1.0, "z": 0.0},
            "type": "Junction",
        },
        {
            "uid": "level_boundary",
            "location": {"x": 1.0, "y": 0.0, "z": 0.0},
            "created": "2019-06-27T16:53:05",
            "display_name": "level_boundary",
            "schematic_location": {"x": 1.0, "y": 0.0, "z": 0.0},
            "type": "LevelBoundary",
        },
        {
            "uid": "storage",
            "location": {"x": 1.0, "y": 1.0, "z": 0.0},
            "level_volume": [
                {"level": 0.0, "volume": 0.0},
                {"level": 10.0, "volume": 10.0},
            ],
            "created": "2019-06-27T16:53:05",
            "display_name": "storage",
            "schematic_location": {"x": 1.0, "y": 1.0, "z": 0.0},
            "type": "Storage",
        },
    ],
    "metadata": {
        "created": "2019-06-25T14:18:37",
        "projection": "unknown",
        "datum": "unknown",
        "num_hierarchy_levels": 1,
    },
}


class TestInstantiateSerialize(TestCase):
    def test00_instantiate_links(self):
        for link in TEST_DATA["links"]:
            link_instance = Links.instantiate(link)
            link_dict = link_instance.asdict()
            self.assertElementUnchanged(link, link_dict)

    def test50_instantiate_nodes(self):
        for node in TEST_DATA["nodes"]:
            node_instance = Nodes.instantiate(node)
            node_dict = node_instance.asdict()
            self.assertElementUnchanged(node, node_dict)

    def assertElementUnchanged(self, element0, element1):
        for prop, val in element0.items():
            original = element1[prop]
            if hasattr(original, "isoformat"):
                original = original.isoformat()
            self.assertEqual(original, val)
