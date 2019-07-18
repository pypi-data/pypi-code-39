import unittest

from CachedFunc import CacheManager, NotInCacheError
from CachedFunc.CacheRepos import MemRepo


class TestCacheManager(unittest.TestCase):
    def test_manageRepos(self):
        manager = CacheManager()
        name = manager.add_repo(MemRepo())
        self.assertIsNotNone(name)

    def test_registerWrapper(self):
        manager = CacheManager()
        manager.add_repo(MemRepo())
        called_times = 0

        @manager.register
        def func(a, b, c=3, *args, **kwargs):
            nonlocal called_times
            called_times += 1
            return a + b + c + sum(args) + sum(kwargs.values())

        # they should be all the same
        func(1, 2, 3)
        func(1, 2)
        func(1, b=2)
        self.assertEqual(called_times, 1)

        self.assertRaises(TypeError, func, 1)
        self.assertEqual(func(1, 2, 3, 4, e=5), 15)

    def test_raiseNotInCacheError(self):
        manager = CacheManager()
        manager.add_repo(MemRepo())
        self.assertRaises(NotInCacheError, manager.get, '123')

    def test_repoUpdate(self):
        manager = CacheManager()
        memRepo1 = MemRepo()
        memRepo2 = MemRepo()
        memRepo3 = MemRepo()

        name1 = manager.add_repo(memRepo1)
        name2 = manager.add_repo(memRepo2)
        name3 = manager.add_repo(memRepo3)
        called_times = 0

        @manager.register
        def func(a, b, c=3, *args, **kwargs):
            nonlocal called_times
            called_times += 1
            return a + b + c + sum(args) + sum(kwargs.values())

        # In fact, the real return value should be 6, we'll see if the key is correct.
        # TODO: I should find some way to get the real key but not use such a magic string.
        key = 'func|{"a": 1, "b": 2, "c": 3}|[]|{}'
        memRepo2[key] = 10
        self.assertEqual(func(1, 2, 3), 10)
        self.assertTrue(key in memRepo1)
        self.assertFalse(key in memRepo3)