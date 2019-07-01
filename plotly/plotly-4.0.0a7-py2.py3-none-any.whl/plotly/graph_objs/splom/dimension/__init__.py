from plotly.basedatatypes import BaseTraceHierarchyType as _BaseTraceHierarchyType
import copy as _copy


class Axis(_BaseTraceHierarchyType):

    # matches
    # -------
    @property
    def matches(self):
        """
        Determines whether or not the x & y axes generated by this
        dimension match. Equivalent to setting the `matches` axis
        attribute in the layout with the correct axis id.
    
        The 'matches' property must be specified as a bool
        (either True, or False)

        Returns
        -------
        bool
        """
        return self["matches"]

    @matches.setter
    def matches(self, val):
        self["matches"] = val

    # type
    # ----
    @property
    def type(self):
        """
        Sets the axis type for this dimension's generated x and y axes.
        Note that the axis `type` values set in layout take precedence
        over this attribute.
    
        The 'type' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['linear', 'log', 'date', 'category']

        Returns
        -------
        Any
        """
        return self["type"]

    @type.setter
    def type(self, val):
        self["type"] = val

    # property parent name
    # --------------------
    @property
    def _parent_path_str(self):
        return "splom.dimension"

    # Self properties description
    # ---------------------------
    @property
    def _prop_descriptions(self):
        return """\
        matches
            Determines whether or not the x & y axes generated by
            this dimension match. Equivalent to setting the
            `matches` axis attribute in the layout with the correct
            axis id.
        type
            Sets the axis type for this dimension's generated x and
            y axes. Note that the axis `type` values set in layout
            take precedence over this attribute.
        """

    def __init__(self, arg=None, matches=None, type=None, **kwargs):
        """
        Construct a new Axis object
        
        Parameters
        ----------
        arg
            dict of properties compatible with this constructor or
            an instance of plotly.graph_objs.splom.dimension.Axis
        matches
            Determines whether or not the x & y axes generated by
            this dimension match. Equivalent to setting the
            `matches` axis attribute in the layout with the correct
            axis id.
        type
            Sets the axis type for this dimension's generated x and
            y axes. Note that the axis `type` values set in layout
            take precedence over this attribute.

        Returns
        -------
        Axis
        """
        super(Axis, self).__init__("axis")

        # Validate arg
        # ------------
        if arg is None:
            arg = {}
        elif isinstance(arg, self.__class__):
            arg = arg.to_plotly_json()
        elif isinstance(arg, dict):
            arg = _copy.copy(arg)
        else:
            raise ValueError(
                """\
The first argument to the plotly.graph_objs.splom.dimension.Axis 
constructor must be a dict or 
an instance of plotly.graph_objs.splom.dimension.Axis"""
            )

        # Handle skip_invalid
        # -------------------
        self._skip_invalid = kwargs.pop("skip_invalid", False)

        # Import validators
        # -----------------
        from plotly.validators.splom.dimension import axis as v_axis

        # Initialize validators
        # ---------------------
        self._validators["matches"] = v_axis.MatchesValidator()
        self._validators["type"] = v_axis.TypeValidator()

        # Populate data dict with properties
        # ----------------------------------
        _v = arg.pop("matches", None)
        self["matches"] = matches if matches is not None else _v
        _v = arg.pop("type", None)
        self["type"] = type if type is not None else _v

        # Process unknown kwargs
        # ----------------------
        self._process_kwargs(**dict(arg, **kwargs))

        # Reset skip_invalid
        # ------------------
        self._skip_invalid = False
