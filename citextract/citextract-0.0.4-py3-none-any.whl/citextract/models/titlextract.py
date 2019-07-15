"""The TitleXtract model."""
import string
from collections import defaultdict
import torch
import torch.nn as nn

from citextract.utils.model import load_model_params


class TitleTagging(nn.Module):
    """TitleTagging model."""

    def __init__(self, input_size, hidden_size, n_layers, n_classes, device):
        """Initialize the model.

        Parameters
        ----------
        input_size : int
            The number of input neurons.
        hidden_size : int
            The number of hidden neurons.
        n_layers : int
            The number of layers.
        n_classes : int
            The number of output classes.
        device : torch.device
            The device to run the computations on.
        """
        super(TitleTagging, self).__init__()

        self.device = device

        self.hidden_size = hidden_size
        self.n_layers = n_layers
        self.lstm = nn.LSTM(input_size, hidden_size, n_layers, batch_first=True, bidirectional=True, dropout=0.5)
        self.fc = nn.Linear(hidden_size * 2, n_classes)

    def forward(self, x):
        """Forward-propagate the input data.

        Parameters
        ----------
        x : torch.Tensor
            The input tensor of size (batch_size, sequence_length, input_size).

        Returns
        -------
        torch.Tensor
            The output tensor of size (batch_size, sequence_length, n_classes).
        """
        # Initiatlize parameters for the first step
        h_0 = torch.zeros(2 * self.n_layers, x.size(0), self.hidden_size).to(self.device)
        c_0 = torch.zeros(2 * self.n_layers, x.size(0), self.hidden_size).to(self.device)

        # Return the output and parameters for the n-th step (n=sequence_len)
        lstm_output, _ = self.lstm(x, (h_0, c_0))

        # Fully connected layer (hidden_size*2 --> n_classes)
        fc_output = self.fc(lstm_output)

        # Softmax
        softmax_output = nn.Softmax(dim=2)(fc_output)

        return softmax_output


def build_titlextract_model(preprocessor, embed_size=32, hidden_size=64, device=None):
    """Build an instance of the TitleXtract model.

    Parameters
    ----------
    preprocessor : TitleXtractPreprocessor
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
    vocab_size = len(preprocessor.chars)
    n_classes = 2
    return nn.Sequential(
        torch.nn.Embedding(vocab_size, embed_size),
        TitleTagging(input_size=embed_size, hidden_size=hidden_size, n_layers=2, n_classes=n_classes, device=device).to(
            device)
    ).to(device)


class TitleXtractPreprocessor:
    """TitleXtract preprocessor."""

    def __init__(self, device=None):
        """Initialize the preprocessor.

        Parameters
        ----------
        device : torch.device
            The device to use.
        """
        chars = list(string.ascii_letters + string.digits + string.punctuation + string.whitespace)
        self.chars = ['<PAD>', '<UNK>'] + chars
        self.device = device
        self.char_mapping = defaultdict(lambda: 1)
        for index, char in enumerate(self.chars):
            self.char_mapping[char] = index

    def map_text_chars(self, text):
        """Map text to numerical character representations.

        Parameters
        ----------
        text : str
            The text to map.

        Returns
        -------
        torch.Tensor
            The tensor representing the mapped characters.
        """
        mapped_chars = list(map(lambda char: self.char_mapping.get(char, 1), text))
        return torch.Tensor(mapped_chars).long().view(1, -1).to(self.device)

    def map_text_targets(self, text, title):
        """Align and map the targets of a text.

        Parameters
        ----------
        text : str
            The text to map.
        title : str
            The title (substring of the text) to map.

        Returns
        -------
        torch.Tensor
            A tensor representing the characters of the text for which an element is 1 if and only if a character
            is both represented by the text and by the title, 0 otherwise.
        """
        start_position = text.index(title)
        mapped_target = [1 if start_position <= index < start_position + len(title) else 0 for index in
                         range(len(text))]
        return torch.Tensor(mapped_target).view(1, -1).long().to(self.device)

    def __call__(self, text, title):
        """Preprocess a text and a title.

        Parameters
        ----------
        text : str
            The text to preprocess.
        title : str
            The title to preprocess.

        Returns
        -------
        tuple
            A tuple consisting of the following elements:
            - A tensor of the characters of the text.
            - A tensor of the targets of the characters of the text.
        """
        return self.map_text_chars(text), self.map_text_targets(text, title)


class TitleXtractor:
    """TitleXtractor wrapper class."""

    def __init__(self, model=None, preprocessor=None, device=None):
        """Initialize the TitleXtractor.

        Parameters
        ----------
        model : torch.nn.modules.container.Sequential
            The model to use.
        preprocessor : TitleXtractPreprocessor
            The preprocessor to use.
        device : torch.device
            The device to use.
        """
        self.device = device
        self.preprocessor = preprocessor if preprocessor else TitleXtractPreprocessor(device=device)
        self.model = model if model else build_titlextract_model(self.preprocessor, device=device)

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
        TitleXtractor
            The wrapper itself.
        """
        self.model = load_model_params(self.model, 'titlextract', model_uri, ignore_cache=ignore_cache,
                                       device=self.device)
        return self

    def __call__(self, ref):
        """Run the TitleXtract model.

        Parameters
        ----------
        ref : str
            Reference to find a title for.

        Returns
        -------
        str
            The found title, and none if no title was found.
        """
        result = self.model(self.preprocessor.map_text_chars(ref)).argmax(dim=2).cpu()[0].detach().numpy().tolist()
        if 1 not in result:
            return None
        start_pos = result.index(1)
        subselection = result[start_pos:]
        if 0 in subselection:
            length = result[start_pos:].index(0)
            title = ref[start_pos:start_pos + length]
        else:
            title = ref[start_pos:]
        return title.strip()
