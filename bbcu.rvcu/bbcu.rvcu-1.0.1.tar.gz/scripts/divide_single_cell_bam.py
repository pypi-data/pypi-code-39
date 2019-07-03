

import os
import re
import sys

input_bam = sys.argv[1]
output_folder = sys.argv[2]
filtered_cell_barcodes_file = sys.argv[3]

with open(filtered_cell_barcodes_file, 'r') as filtered_cell_barcodes_fh:
    filtered_cell_barcodes = {}
    for line in filtered_cell_barcodes_fh:
        barcode = line[:-3] # Remove -1\n characters in end of line
        filtered_cell_barcodes[barcode] = None

def print_to_files(reads_cells, output_folder):
    new_file = False
    for cell_barcode in reads_cells:
        output_file = os.path.join(output_folder, "%s.bam" % cell_barcode)
        if not os.path.isfile(output_file):
            new_file = True
        with open(output_file, 'a') as o_fh:
            if new_file:
                o_fh.writelines(headers)
                new_file = False
            o_fh.writelines(reads_cells[cell_barcode])


with open(input_bam, 'r') as in_fh:
    reads_cells = {}
    headers = []
    regex_rx = re.compile('RX:Z:(\w{16})')
    regex_qx = re.compile('QX:Z:(\S{16})')
    line_counter = 0
    for line in in_fh:
        if line.startswith('@'):
            headers.append(line)
        else:
            cell_barcode = regex_rx.search(line).groups()[0]
            if cell_barcode not in filtered_cell_barcodes:
                continue
            line_counter += 1
            line = regex_rx.sub('RX:Z:', line)
            if cell_barcode not in reads_cells:
                reads_cells[cell_barcode] = []
            reads_cells[cell_barcode].append(regex_qx.sub('QX:Z:', line))
        if line_counter % 100000 == 0:
            line_counter = 0
            print_to_files(reads_cells, output_folder)
            del reads_cells
            reads_cells = {}
    print_to_files(reads_cells, output_folder)


