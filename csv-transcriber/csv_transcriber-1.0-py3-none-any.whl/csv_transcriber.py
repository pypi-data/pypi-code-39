import csv
import sys
import os

def transcribe(i, o):

	if not os.path.isdir(o): # If dir doesnt exist, create.
		os.mkdir(o)

	with open(i, mode='r') as csv_file: # Open CSV File

		re = list(csv.reader(csv_file))
		headers = re[0]

		for row in re[1:]: # Loop through rows

			with open(f'{o}/{row[0]}.txt', mode="w+") as file: # Create text file in that directory with name as first row

				for key in range(len(headers)): # Loop through properties of row

					file.write(f'{headers[key]}: {row[key]}\n') # Write to text file with format: 'Name of Row: Value'

		return