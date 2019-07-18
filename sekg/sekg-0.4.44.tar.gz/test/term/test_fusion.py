from unittest import TestCase

from sekg.term.fusion import Fusion


class TestTerm(TestCase):

    def test_fusion(self):
        fusion_tool = Fusion()
        terms = {"annotated bind", "low bind", "binds", "ok", "low of bind", "string tc", "Fine", "good", "pretty"}
        synsets = fusion_tool.fuse_by_synonym(terms)
        print(synsets)
