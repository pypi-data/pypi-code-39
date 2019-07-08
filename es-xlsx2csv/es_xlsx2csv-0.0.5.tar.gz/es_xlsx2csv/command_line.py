#!/usr/bin.env python3

# Heavily based off https://github.com/calebdinsmore/matillion-columns/blob/master/matillion_columns/command_line.py

from io import BytesIO
import csv
import argparse
import boto3
import xlrd
import pandas as pd
import openpyxl


parser = argparse.ArgumentParser()
parser.add_argument(
    'xlsx_file', help='Path to XLSX file in S3 (or local if -l) (excluding bucket name).')
parser.add_argument('--bucket', '-b', default='translatingdata-dev',
                    help='Bucket to get XLSX from.')
parser.add_argument('--local', '-l', action='store_true',
                    help='Use a local XLSX path')
args = parser.parse_args()


def csv_from_excel_sheet(workbook, sheet_name):
    print(sheet_name)
    sheet = workbook.sheet_by_name(sheet_name)
    new_csv_file = open("%s_%s.csv" % (args.xlsx_file, sheet_name), 'w')
    wr = csv.writer(new_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sheet.nrows):
        wr.writerow(sheet.row_values(rownum))

    new_csv_file.close()


def csv_from_excel():
    wb = xlrd.open_workbook(args.xlsx_file, on_demand=True)
    sheet_names = wb.sheet_names()
    for sheet_name in sheet_names:
        csv_from_excel_sheet(wb, sheet_name)


def s3_csv_from_excel():
    client = boto3.client('s3')
    xlsx_object = client.get_object(Bucket=args.bucket, Key=args.xlsx_file)
    content_body = xlsx_object['Body'].read()
    workbook = openpyxl.load_workbook(BytesIO(content_body))
    sheet_names = workbook.sheetnames
    for sheet_name in sheet_names:
        print('Uploading sheet: %s' % (sheet_name))
        s3_csv_from_excel_sheet(client, content_body, sheet_name)


def s3_csv_from_excel_sheet(client, content_body, sheet_name):
    dataframe = pd.read_excel(BytesIO(content_body), encoding='utf-8-sig',
                              sheet_name=sheet_name)
    filename = args.xlsx_file.replace('.xlsx', '_%s.csv' % (sheet_name))
    csv_buffer = BytesIO()
    dataframe.to_csv(csv_buffer, index=False)
    client.put_object(Body=csv_buffer.getvalue(),
                      Bucket=args.bucket, Key=filename)


def main():
    if not args.local:
        print('Mode: S3')
        s3_csv_from_excel()
    else:
        print('Mode: Local')
        csv_from_excel()
