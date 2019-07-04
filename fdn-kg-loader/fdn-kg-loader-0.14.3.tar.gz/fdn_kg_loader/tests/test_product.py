
from ..model import Product
from ..store import Store
import unittest

class TestProduct(unittest.TestCase):
    def setUp(self):
        self.host = "127.0.0.1"
        self.keyspace = "schema_check"
    def tearDown(self):
        pass

    def test_insert(self):
        o = {"name":"Test Product","gid":"0001"}        
        p = Product()
        p.from_dict(o)
        self.assertIsNotNone(p)
        store = Store(host=self.host, keyspace = self.keyspace)
        store.save(p)
        store.flush()

        r = store.query('match $o isa product, has gid "0001"; get;')
        result = [x for x in r]
        print(result)
        self.assertTrue(len(result) > 0)

    def test_double_insert(self):
        pass
