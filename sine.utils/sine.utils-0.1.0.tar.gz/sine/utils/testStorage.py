import unittest
import os
import uuid
import random
from .storage import Storage

filepath = './temp_test_storage'


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        open(filepath, 'w').close()

    def test_dictFunc(self):
        storage = Storage(filepath)
        key = str(uuid.uuid4())
        value = 'test_content'
        value2 = 'test_content2'
        storage.set(key, value)
        self.assertEqual(storage[key], storage.get(key), msg='getitem')
        storage[key] = value2
        self.assertEqual(storage.get(key), value2, msg='setitem')
        del storage[key]
        self.assertEqual(key in storage, False, msg='delitem')

        storage.set(key, value2)
        storage.setdefault(key, value)
        self.assertEqual(storage.get(key), value2, msg='setdefault')
        storage.clear()
        self.assertEqual(len(storage.items()), 0, msg='empty data')
        del storage

        storage = Storage(filepath)
        self.assertEqual(len(storage.items()), 0, msg='empty data')
        del storage

        return

    def test_baseReadWrite(self):
        storage = Storage(filepath)
        self.assertEqual(len(storage.items()), 0, msg='empty data')
        key = str(uuid.uuid4())
        value = 'test_content'
        storage.set(key, value)
        self.assertEqual(len(storage.items()), 1, msg='one data')
        del storage

        storage = Storage(filepath)
        self.assertEqual(storage[key], value, msg='reopen, correct')
        self.assertEqual(len(storage.items()), 1, msg='reopen, one data')
        storage.pop(key)
        self.assertEqual(len(storage.items()), 0, msg='reopen, delete')
        del storage

        return

    def test_set(self):
        storage = Storage(filepath)
        key = str(uuid.uuid4())
        value = 'test_content'
        storage.set(key, '123')
        storage.set(key, value)
        del storage

        storage = Storage(filepath)
        self.assertEqual(storage[key], value, msg='immediate set')
        del storage

        value2 = 'test_content2'
        storage = Storage(filepath)
        storage.set(key, value2)
        del storage

        storage = Storage(filepath)
        self.assertEqual(storage[key], value2, msg='reopen set')
        del storage

        return

    def test_randomOp(self):
        testSize = 1000

        storage = Storage(filepath)
        control = {}

        i = 0
        while i < testSize:
            i += 1
            op = random.randint(1, 2)
            if op == 1:
                key = str(random.randint(0, testSize))
                value = str(random.randint(0, testSize))
                control[key] = value
                storage.set(key, value)
            elif op == 2:
                key = str(random.randint(0, testSize))
                if key in control:
                    del control[key]
                storage.pop(key)

        del storage

        storage = Storage(filepath)
        self.assertEqual(len(storage.items()), len(
            control.items()), msg='random data size')
        for k, v in storage.items():
            self.assertIn(k, control, msg='missing data ' + k)
            self.assertEqual(v, control[k], msg='random data mismatch')
        del storage

        storage = Storage(filepath)
        self.assertEqual(len(storage.items()), len(
            control.items()), msg='(2)random data size')
        for k, v in storage.items():
            self.assertIn(k, control, msg='(2)missing data ' + k)
            self.assertEqual(v, control[k], msg='(2)random data mismatch')
        del storage

        return

    def test_compress(self):
        storage = Storage(filepath)
        self.assertEqual(storage.getRecordCount(), 0, msg='empty record')
        key = str(uuid.uuid4())
        value = 'test_content'
        value2 = 'test_content2'
        storage.set(key, value)
        self.assertEqual(storage.getRecordCount(), 1, msg='one record')
        storage.set(key, value + '2')
        self.assertEqual(storage.getRecordCount(), 2, msg='two record')
        storage.set(key, value2)
        self.assertEqual(storage.getRecordCount(), 3, msg='three record')
        storage.compress()
        self.assertEqual(storage.getRecordCount(), 1,
                         msg='compress, one record')
        self.assertEqual(storage[key], value2, msg='compress, correct')
        del storage

        storage = Storage(filepath)
        storage.set(key, value)
        self.assertEqual(storage.getRecordCount(), 2,
                         msg='reopen set, two record')
        self.assertEqual(storage[key], value, msg='reopen set, correct')
        del storage

        storage = Storage(filepath)
        storage.compress()
        self.assertEqual(storage.getRecordCount(), 1,
                         msg='reopen compress, two record')
        self.assertEqual(storage[key], value, msg='reopen compress, correct')
        del storage

        return

    def tearDown(self):
        os.remove(filepath)


if __name__ == '__main__':
    unittest.main()
