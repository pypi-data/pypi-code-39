import csv, os

def get_headers(sample_data):
    """
    get headers based on keys in the combined qualifyr json data
    Returns a list of header columns sample_name,result,quality_file.metric<1..N>
    """
    header_items = ['sample_name', 'result']
    for quality_file in sorted(sample_data['checks'].keys()):
        for metric in sorted(sample_data['checks'][quality_file].keys()):
            for sub_metric in ['metric_value', 'check_result']:
                header_items.append(f'{quality_file}.{metric}.{sub_metric}')
    return header_items

def create_text_report(json_data, output_dir = '.'):
    """
    Create a TSV file with one row per sample
    """
    header_items = get_headers(json_data[0])

    filename = os.path.join(output_dir, 'qualifyr_report.tsv')
    with open(filename , 'w') as fh:
        writer = csv.writer(fh, delimiter='\t')
        writer.writerow(header_items)
        for sample_data in sorted(json_data, key=lambda sample_data: sample_data['sample_name']):
            row_items = []
            for index, header_item in enumerate(header_items):
                if index < 2:
                    row_items.append(sample_data[header_item])
                else:
                    quality_file, metric, sub_metric = header_item.split('.')
                    row_items.append(sample_data['checks'][quality_file][metric][sub_metric])

            writer.writerow(row_items)
    