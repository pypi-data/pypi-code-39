"""Extensions of the attrs_ library. This module imports the whole attrs_ library, and imports some submodules into its
namespace, so the recommended ways of using it are

.. code::

    import attrs_patch.attr as attr

or

.. code::

    from attrs_patch import attr

Enhancements:

* :func:`attrs_patch.attr.autodoc` - class decorator for automatically documenting :class:`attr.s` classes,
* :func:`attrs_patch.attr.converters.frozen_numpy_array` - converter callable that ensures a :class:`Numpy array
  <numpy.ndarray>` is read-only,
* :func:`attrs_patch.attr.validators.nonzero` - validator that checks for non-zero numerals, and
* :func:`attrs_patch.attr.validators.positive` - validator that checks for positive numerals.

.. _attrs: http://www.attrs.org/en/stable/
"""

import attr as _attr
import inspect
import textwrap
import warnings

from . import converters as _converters, validators as _validators
from attr import *

converters = _converters
validators = _validators


def autodoc(attrs_class):
    """A class decorator that updates the docstring of an :class:`attr.s` class to include the docstrings of the
    :class:`attributes <attr.ib>`, and emits warnings when partially undocumented attributes are found.

    If the class contains any attributes, they are documented as *constructor parameters* in a *Parameters* section,
    added at the end of the class' docstring. In order to extract the most information per parameter description, this
    decorator assumes that every attribute

    * Is typed (either via the ``type`` argument, or via `PEP 526`_ type-annotations), and
    * Contains a metadata dictionary with the keys

        help:
            The string that describes the attribute, and will go in the description of the corresponding parameter.

    Default values are, of course, optional, and if provided, the parameter's description will inform this. Private
    attributes will have their names rendered correctly (without the leading underscore), and non-private attributes
    help-text will be complemented with a reminder that the parameter's value can be later accessed via an attribute
    with that name. After all, the point of attrs_ is to produce classes with transparent behavior to the final user.

    .. warning::

        Currently, there is no support for indicating that arguments are keyword-only, hashable, or validated. These and
        other exceptional conditions should be informed in the docstring.

    .. _PEP 526: https://www.python.org/dev/peps/pep-0526/
    """

    def fix_indent(docstring):
        lines = docstring.split("\n")

        if len(lines) > 1:
            for i in range(1, len(lines)):
                if lines[i]:
                    break
            parts = [
                "\n".join(lines[:i]),
                textwrap.dedent("\n".join(lines[i:])),
            ]
            result = "\n".join(p for p in parts if p)
            return result
        else:
            return lines[0]

    def param_doc(field):
        field_fn = (
            f"{attrs_class.__module__}.{attrs_class.__name__}.{field.name}"
        )

        if field.name[0] == "_":
            name = field.name[1:]
            help_complement = ""
        else:
            name = field.name
            help_complement = f"This value is accessible, after initialization, via the ``{field.name}`` attribute."

        if field.type is None:
            type = "Any"
            warnings.warn(f'Field "{field_fn}" has no declared type.')
        else:
            type = field.type.__name__

        if field.default is not _attr.NOTHING:
            optional = ", optional"
        else:
            optional = ""

        title = f"{name}: {type}{optional}"

        if "help" in field.metadata:
            description = textwrap.indent(
                textwrap.fill(
                    text=(
                        field.metadata["help"] + " " + help_complement
                    ).strip(),
                    width=96,
                ),
                prefix=" " * 4,
            )
        else:
            description = help_complement
            warnings.warn(f"Field {field_fn} not documented.")

        return title + "\n" + description

    if _attr.fields(attrs_class):
        params_section = (
            textwrap.dedent(
                """\
            Parameters
            ----------
            """
            )
            + "\n\n".join(
                param_doc(field) for field in _attr.fields(attrs_class)
            )
        )
    else:
        params_section = ""

    if attrs_class.__doc__ and params_section:
        attrs_class.__doc__ = (
            f"{fix_indent(attrs_class.__doc__).rstrip()}\n\n{params_section}"
        )
    elif params_section:
        attrs_class.__doc__ = params_section

    return attrs_class


def copy(attribute, copy_type=False, **kwargs):
    """Copy an attribute.

    Example
    -------
    .. code:: python

        import attrs_patch as attr

        @attr.s
        class A:
            a = attr.ib(default=4)
            b = attr.ib(default='five')

        @attr.s
        class B:
            a = attr.copy(attr.fields(A).a)
            b = attr.ib(default='five')

    Parameters
    ----------
    attribute: attr.Attribute
        The original attribute.

    copy_type: bool, optional
        Whether or not to copy the ``type`` argument (copied from :attr:`attrs.Attribute.type`) to :func:`attr.ib`. The
        rationale behind the default behavior (not copying), is justified by the warning below.

    **kwargs
        Override options from original attribute when calling :func:`attr.ib`.

    Returns
    -------
    copied_attribute: attr.Attribute

    Warning
    -------
    If you depend on type hint annotations (for generating data-class schemas with :mod:`marshmallow_annotations`, for
    instance), you should remember to re-annotate the copied attributes. This is necessary because Python does not
    create the ``__annotations__`` attribute unless there is at least one annotated member, which prevents us from
    adopting a more elegant solution like dropping annotations altogether, declaring types via the ``type`` parameter,
    and patching :func:`attr.s` to synchronize these with annotations (as there won't be an annotations dictionary
    available).
    """
    signature = inspect.signature(_attr.ib)

    excluded_params = ["convert", "factory"]
    if not copy_type:
        excluded_params.append("type")

    kwargs = {
        **{
            ib_param: getattr(attribute, ib_param)
            for ib_param in signature.parameters
            if ib_param not in excluded_params
        },
        **kwargs,
    }

    bound_args = signature.bind_partial(**kwargs)
    bound_args.apply_defaults()
    copied_attribute = _attr.ib(*bound_args.args, **bound_args.kwargs)

    return copied_attribute
