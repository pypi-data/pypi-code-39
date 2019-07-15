import os
import sys


def resolve_file_path(file):
    if os.path.exists('tests'):
        return os.path.join('tests', file)
    else:
        return file


def mocked_pdf_requests_get(url, *args, **kwargs):
    # Add the tests folder to the path such that the test files can be found
    sys.path.append('tests')

    # A fake response class
    class MockResponse:
        def __init__(self, content, status_code):
            self.content = content
            self.status_code = status_code

    # Check for PDF files
    if url.endswith('.pdf'):
        # If it is a PDF file, then load the corresponding PDF file from the test file directory
        with open(resolve_file_path(os.path.join('test_files', 'pdf', url)), 'rb') as in_file:
            response = MockResponse(in_file.read(), 200)
        return response

    # When no mocked response was found, simply return a 404 not found status
    return MockResponse(None, 404)
