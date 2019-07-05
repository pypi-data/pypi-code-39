__version__ = '0.1.2'

import argparse
import json
import os
import xlrd
from datetime import datetime

def set_args():
    args = argparse.ArgumentParser()
    args.add_argument('--perentry', action='store_true', help='Output a JSON file per entry of XLS file.')
    args.add_argument('--persheet', action='store_true', help='Output a JSON file per sheet of XLS file.')
    args.add_argument('xls_input', help='Specify XLS file.')
    args.add_argument('output_path', nargs='?', help='Specify output folder for --persheet mode.', default='output')
    return args.parse_args()

def standard_path(p):
    try:
        if p.endswith('/'):
            return p
        else:
            return p+'/'
    
    except IndexError:
        return p
    
def read_type(c: 'sheet.cell_type'):            
    '''
    https://xlrd.readthedocs.io/en/latest/api.html#xlrd.sheet.Cell

    XL_CELL_ERROR:
    int representing internal Excel codes; 
    for a text representation, refer to the supplied dictionary 
    error_text_from_code

    XL_CELL_BLANK:
    empty string ''. 
    Note: this type will appear only when open_workbook(..., formatting_info=True) is used.
    '''
    symbols = ('empty', 'text', 'number', 'date', 'bool', 'error', 'blank')
    return symbols[c]

def read_number(c):
    '''Properly display int.'''
    if str(c).endswith('.0'):
        return int(c)
    return c

def read_date(c):
    '''
    Properly display date.
    ISO 8601 format YYYY-MM-DD
    '''
    # https://xlrd.readthedocs.io/en/latest/api.html#xlrd.book.Book.datemode
    return xlrd.xldate.xldate_as_datetime(xldate=c, datemode=0)

def per_sheet():
    '''
    Read XLS file and write each sheet to a JSON file.
    The JSON key will be the row number.
    '''
    output_path = standard_path(args.output_path)
    os.makedirs(output_path, exist_ok=1)

    book = xlrd.open_workbook(args.xls_input)
    data = {}
    
    file_name = args.xls_input

    for sheet in book.sheets():

        if file_name.endswith('x'):
            prefix = output_path+args.xls_input[:-5]+f'_{sheet.name}'
        else:
            prefix = output_path+args.xls_input[:-4]+f'_{sheet.name}'

        nb_row = max(0, sheet.nrows)
        nb_col = max(0, sheet.ncols)

        for i in range(1, nb_row):            
            number = sheet.cell_value(rowx=i, colx=0)
            helper_dict = {}

            for j in range(0, nb_col):                                
                key = sheet.cell_value(rowx=0, colx=j)
                
                # Read cell type before writing.
                t = read_type(sheet.cell_type(rowx=i, colx=j))
                v = sheet.cell_value(rowx=i, colx=j)
                
                if t == 'number':
                    v = read_number(v)
                if t == 'date':
                    v = read_date(v)
                    v = str(v)[:10]
                                
                helper_dict[key] = v                
                data[number] = helper_dict
        
        # Save after finished reading a sheet.
        json_outfile = prefix+'.json'
        with open(json_outfile, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=2)

def per_entry():
    '''
    Read XLS file and write each row to a JSON file.
    The JSON key will be the row number.
    '''
    output_path = standard_path(args.output_path)
    os.makedirs(output_path, exist_ok=1)

    book = xlrd.open_workbook(args.xls_input)    
    
    for sheet in book.sheets():
        file_name = args.xls_input 
        
        if file_name.endswith('x'):
            prefix = output_path+args.xls_input[:-5]
        else:
            prefix = output_path+args.xls_input[:-4]

        nb_row = max(0, sheet.nrows)
        nb_col = max(0, sheet.ncols)

        for i in range(1, nb_row):            
            number = sheet.cell_value(rowx=i, colx=0)
            data = {}
            helper_dict = {}

            for j in range(0, nb_col):                
                key = sheet.cell_value(rowx=0, colx=j)
                
                # Read cell type before writing.
                t = read_type(sheet.cell_type(rowx=i, colx=j))
                v = sheet.cell_value(rowx=i, colx=j)
                
                if t == 'number':
                    v = read_number(v)
                if t == 'date':
                    v = read_date(v)
                    v = str(v)[:10]
                                
                helper_dict[key] = v
                data[number] = helper_dict

            # Save after finished reading row (i)
            json_outfile = prefix+f'_{sheet.name}{i}.json'
            with open(json_outfile, 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, ensure_ascii=False, indent=2)

def single_json():
    '''
    Read XLS file and write to single JSON file.
    The JSON key will be the name of the sheet.
    '''
    if args.output_path == 'output':
        json_outfile = args.output_path+'.json'
    
    file_name = args.xls_input 

    if file_name.endswith('x'):
        json_outfile = args.xls_input[:-5]+'.json'
    else:
        json_outfile = args.xls_input[:-4]+'.json'

    book = xlrd.open_workbook(args.xls_input)
    bind = {}
    data = {}
    
    for sheet in book.sheets():
        nb_row = max(0, sheet.nrows)
        nb_col = max(0, sheet.ncols)

        for i in range(1, nb_row):            
            number = sheet.cell_value(rowx=i, colx=0)
            helper_dict = {}

            for j in range(0, nb_col):                
                key = sheet.cell_value(rowx=0, colx=j)
                
                # Read cell type before writing.
                t = read_type(sheet.cell_type(rowx=i, colx=j))
                v = sheet.cell_value(rowx=i, colx=j)
                
                if t == 'number':
                    v = read_number(v)
                if t == 'date':
                    v = read_date(v)
                    v = str(v)[:10]
                                
                helper_dict[key] = v

            data[number] = helper_dict

        bind[sheet.name] = data
    
    # Save after finished reading everything.
    with open(json_outfile, 'w', encoding='utf-8') as outfile:
        json.dump(bind, outfile, ensure_ascii=False, indent=2)

# Usage:
# xls2json --perentry excel_file.xlsx
# xls2json --persheet excel_file.xlsx
# xls2json excel_file.xlsx

args = set_args()

def main():
    if args.perentry:        
        per_entry()
    elif args.persheet:
        per_sheet()
    else:
        single_json()

if __name__ == '__main__':
    main()