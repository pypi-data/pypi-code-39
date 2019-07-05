import csv

def get_country(out_company):
    if out_company=='':
        return ''
    dataset = []
    with open('new_org_view.csv', 'w', encoding='UTF-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            dataset.append(row)
    for row in dataset:
        in_company = row[0]
        counrty = row[1]
        if out_company==in_company:
            return counrty
