import unittest
from winterboot.WinterBoot import wireOneService, autoload, consumers
from winterboot.Autowired import Autowired
from winterboottest.WinterBootTestData import WinterBootTestData



class Test(unittest.TestCase):

    def setUp(self):
        self.testData = WinterBootTestData()
        Autowired(self.testData.undefinedConsumedServiceId)

    def test_wireOneService_by_default_wires_undefined_services(self):
        wireOneService(self.testData.undefinedConsumedServiceId,lazy=True)

    def test_wireOneService_throws_AttributeError_if_lazy_is_False_and_there_is_a_consumer(self):
        self.assertRaises(AttributeError,lambda: wireOneService(self.testData.undefinedConsumedServiceId,lazy=False))

    def test_wireOneService_is_silent_if_there_is_no_consumer(self):
        wireOneService(self.testData.undefinedNonConsumedServiceId,lazy=True)

    def test_wireOneService_is_silent_if_there_is_no_consumer_even_if_lazy_is_false(self):
        wireOneService(self.testData.undefinedNonConsumedServiceId,lazy=False)

    def test_autoload_registers_all_services_in_a_package(self):
        del(consumers[self.testData.undefinedConsumedServiceId])
        import testpackage
        autoload(testpackage)
        testService = Autowired('testService')
        self.assertTrue(testService.canBeCalled())

if __name__ == "__main__":
    unittest.main()