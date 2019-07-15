import unittest
from absstream.stream import Stream


class Test(unittest.TestCase):
    def test_stream(self):
        with self.assertRaises(TypeError):
            Stream(None)

        s = Stream('123')
        self.assertEqual(len(s), 3)
        s = Stream([1, 2, 3])
        self.assertEqual(len(s), 3)

        it = iter(s)
        self.assertEqual(next(it), 1)
        self.assertEqual(next(it), 2)
        self.assertEqual(next(it), 3)
        with self.assertRaises(StopIteration):
            next(it)

        self.abs_test('123')
        self.abs_test(['1', '2', '3'])
        self.abs_test(('1', '2', '3'))

    def abs_test(self, src):
        s = Stream(src)
        self.assertEqual(s.eof(), False)
        self.assertEqual(s.index, 0)
        self.assertEqual(s.get(), '1')
        self.assertEqual(s.index, 1)
        self.assertEqual(s.get(), '2')
        self.assertEqual(s.index, 2)
        self.assertEqual(s.get(), '3')
        self.assertEqual(s.index, 3)
        self.assertEqual(s.get(), Stream.EOF)
        self.assertEqual(s.eof(), True)

        s.prev()
        self.assertEqual(s.index, 2)
        self.assertEqual(s.cur(), '3')

        s.prev()
        self.assertEqual(s.index, 1)
        self.assertEqual(s.cur(), '2')

        s.next()
        self.assertEqual(s.index, 2)
        self.assertEqual(s.cur(), '3')

        s.index = 0
        self.assertEqual(s.cur(), '1')
        self.assertEqual(s.cur(1), '2')
        self.assertEqual(s.cur(2), '3')
        self.assertEqual(s.cur(3), Stream.EOF)

        s.index = 2
        self.assertEqual(s.cur(), '3')
        self.assertEqual(s.cur(-1), '2')
        self.assertEqual(s.cur(-2), '1')
        self.assertEqual(s.cur(-3), Stream.EOF)

        with self.assertRaises(TypeError):
            s.cur(None)

        with self.assertRaises(TypeError):
            s.index = None
    


