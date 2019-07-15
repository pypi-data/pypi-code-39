from unittest import TestCase

from storage import StorageRepository

class TestStorage(TestCase):
    def setUp(self):
        with open('data/P1.csv', 'r') as file:
            self.files = [file.readlines()]
        self.storage = StorageRepository(self.files)

    def test_build(self):
        self.storage.build()
        self.assertTrue(len(self.storage.storage) != 0)



