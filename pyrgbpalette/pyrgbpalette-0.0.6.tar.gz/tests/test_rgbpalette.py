import unittest
from src.rgbpalette import *
from ddt import ddt, data, file_data, unpack

try:
    import yaml
except ImportError:  # pragma: no cover
    have_yaml_support = False
else:
    have_yaml_support = True
    del yaml

# A good-looking decorator
needs_yaml = unittest.skipUnless(
    have_yaml_support, "Need YAML to run this test"
)

@ddt
class Test_rgb_in_rainbow(unittest.TestCase):

    @data((0.0, (97, 0, 97)),
          (0.1, (92, 0, 198)),
          (0.2, (0, 92, 255)),
          (0.3, (0, 255, 244)),
          (0.4, (86, 255, 0)),
          (0.5, (210, 255, 0)),
          (0.6, (255, 183, 0)),
          (0.7, (255, 37, 0)),
          (0.8, (211, 0, 0)),
          (0.9, (157, 0, 0)),
          (0.99, (103, 0, 0)),
          (0.999, (97, 0, 0)),
          (0.9999, (97, 0, 0)),
          (1.0, (97, 0, 97)))
    @unpack
    def test_rgb_in_rainbow_ddt(self, val, result):
        rgbv = rgb_in_rainbow(val)
        self.assertEqual(result, rgbv)
