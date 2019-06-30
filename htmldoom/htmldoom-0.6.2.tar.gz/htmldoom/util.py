from functools import lru_cache
from html import escape
from re import sub

from htmldoom.conf import CacheConfig

__all__ = ["render", "renders", "double_quote", "fmt_prop"]


@lru_cache(maxsize=CacheConfig.MAXSIZE)
def render(*doms: object) -> str:
    """Use it to render DOM elements.
    
    Example:
        >>> from htmldoom import render
        >>> from htmldoom.elements import p
        >>> 
        >>> print(render(p()("render me"), p()("me too")))
        <p>render me</p><p>me too</p>
    """
    if not doms:
        return ""

    if len(doms) == 1:
        dom = doms[0]
        if callable(dom):
            # Forgot to call with no arguments? no worries...
            dom = dom()
        if isinstance(dom, str):
            return escape(dom)
        if isinstance(dom, bytes):
            return dom.decode()
        raise ValueError(
            f"{dom}: expected either of str, bytes, or a callable but got {type(dom)}"
        )
    return "".join(map(render, doms))


def renders(*element: bytes) -> callable:
    """Decorator for rendering dynamic elements based on given template.
    
    It improves the performance a lot by pre-compiling the templates.
    Hence, it's highly recommended to use this decorator.

    Example (syntax 1):
        >>> @renders(
        ...     e.p()("{x}"),
        ...     e.p()("another {x}"),
        ... )
        ... def render_paras(data: dict) -> dict:
        ...     return {"x": data["x"]}
        >>> 
        >>> render_paras({"x": "awesome paragraph"})
        <p>awesome paragraph</p><p>another awesome paragraph</p>
    
    Example (syntax 2):
        >>> render_paras = renders(
        ...     e.p()("{x}"),
        ...     e.p()("another {x}"),
        ... )(lambda data: {"x": data["x"]})
        >>> 
        >>> render_paras({"x": "awesome paragraph"})
        <p>awesome paragraph</p><p>another awesome paragraph</p>
    """
    template: str = render(*element)

    def wrapped(func: callable) -> str:
        def renderer(*args: object, **kwargs: object) -> str:
            return template.format(**func(*args, **kwargs))

        return renderer

    return wrapped


@lru_cache(maxsize=CacheConfig.MAXSIZE)
def double_quote(txt: str) -> str:
    """Double quote strings safely for attributes.
    
    Usage:
        >>> double_quote('abc"xyz')
        '"abc\\"xyz"'
    """
    return '"{}"'.format(txt.replace('"', '\\"'))


@lru_cache(maxsize=CacheConfig.MAXSIZE)
def fmt_prop(key: str, val: str) -> str:
    """Format a key-value pair for an HTML tag."""
    key = key.rstrip("_").replace("_", "-")
    if val is None:
        if sub("[a-zA-Z_]", "", key):
            return double_quote(key)
        return key
    return f"{key}={double_quote(val)}"
