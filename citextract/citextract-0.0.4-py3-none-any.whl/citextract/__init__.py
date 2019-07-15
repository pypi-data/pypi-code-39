"""CiteXtract - Bringing structure to the papers on ArXiv."""

project_settings = dict({
    'project_name': 'CiteXtract',
    'description': "CiteXtract - Bringing structure to the papers on ArXiv.",
    'url': "https://www.citextract.com/",
    'author': 'Kevin Jacobs',
    'author_email': 'kevin91nl@gmail.com',
    'copyright_text': '2019, Kevin Jacobs',
    'version': '0.0.4',
    'refxtract_version': '0.0.1',
    'titlextract_version': '0.0.1'
})

name = project_settings.get('project_name').lower()
__version__ = project_settings.get('version')
