"""
Project: jdna
File: region
Author: Justin
Date: 2/21/17

Description: Basic functionality for defining regions of linear, circularized, or reversed
regions of a sequence.

"""
from weakref import WeakValueDictionary

from .exceptions import RegionError


def argmin(arr):
    return min(enumerate(arr), key=lambda x: x[1])[0]


def argmax(arr):
    return max(enumerate(arr), key=lambda x: x[1])[0]


#
#     __slots__ = ['_id', '_name', '_uuid']
#
#     def __init__(self, id=None, name=None):
#         self._id = id
#         self._name = name
#
#     @property
#     def id(self):
#         return self._id
#
#     @property
#     def name(self):
#         return self._name
#
#     @property
#     def uuid(self):
#         return self._uuid


def force_same_context(error=False):
    """ Wrapper that returns False or raises Error if other Region has a different context. If error==False,
    then wrapped function returns False. If error=True, then raises a RegionError. """

    def context_wrapper(fxn):
        def check_context(*args, **kwargs):
            self = args[0]
            other = args[1]
            if not self.same_context(other):
                if error:
                    raise RegionError(
                        "Cannot compare two regions if they have different sequence contexts."
                    )
                else:
                    return False
            return fxn(*args, **kwargs)

        return check_context

    return context_wrapper


class ContextAssociation(object):
    region_dict = {}

    def __init__(self, context=None, region=None):
        assert region and context
        self.region = region
        self.context = context
        self.region_dict.setdefault(id(context), WeakValueDictionary({}))[
            id(region)
        ] = self


class Context(object):
    """ Abstract sequence of a certain length, start_index and topology [Circular or linear].
    Context features are immutable."""

    __slots__ = [
        "strict",
        "start",
        "end",
        "length",
        "circular",
        "track_regions",
        "name",
        "id",
    ]

    DEFAULT_START_INDEX = 0

    def __init__(
        self,
        length,
        circular,
        name=None,
        id=None,
        start_index=DEFAULT_START_INDEX,
        strict=False,
        track_regions=False,
    ):
        """
        Context constructor

        :param length: length of context
        :type length: int
        :param circular: topology of context; True for circular contexts
        :type circular: bool
        :param start_index: the starting index offset for this context (usually 0 or 1)
        :type start_index: int
        :param strict: if strict=True, indexes beyond the maximum index, even for circular sequences, are disallowed
        :type bool
        """
        self.strict = strict
        self.start = start_index
        self.end = start_index + length - 1
        self.length = length
        self.circular = circular
        self.track_regions = track_regions
        self.name = name
        self.id = id

    def regions(self):
        """List regions associated with this context. This is tracked by a WeakValueDictionary
        in the ContextAssociation class"""
        associations = ContextAssociation.region_dict.get(id(self), {}).values()
        return [a.region for a in associations]

    @property
    def bounds(self):
        return self.start, self.end

    def span(self, x, y):
        """
        Calculates the inclusive distance between two points given the context sequence from left to right.

        ::

        e.g.
              context:    |------|
              positions:   x  y
              distance:    1234
        e.g.
              context:    |------|
              positions:   y  x
              distance:   56  1234

        :param x: position 1
        :type x: int
        :param y: position 2
        :type y: int
        :return:
        :rtype: int
        """
        x = self.t(x)
        y = self.t(y)
        mx = max(x, y)
        mn = min(x, y)
        m = mx - mn - 1
        if x > y:
            if self.circular:
                return self.length - m
            else:
                return None
        return int(m + 2)

    def within_bounds(self, pos, inclusive=True):
        """
        Whether a position is withing the bounds of acceptable indices given the context sequence.

        :param pos: position
        :type pos: int
        :param inclusive: whether to be inclusive (or exclusive)
        :type inclusive: bool
        :return: True (within bound) or False (not within bounds)
        :rtype: bool
        """
        if inclusive:
            return self.start <= pos <= self.end
        else:
            return self.start < pos < self.end

    def t(self, pos):
        """
        Alias for translate_pos
        """
        return self.translate_pos(pos)

    def translate_pos(self, pos):
        """
        Translates the index to an allowable index on a circular sequence context.
        Throws RegionError if context is linear and pos is outside of bounds.

        ::

            Context:  |-------|
            C_Index:  1.......9..11
            Pos:      11
            TransPos: 2

        :param pos:
        :type pos:
        :return:
        :rtype:
        """
        if self.circular:
            cleared = False
            while not cleared:
                cleared = True
                if pos > self.end:
                    if self.strict:
                        raise RegionError(
                            "Position {} outside of bounds for strict context.".format(
                                pos
                            )
                        )
                    else:
                        pos = pos - self.length
                        cleared = False
                if pos < self.start:
                    pos = pos + self.length
                    cleared = False
        else:
            if not self.within_bounds(pos, inclusive=True):
                raise RegionError(
                    "Position {} outside of bounds for linear context [{} {}].".format(
                        pos, self.start, self.end
                    )
                )
        return pos

    def __eq__(self, other):
        """Whether another context is functionally equivalent"""
        return (
            self.circular == other.circular
            and self.start == other.start
            and self.end == other.end
            and self.length == other.length
        )

    def __len__(self):
        """The length of the context"""
        return self.length

    def __str__(self):
        return "Context(length={length}, circular={circular}, start_index={start_index})".format(
            length=self.length, circular=self.circular, start_index=self.start
        )

    def __repr__(self):
        return str(self)


class Region(object):
    """
    Classifies an abstract region of a sequence. A region is defined by the inclusive "start" and "end"
    positions in context of an arbitrary sequence defined by the start_index and length.

    Regions can be circular or linear. For circular regions, negative indicies and indicies greater
    than the length are allowable and will be converted to appropriate indices.

    Direction of the region can be FORWARD or REVERSE or BOTH. For reversed directions, start
    and end positions should be flipped.

    Alternative start_index can be used (DEFAULT: 1) to handle sequences that start at 0 or 1.

    A new Region can be created either by defining the start and end positions or defining the
    start position and length by Region.create(length, circular) ::

        E.g. Linear Region
            length: 9
            start_index: 1
            start: 2
            end: 5
            length = 5-2+1 = 4
            Context:  |-------|
            C_Index:  1.......9
            Region:    2..4

        E.g. Circular Region
            length: 9
            start_index: 1
            start: 8
            end: 2
            length = 4
            Context:  |-------|
            C_Index:  1.......9
            Region:   .2     8.

        E.g. Calling Region(5, 7, 9, True, direction=REVERSE, start_index=1)
                  |-------|         Context
                  123456789
                  <<<<| |<<        Region Direction
                      s e          Start (s) and end (e)
    """

    __slots__ = [
        "_span",
        "_context",
        "_direction",
        "_context_association",
        "name",
        "id",
    ]

    START_INDEX = 1
    FORWARD = 1
    REVERSE = -1
    BOTH = 2

    def __init__(self, start, end, context, direction=FORWARD, name=None, id=None):
        """
        Annotates some region from a contextual sequence with either circular or linear topologies.

        All indices are INCLUSIVE.

        Making a forward region:
            Region(1, 5, context=Context(length=10, circular=False, start_index=1))

        Making a reverse region:
            Region(1, 5, direction=Region.REVERSE, context=Context(length=10, circular=False, start_index=1))

        Invalid regions:
            Region(5, 1, direction=Region.REVERSE, context=Context(length=10, circular=False, start_index=1))
                > This would imply a circular sequence context since the region starts at 5 goes in reverse through an
                origin to index 5.

            Region(5, 1, direction=Region.FORWARD, context=Context(length=10, circular=False, start_index=1))
                This would imply a circular sequence context since the region starts at 5 goes forward through an
                origin to index 1.

        :param start: start index of region
        :type start: int
        :param end: end index of region
        :type end: int
        :param context: context sequence for this region
        :type context: Context
        :param direction: Region.FORWARD or Region.REVERSE
        :type direction: int
        :param name: optional name of region
        :type name: str
        """

        self.name = name
        self.id = id
        self._direction = direction  # 1 or -1
        self._validate_direction()
        self._span = [start, end]
        self._context = context
        self._context_association = None
        if self._context.track_regions:
            self._associate_with_context(context)
        self._validate_region()
        self._span = [context.t(start), context.t(end)]

    def _associate_with_context(self, context):
        self._context_association = ContextAssociation(context=context, region=self)

    def _validate_direction(self):
        """Validates that the direction key is understood"""
        if self.direction not in [Region.FORWARD, Region.REVERSE, Region.BOTH]:
            raise RegionError(
                "Direction {} not understood. Direction must be Region.FORWARD = {}, Region.REVERSE = {},\
             or Region.BOTH = {}".format(
                    self.direction, Region.FORWARD, Region.REVERSE, Region.BOTH
                )
            )

    def _validate_region(self):
        """Validates that the start and end regions are within the bounds of its context."""
        if not self.context.circular and self.left_end > self.right_end:
            raise RegionError(
                "Left index {} cannot be greater that right index {} for linear region {}".format(
                    self.left_end, self.right_end, self
                )
            )

    @property
    def context(self):
        return self._context

    @property
    def start_index(self):
        """The minimum index for this region (defined by context). Alias of bounds_start"""
        return self.bounds_start

    @property
    def bounds_start(self):
        """The maximum index for the context of this region"""
        return self.context.start

    @property
    def bounds_end(self):
        """The maximum index for the context of this region"""
        return self.context.end

    @property
    def context_length(self):
        """The length of the context this region is in"""
        return self.context.length

    @property
    def length(self):
        """The length of this region"""
        return self.context.span(self.left_end, self.right_end)

    @property
    def circular(self):
        return self.context.circular

    def reindex(self, i):
        """Reindex this region."""
        copied = self.copy()
        delta = i - self.context.start
        copied.abs_shift(-delta)
        copied._validate_region()
        return copied

    # def reset_starting_index(self, i):
    #     """Return a copy of this region under a context that starts
    #     at a new starting index."""
    #     delta = i - self.context.start
    #     new_context = deepcopy(self.context)
    #     new_context.start = i
    #     return Region(
    #         self.start + delta,
    #         self.end + delta,
    #         new_context,
    #         self.direction,
    #         self.name,
    #         self.id,
    #     )

    def abs_shift(self, i):
        """Shift the region absolutely."""
        new_span = [self.context.t(_x + i) for _x in self._span]
        self._span = new_span
        self._validate_region()

    def shift(self, i):
        """Shift the region. If reverse, will shift in the negative direction."""
        if self.is_reverse():
            self.abs_shift(-i)
        else:
            self.abs_shift(i)

    @property
    def start(self):
        """
        Gets the start position of the region. Internally
        reverses the start and end positions if direction is
        reversed.

        :return:
        """
        if self.is_forward():
            return self._span[0]
        else:
            return self._span[1]

    @start.setter
    def start(self, x):
        """
        Sets the start position of the region. Internally
        reverses the start and end positions if direction is
        reversed.

        :return:
        """
        pos = self.context.t(x)
        if self.is_forward():
            self._span[0] = pos
        else:
            self._span[1] = pos

    @property
    def end(self):
        """
        Gets the end position of the region. Internally
        reverses the start and end positions if direction is
        reversed.

        :return:
        """
        if self.is_forward():
            return self._span[1]
        else:
            return self._span[0]

    @end.setter
    def end(self, x):
        """
        Sets the end position of the region. Internally
        reverses the start and end positions if direction is
        reversed.

        :return:
        """
        pos = self.context.t(x)
        if self.is_forward():
            self._span[1] = pos
        else:
            self._span[0] = pos

    @property
    def direction(self):
        """Direction of the region"""
        return self._direction

    @property
    def left_end(self):
        """
        Returns left end stop

        e.g. ::

            |--------|
            ^L       ^R

            --|        |---
              ^R       ^L

        :return: index of left region end stop
        :rtype: int
        """
        return self._span[0]

    @property
    def right_end(self):
        """
        Returns left end stop
        e.g. ::

            |--------|
            ^L       ^R

            --|        |---
              ^R       ^L
        :return: index of right region end stop
        :rtype: int
        """
        return self._span[1]

    def set_ends(self, x, y):
        self._span[0] = x
        self._span[1] = y
        if self.spans_origin() and not self.circular:
            raise RegionError(
                "Invalid region. Linear region cannot span origin. {}".format(self)
            )

    @left_end.setter
    def left_end(self, x):
        """Sets the left end stop"""
        self._span[0] = self.context.t(x)
        if self.spans_origin() and not self.circular:
            raise RegionError(
                "Invalid region. Linear region cannot span origin. {}".format(self)
            )

    @right_end.setter
    def right_end(self, x):
        """Sets the left end stop"""
        self._span[1] = self.context.t(x)
        if self.spans_origin() and not self.circular:
            raise RegionError(
                "Invalid region. Linear region cannot span origin. {}".format(self)
            )

    def is_forward(self):
        """Whether this region is pointed 'forward'"""
        return self.direction in [Region.FORWARD]

    def is_reverse(self):
        """Whether this region is pointed in 'reverse'"""
        return self.direction in [Region.REVERSE]

    def spans_origin(self):
        """Returns whether region spans origin. Agnostic as to self.circular. """
        return self._span[0] > self._span[1]

    def within_region(self, pos, inclusive=True):
        """
        Returns whether a position is within the region. Handles circular regions.

        :param pos: index
        :type pos: int | list
        :param inclusive: whether to be inclusive (or exclusive)
        :type inclusive: bool
        :return: whether index is within region
        :rtype: bool
        """
        if isinstance(pos, int):
            pos = [pos]
        if self.spans_origin():
            v = [(self._span[0], self.bounds_end), (self.bounds_start, self._span[1])]
        else:
            v = [self._span]
        if inclusive:
            for p in pos:
                if not any([i[0] <= p <= i[1] for i in v]):
                    return False
        else:
            for p in pos:
                if not any([i[0] < p < i[1] for i in v]):
                    return False
        return True

    def sub_region(self, left, right):
        """
        Creates a sub region with the same context_length and direction as this region
        with inclusive span.

        :param left: left span (inclusive)
        :param right: right span (inclusive)
        :return:
        """

        if self.within_region(left, inclusive=True) and self.within_region(
            right, inclusive=True
        ):
            r = self.copy()
            r._span = [left, right]
            r._validate_region()
            return r
        else:
            raise RegionError(
                "Sub region bounds [{}-{}] outside of Region bounds [{}-{}]".format(
                    left, right, self._span[0], self._span[1]
                )
            )

    def same_context(self, other):
        """
        Compares the context properties (length, bounds_start, bounds_ends) between two Regions.

        :param other: The other Region
        :type other: Region
        :return: Whether the other region's context sequence is the same length and has same start_index as this Region
        :rtype: bool
        """
        return self.context == other.context

    # TODO: Why not __copy__?
    def copy(self):
        """
        Creates another region with identical properties.

        :return: Copied region
        :rtype: Region
        """
        # s, e = self.start, self.end
        # if self.direction is Region.REVERSE:
        #     s, e = self.end, self.start
        return self.__class__(
            self._span[0],
            self._span[1],
            self.context,
            direction=self.direction,
            name=self.name,
        )

    @force_same_context(error=True)
    def get_overlap(self, other):
        """
        Returns a region representing the overlap with another region
        e.g. ::

                |--------|         self
                      |--------|   other
                      |--| << This is returned

        :param other: other Region
        :type other: Region
        :return: Region if there is an overlap, None if there is no overlap
        :rtype: Region
        """
        if self.end_overlaps_with(other):
            r = self.copy()
            r._direction = Region.FORWARD
            r.start = other.left_end
            r.end = self.right_end
            return r
        else:
            return None

    @force_same_context(error=True)
    def equivalent_location(self, other):
        return other.start == self.start and other.end == self.end

    @force_same_context(error=True)
    def encompasses(self, other, inclusive=True):
        return self.within_region(other._span, inclusive=inclusive)

    @force_same_context(error=True)
    def end_overlaps_with(self, other):
        """
         Whether this region overlaps the next region it this regions end. Other needs some kind of overhang to
         return True.
         False if context is different. ::

             True
                 self   |------|
                 other      |-------|

             False
                 self         |------|
                 other  |-------|

             False
                 self   |------|
                 other    |----|

             True
                 self   |------|
                 other    |-----|
        :param other: other Region
        :type other: Region
        :return: True if region ends overlaps, False if otherwise.
        :rtype: bool
        """

        return self.within_region(
            other.left_end, inclusive=True
        ) and not self.encompasses(other)

    @force_same_context(error=True)
    def get_gap(self, other):
        """
        Gets the gap region. Returns None if there is no gap or Regions are not consecutive. Always are in the
        forward direction. ::

            Context:        |----------------------|
            This Region:        |-------|
            Other Region:                    |------|
            Gap:                         |==|


            r1:         ----|              |-----
            r2:                  |----|
            r1.get_gap(r2)   |==|
            r2.get_gap(r1)             |==|

        :param other: other Region
        :type other: Region
        :return: gap as a Region
        :rtype: Region
        """
        if self.consecutive_with(other):
            return None
        if not self.within_region(other.left_end) or self is other:
            x = self.right_end + 1
            y = other.left_end - 1
            if x > y and not self.circular:
                return None
            else:
                r = self.copy()
                r.right_end = other.left_end - 1
                r.left_end = self.right_end + 1
                return r
        else:
            return None

    @force_same_context(error=True)
    def get_gap_span(self, other):
        """
        Returns span of gap. Returns 0 if regions are consecutive, negative if regions overlap, positive for gaps.

        e.g. ::

            +        |--------|***|-----| (length of three gap)

            -        |------***
                            ***-----|
                            *** (length of three overhang)

            0        |----||----| (0 for consecutive)

            None     |--------|
                        |-----| (None

        :param other:
        :type other:
        :return: span of gap (0 for consecutive, - for overlap, + for gap)
        :rtype: int
        """
        overlap = self.get_overlap(other)
        gap = self.get_gap(other)
        cons = self.consecutive_with(other)
        if cons:
            return 0
        if overlap is not None:
            return -overlap.length
        if gap is not None:
            return gap.length

    # @force_same_context(error=True)
    # def no_overlap(self, other):
    #     """
    #     Returns True if there is no overlap with the other Region
    #
    #     :param other: Other Region
    #     :type other: Region
    #     :return: if there is no overlap
    #     :rtype: bool
    #     """
    #     return not self.within_region(other.start, inclusive=True) \
    #            and not other.within_region(self.end, inclusive=True)

    @force_same_context(error=True)
    def consecutive_with(self, other):
        """
        Returns whether the right_end is consecutive with the other region's left_end ::

            |-------||----|

        :param other: other Region
        :type other: Region
        :return: True if other region is consecutive with this region
        :rtype: bool
        """
        try:
            return self.right_end == self.context.t(other.left_end - 1)
        except RegionError:
            return False

    @force_same_context(error=True)
    def fuse(self, other, inplace=True):
        """
        Fuses this region with other region. If regions are not consecutive, returns None ::

            |-----------| (1)
                         |-----------| (2)
            |------------------------| (1 modified)

        :param other: other Region
        :type other: Region
        :return: this Region (self, modified by extension by other Region)
        :rtype: Region
        """
        if self.consecutive_with(other):
            new_region = self
            if not inplace:
                new_region = self.copy()
            new_region.right_end = other.right_end
            return new_region
        else:
            return None

    def extend_start(self, x):
        """
        Extends the start by x amount. Retracts start if negative. Raises error if retracts past end.

        e.g. extend start by +4 ::

                s          e
                |----------|
            |<<<|----------|
            |--------------|

        :param x:
        :type x:
        :return:
        :rtype:
        """
        if x <= -self.length:
            raise RegionError("Cannot retract past end.")
        elif x >= self.context.length - self.length + 1:
            raise RegionError("Cannot extend around origin.")
        if self.is_forward():
            self.left_end -= x
        else:
            self.right_end += x

    def extend_end(self, x):
        """
        Extends the end by x amount. Retracts end if negative. Raises error if retracts past start.

        e.g. extend end by +4 ::

            s          e
            |----------|
            |----------|>>>|
            |--------------|

        :param x:
        :type x:
        :return:
        :rtype:
        """
        if x <= -self.length:
            raise RegionError("Cannot retract past end")
        elif x >= self.context.length - self.length + 1:
            raise RegionError("Cannot extend around origin.")
        if self.is_reverse():
            self.left_end -= x
        else:
            self.right_end += x

    def set_forward(self):
        """ Reverses direction of region if region is reverse """
        if not self.is_forward():
            self.reverse_direction()

    def set_reverse(self):
        """ Reverses direction of region if region is forward """
        if self.is_forward():
            self.reverse_direction()

    def reverse_direction(self):
        """ Reverses the direction of this region. Reverses the start and end indices. """
        if self.is_forward():
            self._direction = Region.REVERSE
        else:
            self._direction = Region.FORWARD
        return self.direction

    def __getitem__(self, val):
        if isinstance(val, int):
            # get position relative to this region
            try:
                if val >= 0:
                    x = self.context.t(self.left_end + val)
                else:
                    x = self.context.t(self.right_end + val + 1)
            except RegionError:
                raise IndexError(
                    "Invalid region index '{}'. Maximum index is {}.".format(
                        val, len(self) - 1
                    )
                )
            if not self.within_region(x, inclusive=True):
                raise IndexError(
                    "Invalid region index '{}'. Maximum index is {}.".format(
                        val, len(self) - 1
                    )
                )
            return x
        elif issubclass(type(val), slice):
            if val.step:
                raise ValueError(
                    "{} slicing does not support step".format(self.__class__.__name__)
                )
            if val.start:
                i = self[val.start]
            else:
                i = self._span[0]

            if val.stop:
                j = self[val.stop - 1]
            else:
                j = self._span[1]
            return self.sub_region(i, j)
        else:
            raise ValueError(
                "Unable to slice {} with a '{}' type".format(
                    self.__class__.__name__, type(val)
                )
            )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __len__(self):
        return self.length

    def __str__(self):
        return "Region({span}, name={name}, direction={direction}, context={context})".format(
            span=tuple(self._span),
            direction=self.direction,
            context=self.context,
            name=self.name,
        )

    def __repr__(self):
        return str(self)
