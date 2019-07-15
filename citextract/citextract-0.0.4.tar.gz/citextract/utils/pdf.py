"""PDF utilities for converting PDF to a usable format."""
import datetime
import os
from io import StringIO
from random import randint

import requests
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def convert_pdf_url_to_text(pdf_url):
    """Convert a PDF URL to text.

    Parameters
    ----------
    pdf_url : str
        The URL to parse.

    Returns
    -------
    str
        The text which was found in the PDF document.
    """
    response = requests.get(pdf_url)
    filename = '_tmp_' + datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S') + '_' + str(randint(0, 100000)) + '.pdf'
    with open(filename, 'wb') as out_file:
        out_file.write(response.content)
    try:
        text = convert_pdf_file_to_text(filename)
    finally:
        os.remove(filename)
    return text


def convert_pdf_file_to_text(path):
    """Convert a PDF file to text.

    Parameters
    ----------
    path : str
        Path to the PDF file.

    Returns
    -------
    str
        The text found in the PDF file.
    """
    resource_manager = PDFResourceManager()
    return_string = StringIO()
    codec = 'utf-8'
    la_params = LAParams()
    device = TextConverter(resource_manager, return_string, codec=codec, laparams=la_params)
    with open(path, 'rb') as input_file:
        interpreter = PDFPageInterpreter(resource_manager, device)
        for page in PDFPage.get_pages(input_file, set(), maxpages=0, password="", caching=True, check_extractable=True):
            interpreter.process_page(page)
    device.close()
    result = return_string.getvalue()
    return_string.close()
    return result
