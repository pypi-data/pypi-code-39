import unittest
from winterboot.WinterBoot import consumers
from winterboot.Autowired import Autowired
from winterboottest.WinterBootTestData import WinterBootTestData

class Test(unittest.TestCase):


    def setUp(self):
        self.serviceId = WinterBootTestData().undefinedConsumedServiceId
        self.testArtifact = Autowired(self.serviceId)

    def tearDown(self):
        del consumers[self.serviceId]

    def testAutowired_stores_itself_in_the_consumers_for_service_id(self):
        self.assertTrue(self.testArtifact in consumers[self.serviceId])
    

    def test_an_error_is_raised_if_we_try_to_use_an_autowired_service_without_definition(self):
        self.assertRaises(AttributeError,lambda : Autowired(self.serviceId).call())

if __name__ == "__main__":
    unittest.main()