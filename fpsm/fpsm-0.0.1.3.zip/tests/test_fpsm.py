import unittest
import fpsm


class TestFpsm(unittest.TestCase):
    def test_head(self):
        res = fpsm.head([1, 2, 3, 4, 5])
        ans = 1
        self.assertEqual(res, ans)

    def test_tail(self):
        res = fpsm.tail([1, 2, 3, 4, 5])
        ans = [2, 3, 4, 5]
        self.assertEqual(res, ans)

    def test_init(self):
        res = fpsm.init([1, 2, 3, 4, 5])
        ans = [1, 2, 3, 4]
        self.assertEqual(res, ans)

    def test_last(self):
        res = fpsm.last([1, 2, 3, 4, 5])
        ans = 5
        self.assertEqual(res, ans)

    def test_take(self):
        res = fpsm.take(3, [1, 2, 3, 4, 5])
        ans = [1, 2, 3]
        self.assertEqual(res, ans)

    def test_null(self):
        res = fpsm.null([])
        ans = True
        self.assertEqual(res, ans)

    def test_foldl(self):
        res = fpsm.foldl(lambda x, y: 2 * x + y, [1, 1, 0])
        ans = 6
        self.assertEqual(res, ans)

    def test_foldr(self):
        res = fpsm.foldr(lambda x, y: x + y * 2, [1, 0, 1])
        ans = 5
        self.assertEqual(res, ans)

    def test_concat(self):
        res = fpsm.concat([1, 2, 3], [4, 5, 6])
        ans = list(range(1, 7))
        self.assertEqual(res, ans)

    def test_concat_map(self):
        res = fpsm.concat_map(lambda x: [0, x], [1, 2], [3, 4])
        ans = [0, 1, 0, 2, 0, 3, 0, 4]
        self.assertEqual(res, ans)

    def test_product(self):
        res = fpsm.product(range(1, 6))
        ans = 120
        self.assertEqual(res, ans)

    def test_drop(self):
        res = fpsm.drop(2, range(5))
        ans = [2, 3, 4]
        self.assertEqual(res, ans)

    def test_split_at(self):
        res = fpsm.split_at(3, range(5))
        ans = [[0, 1, 2], [3, 4]]
        self.assertEqual(res, ans)

    def test_span(self):
        res = fpsm.span(lambda x: x < 4, [1, 3, 4, 5, 1, 2])
        ans = [[1, 3], [4, 5, 1, 2]]
        self.assertEqual(res, ans)

    def test_elem(self):
        res = fpsm.elem(3, range(5))
        ans = True
        self.assertEqual(res, ans)

    def test_not_elem(self):
        res = fpsm.not_elem(3, range(5))
        ans = False
        self.assertEqual(res, ans)

    def test_flatten(self):
        res = fpsm.flatten([range(2), range(3)])
        ans = [0, 1, 0, 1, 2]
        self.assertEqual(res, ans)

    def test_infinite(self):
        inf = fpsm.infinite(2)
        res = [next(inf) for _ in range(5)]
        ans = [2, 3, 4, 5, 6]
        self.assertEqual(res, ans)


if __name__ == '__main__':
    unittest.main()
