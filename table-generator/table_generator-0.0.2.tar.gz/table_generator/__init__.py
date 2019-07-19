import sys
import os.path

import lxml.etree as etree


# for packaging
name = "table_generator"

# html templates for inserting children
DOCUMENT = '<!DOCTYPE html><html><head></head><body>%s</body></html>'
TABLE = '<table>%s</table>'
TR = '<tr>%s</tr>'
TH = '<th>%s</th>'
TD = '<td>%s</td>'


def generate_html(data, complete_file, header, pretty, attrs=False):
    """Generates code for html table from self.data
    
    Args:
        data (list) -- 2D list containing data organized into rows
        complete_file (bool) -- whether or not to add html elements to make code function as a separate file.
        header (bool) -- whether or not to turn first row of csv values into <th> tags
        pretty (bool) - whether or not to prettify the output code
        attrs (dict) - html attributes mapped to corresponding values.

    Returns:
        str -- html code for table element containing data from csv file
    """

    table_children = ''  # rows to be added here
    
    if header:
        # generate code from first row as header row
        header_row = ''
        for header in data[0]:
            header_row += TH % header

        table_children += TR % header_row

    # determines whether to use whole list or exclude first row
    starting_index = 0
    if header:
        starting_index = 1

    data_rows = ''
    for row in data[starting_index:]:
        row_element = ''
        for value in row:
            row_element += TD % value
        data_rows += TR % row_element

    table_children += data_rows

    html_table = TABLE % table_children

    if complete_file:
        html = DOCUMENT % html_table
    else:
        html = html_table

    if attrs:
        
        attrs_strings = []
        for key, val in attrs.items():
            attrs_strings.append(f'{key}="{val}"')

        attrs_string = ' '.join(attrs_strings)

        html = html.replace('<table>', f'<table {attrs_string}') 

    if pretty:
        
        i = 0
        tmp = f'{i}.html'
        while os.path.isfile(tmp):
            i += 1
            tmp = f'{i}.html'

        with open(tmp, 'w+') as f:
            f.write(html)
        
        x = etree.parse(tmp)

        os.remove(os.path.abspath(tmp))

        html = etree.tostring(x, pretty_print=True).decode()
        html = html.replace('<head/>', '<head></head>')
        html = html.replace('<th/>', '<th></th>')
        html = html.replace('<td/>', '<td></td>')
        html = html.replace('  ', '    ')

    return html
