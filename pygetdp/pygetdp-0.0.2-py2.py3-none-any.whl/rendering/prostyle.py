"""
    prostyle.py
    ~~~~~~~~~~~~~~~~~~~~~~

    A style for highlighting GetDP .pro files
"""


from pygments.style import Style
from pygments.token import (
    Comment,
    Error,
    Generic,
    Keyword,
    Literal,
    Name,
    Number,
    Operator,
    Other,
    Punctuation,
    String,
    Text,
    Whitespace,
)


class ProStyle(Style):
    """
    This style mimics the Monokai color scheme.
    """

    background_color = "#272822"
    highlight_color = "#49483e"

    styles = {
        # No corresponding class for the following:
        Text: "#f8f8f2",  # class:  ''
        Whitespace: "",  # class: 'w'
        Error: "#b84c39 bg:#2b0303",  # class: 'err'
        Other: "",  # class 'x'
        Comment: "#75715e",  # class: 'c'
        Comment.Multiline: "",  # class: 'cm'
        Comment.Preproc: "",  # class: 'cp'
        Comment.Single: "",  # class: 'c1'
        Comment.Special: "",  # class: 'cs'
        Keyword: "#91ad86",  # class: 'k'
        Keyword.Constant: "",  # class: 'kc'
        Keyword.Declaration: "",  # class: 'kd'
        Keyword.Namespace: "#da8b7d",  # class: 'kn'
        Keyword.Pseudo: "",  # class: 'kp'
        Keyword.Reserved: "",  # class: 'kr'
        Keyword.Type: "",  # class: 'kt'
        Operator: "#da8b7d",  # class: 'o'
        Operator.Word: "",  # class: 'ow' - like keywords
        Punctuation: "#f8f8f2",  # class: 'p'
        Name: "#f8f8f2",  # class: 'n'
        Name.Attribute: "#d0c36d",  # class: 'na' - to be revised
        Name.Builtin: "",  # class: 'nb'
        Name.Builtin.Pseudo: "",  # class: 'bp'
        Name.Class: "#d0c36d",  # class: 'nc' - to be revised
        Name.Constant: "#77a1aa",  # class: 'no' - to be revised
        Name.Decorator: "#d0c36d",  # class: 'nd' - to be revised
        Name.Entity: "",  # class: 'ni'
        Name.Exception: "#d0c36d",  # class: 'ne'
        Name.Function: "#d0c36d",  # class: 'nf'
        Name.Property: "",  # class: 'py'
        Name.Label: "",  # class: 'nl'
        Name.Namespace: "",  # class: 'nn' - to be revised
        Name.Other: "#d0c36d",  # class: 'nx'
        Name.Tag: "#da8b7d",  # class: 'nt' - like a keyword
        Name.Variable: "",  # class: 'nv' - to be revised
        Name.Variable.Class: "",  # class: 'vc' - to be revised
        Name.Variable.Global: "",  # class: 'vg' - to be revised
        Name.Variable.Instance: "",  # class: 'vi' - to be revised
        Number: "#b97d8d",  # class: 'm'
        Number.Float: "",  # class: 'mf'
        Number.Hex: "",  # class: 'mh'
        Number.Integer: "",  # class: 'mi'
        Number.Integer.Long: "",  # class: 'il'
        Number.Oct: "",  # class: 'mo'
        Literal: "#b97d8d",  # class: 'l'
        Literal.Date: "#e6bb74",  # class: 'ld'
        String: "#e6bb74",  # class: 's'
        String.Backtick: "",  # class: 'sb'
        String.Char: "",  # class: 'sc'
        String.Doc: "",  # class: 'sd' - like a comment
        String.Double: "",  # class: 's2'
        String.Escape: "#b97d8d",  # class: 'se'
        String.Heredoc: "",  # class: 'sh'
        String.Interpol: "",  # class: 'si'
        String.Other: "",  # class: 'sx'
        String.Regex: "",  # class: 'sr'
        String.Single: "",  # class: 's1'
        String.Symbol: "",  # class: 'ss'
        Generic: "",  # class: 'g'
        Generic.Deleted: "#da8b7d",  # class: 'gd',
        Generic.Emph: "italic",  # class: 'ge'
        Generic.Error: "",  # class: 'gr'
        Generic.Heading: "",  # class: 'gh'
        Generic.Inserted: "#d0c36d",  # class: 'gi'
        Generic.Output: "",  # class: 'go'
        Generic.Prompt: "",  # class: 'gp'
        Generic.Strong: "bold",  # class: 'gs'
        Generic.Subheading: "#75715e",  # class: 'gu'
        Generic.Traceback: "",  # class: 'gt'
    }
