from plotly.basedatatypes import BaseTraceHierarchyType as _BaseTraceHierarchyType
import copy as _copy


class Marker(_BaseTraceHierarchyType):

    # color
    # -----
    @property
    def color(self):
        """
        Sets the marker color of all intermediate sums and total
        values.
    
        The 'color' property is a color and may be specified as:
          - A hex string (e.g. '#ff0000')
          - An rgb/rgba string (e.g. 'rgb(255,0,0)')
          - An hsl/hsla string (e.g. 'hsl(0,100%,50%)')
          - An hsv/hsva string (e.g. 'hsv(0,100%,100%)')
          - A named CSS color:
                aliceblue, antiquewhite, aqua, aquamarine, azure,
                beige, bisque, black, blanchedalmond, blue,
                blueviolet, brown, burlywood, cadetblue,
                chartreuse, chocolate, coral, cornflowerblue,
                cornsilk, crimson, cyan, darkblue, darkcyan,
                darkgoldenrod, darkgray, darkgrey, darkgreen,
                darkkhaki, darkmagenta, darkolivegreen, darkorange,
                darkorchid, darkred, darksalmon, darkseagreen,
                darkslateblue, darkslategray, darkslategrey,
                darkturquoise, darkviolet, deeppink, deepskyblue,
                dimgray, dimgrey, dodgerblue, firebrick,
                floralwhite, forestgreen, fuchsia, gainsboro,
                ghostwhite, gold, goldenrod, gray, grey, green,
                greenyellow, honeydew, hotpink, indianred, indigo,
                ivory, khaki, lavender, lavenderblush, lawngreen,
                lemonchiffon, lightblue, lightcoral, lightcyan,
                lightgoldenrodyellow, lightgray, lightgrey,
                lightgreen, lightpink, lightsalmon, lightseagreen,
                lightskyblue, lightslategray, lightslategrey,
                lightsteelblue, lightyellow, lime, limegreen,
                linen, magenta, maroon, mediumaquamarine,
                mediumblue, mediumorchid, mediumpurple,
                mediumseagreen, mediumslateblue, mediumspringgreen,
                mediumturquoise, mediumvioletred, midnightblue,
                mintcream, mistyrose, moccasin, navajowhite, navy,
                oldlace, olive, olivedrab, orange, orangered,
                orchid, palegoldenrod, palegreen, paleturquoise,
                palevioletred, papayawhip, peachpuff, peru, pink,
                plum, powderblue, purple, red, rosybrown,
                royalblue, rebeccapurple, saddlebrown, salmon,
                sandybrown, seagreen, seashell, sienna, silver,
                skyblue, slateblue, slategray, slategrey, snow,
                springgreen, steelblue, tan, teal, thistle, tomato,
                turquoise, violet, wheat, white, whitesmoke,
                yellow, yellowgreen

        Returns
        -------
        str
        """
        return self["color"]

    @color.setter
    def color(self, val):
        self["color"] = val

    # line
    # ----
    @property
    def line(self):
        """
        The 'line' property is an instance of Line
        that may be specified as:
          - An instance of plotly.graph_objs.waterfall.totals.marker.Line
          - A dict of string/value properties that will be passed
            to the Line constructor
    
            Supported dict properties:
                
                color
                    Sets the line color of all intermediate sums
                    and total values.
                width
                    Sets the line width of all intermediate sums
                    and total values.

        Returns
        -------
        plotly.graph_objs.waterfall.totals.marker.Line
        """
        return self["line"]

    @line.setter
    def line(self, val):
        self["line"] = val

    # property parent name
    # --------------------
    @property
    def _parent_path_str(self):
        return "waterfall.totals"

    # Self properties description
    # ---------------------------
    @property
    def _prop_descriptions(self):
        return """\
        color
            Sets the marker color of all intermediate sums and
            total values.
        line
            plotly.graph_objects.waterfall.totals.marker.Line
            instance or dict with compatible properties
        """

    def __init__(self, arg=None, color=None, line=None, **kwargs):
        """
        Construct a new Marker object
        
        Parameters
        ----------
        arg
            dict of properties compatible with this constructor or
            an instance of
            plotly.graph_objs.waterfall.totals.Marker
        color
            Sets the marker color of all intermediate sums and
            total values.
        line
            plotly.graph_objects.waterfall.totals.marker.Line
            instance or dict with compatible properties

        Returns
        -------
        Marker
        """
        super(Marker, self).__init__("marker")

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
The first argument to the plotly.graph_objs.waterfall.totals.Marker 
constructor must be a dict or 
an instance of plotly.graph_objs.waterfall.totals.Marker"""
            )

        # Handle skip_invalid
        # -------------------
        self._skip_invalid = kwargs.pop("skip_invalid", False)

        # Import validators
        # -----------------
        from plotly.validators.waterfall.totals import marker as v_marker

        # Initialize validators
        # ---------------------
        self._validators["color"] = v_marker.ColorValidator()
        self._validators["line"] = v_marker.LineValidator()

        # Populate data dict with properties
        # ----------------------------------
        _v = arg.pop("color", None)
        self["color"] = color if color is not None else _v
        _v = arg.pop("line", None)
        self["line"] = line if line is not None else _v

        # Process unknown kwargs
        # ----------------------
        self._process_kwargs(**dict(arg, **kwargs))

        # Reset skip_invalid
        # ------------------
        self._skip_invalid = False


from plotly.graph_objs.waterfall.totals import marker
