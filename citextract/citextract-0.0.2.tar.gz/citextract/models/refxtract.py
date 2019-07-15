"""RefXtract package."""
import torch
import torch.nn as nn

from citextract.utils.model import load_model_params


class BiRNN(nn.Module):
    """Bidirectional RNN model."""

    def __init__(self, input_size, hidden_size, num_layers=1, num_classes=2, device=None):
        """Initialize the Bidirectional RNN model.

        Parameters
        ----------
        input_size : int
            The number of input neurons.
        hidden_size : int
            The number of hidden neurons.
        num_layers : int
            The number of layers.
        num_classes : int
            The number of output classes.
        device : torch.device
            The device to run on.
        """
        super(BiRNN, self).__init__()
        self.device = device
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_size * 2, num_classes)

    def forward(self, x):
        """Forward-propagate the given input.

        Parameters
        ----------
        x : torch.Tensor
            The tensor of size [batch_size, sequence_length, input_size] to forward-propagate.

        Returns
        -------
        torch.Tensor
            The output, which has a shape of [batch_size, sequence_length, num_classes].
        """
        # Set initial states
        h0_variable = torch.zeros(self.num_layers * 2, x.size(0), self.hidden_size).to(self.device)
        c0_variable = torch.zeros(self.num_layers * 2, x.size(0), self.hidden_size).to(self.device)

        # Forward propagate LSTM
        out, _ = self.lstm(x, (h0_variable, c0_variable))

        # Decode the hidden state of the last time step
        out = nn.Softmax(dim=2)(self.fc(out))
        return out


class RefXtractText:
    """Simple helper class which contains the text and char indices of a given input."""

    def __init__(self, text, idx):
        """Initialize the RefXtractText object.

        Parameters
        ----------
        text : str
            The initial text that was used.
        idx : torch.Tensor
            The tensor containing the character indices.
        """
        self.text = text
        self.idx = idx


class RefXtractPreprocessor:
    """Preprocessor class for preprocessing textual data."""

    def __init__(self, device=None):
        """Initialize the preprocessor.

        Parameters
        ----------
        device : torch.device
            The device to use.
        """
        char_map = dict({
            '0': '0123456789',
            ',': ',',
            ':': ':;',
            '"': '“”"\'',
            '#': '#',
            '[': '[',
            '(': '(',
            '{': '{',
            ']': ']',
            ')': ')',
            '}': '}',
            '.': '.',
            '-': '-',
            '+': '+',
            '_': '_',
            '/': '/',
            '&': '&',
            '!': '!?',
            ' ': ' ',
            '\n': '\n\r',
            '\t': '\t',
        })
        for item in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
            char_map[item] = item
        self.char_map = char_map
        self.device = device

    def map_char(self, char):
        """Map a given character to a normalized class representant.

        Parameters
        ----------
        char : str
            The char to map.

        Returns
        -------
        str
            The mapped character.
        """
        for key, pattern in self.char_map.items():
            if char in pattern:
                return key
        return 'U'

    def mapped_char_to_id(self, mapped_char):
        """Map a character to an numerical identifier.

        Parameter
        ---------
        mapped_char : str
            The mapped character that should be converted to its numerical representation.

        Returns
        -------
        int
            The numerical representation of the character.
        """
        keys = sorted(list(self.char_map.keys()))
        return 1 if mapped_char not in keys else keys.index(mapped_char) + 4

    def get_vocab_size(self):
        """Compute the size of the vocabulary.

        Returns
        -------
        int
            Size of the vocabulary.
        """
        return len(self.char_map) + 4

    def __call__(self, fragment):
        """Compute a numerical representation for a given fragment.

        Parameters
        ----------
        fragment : str
            Fragment to compute a numerical representation for.

        Returns
        -------
        RefXtractText
            The numerical representation of the given fragment.
        """
        mapped_fragment = ''.join(list(map(self.map_char, fragment)))
        mapped_fragment_ids = [2] + list(map(self.mapped_char_to_id, mapped_fragment)) + [3]
        return RefXtractText(' ' + fragment + ' ',
                             torch.Tensor(mapped_fragment_ids).view(1, -1).long().to(self.device))


def build_refxtract_model(preprocessor, embed_size=128, hidden_size=128, device=None):
    """Build an instance of the RefXtract model.

    Parameters
    ----------
    preprocessor : RefXtractPreprocessor
        The preprocessor to use.
    embed_size : int
        The number of embedding neurons to use.
    hidden_size : int
        The number of hidden neurons to use.
    device : torch.device
        The device to compute on.

    Returns
    -------
    torch.nn.modules.container.Sequential
        A RefXtract model instance.
    """
    return nn.Sequential(
        torch.nn.Embedding(preprocessor.get_vocab_size(), embed_size),
        torch.nn.Dropout(0.5),
        BiRNN(embed_size, hidden_size, 1, 4, device=device)
    )


def preprocess_reference_text(text):
    """Preprocess a PDF text.

    Parameters
    ----------
    text : str
        The text (possibly from a converted PDF) to preprocess.

    Returns
    -------
    tuple
        A tuple consisting of the following elements:
        - has_reference_section : A boolean which is true when the text contained the string 'reference'
          (not case-sensitive), false otherwise.
        - reference_section : A string containing the reference section.
        - non_reference_section : A string containing the text which was not in the reference section.
    """
    try:
        splitpoint = text.lower().rindex('reference')
    except ValueError:
        splitpoint = False
    while splitpoint and len(text) - splitpoint < 100 and 'reference' in text[:splitpoint].lower():
        text = text[:splitpoint]
        splitpoint = text.lower().rindex('reference')
    if not splitpoint:
        has_reference_section = False
        non_reference_section, reference_section = text, ''
    else:
        has_reference_section = True
        non_reference_section, reference_section = text[:splitpoint], text[splitpoint:]
    return has_reference_section, reference_section, non_reference_section


def extract_references(text, preprocessor, model):
    """Extract references from a given text.

    Parameters
    ----------
    text : str
        The text to extract the references from.
    preprocessor : RefXtractPreprocessor
        The preprocessor to use.
    model : torch.nn.modules.container.Sequential
        The model to use.

    Returns
    -------
    list
        A list containing the found references.
    """
    has_reference_section, reference_section, non_reference_section = preprocess_reference_text(text)
    reference_text = reference_section if has_reference_section else non_reference_section
    fragment = preprocessor(reference_text)
    out = model(fragment.idx).argmax(dim=2).cpu().numpy()

    buffer = ''
    found_citations = []
    in_citation = False
    for char, pred in zip(fragment.text, out[0, :]):
        if pred == 2:
            in_citation = True
        if pred == 3:
            in_citation = False
        if pred in [2, 3]:
            if buffer:
                found_citations.append(buffer)
            buffer = char
        elif pred == 1:
            buffer += char
        elif pred == 0:
            if in_citation:
                buffer += char
            else:
                if buffer:
                    found_citations.append(buffer)
                    buffer = ''
    return found_citations


class RefXtractor:
    """RefXtractor class."""

    def __init__(self, model=None, preprocessor=None, device=None):
        """Initialize the RefXtractor.

        Parameters
        ----------
        model : torch.nn.modules.container.Sequential
            The model to use.
        preprocessor : RefXtractPreprocessor
            The preprocessor to use.
        device : torch.device
            The device to use.
        """
        self.device = device
        self.preprocessor = preprocessor if preprocessor else RefXtractPreprocessor(device=device)
        self.model = model if model else build_refxtract_model(self.preprocessor, device=device)

    def load(self, model_uri=None, ignore_cache=False):
        """Load model parameters from the internet.

        Parameters
        ----------
        model_uri : str
            The model URI to load from.
        ignore_cache : bool
            When true, all caches are ignored and the model parameters are forcefully downloaded.

        Returns
        -------
        RefXtractor
            The wrapper itself.
        """
        self.model = load_model_params(self.model, 'refxtract', model_uri, ignore_cache=ignore_cache,
                                       device=self.device)
        return self

    def __call__(self, text):
        """Execute the model on a text.

        Parameters
        ----------
        text : str
            The text to extract references from.

        Returns
        -------
        list
            A list containing the found references.
        """
        return extract_references(text, self.preprocessor, self.model)
