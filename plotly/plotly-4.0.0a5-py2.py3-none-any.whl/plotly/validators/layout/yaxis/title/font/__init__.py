import _plotly_utils.basevalidators


class SizeValidator(_plotly_utils.basevalidators.NumberValidator):
    def __init__(
        self, plotly_name="size", parent_name="layout.yaxis.title.font", **kwargs
    ):
        super(SizeValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "ticks"),
            min=kwargs.pop("min", 1),
            role=kwargs.pop("role", "style"),
            **kwargs
        )


import _plotly_utils.basevalidators


class FamilyValidator(_plotly_utils.basevalidators.StringValidator):
    def __init__(
        self, plotly_name="family", parent_name="layout.yaxis.title.font", **kwargs
    ):
        super(FamilyValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "ticks"),
            no_blank=kwargs.pop("no_blank", True),
            role=kwargs.pop("role", "style"),
            strict=kwargs.pop("strict", True),
            **kwargs
        )


import _plotly_utils.basevalidators


class ColorValidator(_plotly_utils.basevalidators.ColorValidator):
    def __init__(
        self, plotly_name="color", parent_name="layout.yaxis.title.font", **kwargs
    ):
        super(ColorValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "ticks"),
            role=kwargs.pop("role", "style"),
            **kwargs
        )
