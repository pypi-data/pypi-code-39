from unittest import TestCase
from pkg.decorators import exception


class DecoratorsTests(TestCase):

    @exception(safe=True, default=1000)
    def method(self, error=False):
        if not error:
            return 10
        else:
            raise ValueError("Some error")

    def test_exception_as_safe(self):
        value = self.method(error=True)
        normal_value = self.method()
        assert value == 1000
        assert normal_value == 10

