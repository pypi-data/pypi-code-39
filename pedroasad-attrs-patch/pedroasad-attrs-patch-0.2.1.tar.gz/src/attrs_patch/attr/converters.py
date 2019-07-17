from attr.converters import *

try:
    import numpy

    def frozen_numpy_array(array):
        """A converter that allows :class:`Numpy array <numpy.ndarray>` attributes in frozen attrs_ classes. **Should be
        used with** ``hash=False``.

        Example
        -------

        .. code:: python

            from numpy import array
            import attrs_patch as attr

            @attr.s(frozen=True)
            class Struct:
                arr = attr.ib(converter=attr.frozen_numpy_array, hash=False)

            ob = Struct(arr=array([1, 2, 3, 4]))
        """
        frozen_array = array[:]
        frozen_array.flags.writeable = False
        return frozen_array


except ImportError:
    pass
