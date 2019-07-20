import sys

def write(qrcode):
	write = sys.stdout.write
	for row in qrcode.matrix:
		for col in row:
			write('X' if col else '_')
		write('\n')