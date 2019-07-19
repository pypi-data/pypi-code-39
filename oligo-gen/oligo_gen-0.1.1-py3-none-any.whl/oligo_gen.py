import Bio
from Bio import SeqIO

def recordOligo(seq, leno, off):
	s = len(seq)
	for i in range(0,s-(s%off)-leno+1,off):
		print(seq[i:i+leno])

def genomeOligo(genome, olen, ooff):
	for k in range(0,len(genome)):
		recordOligo(str(genome[k].seq), olen, ooff)

def oligo_gen(filename, length, offset):
	records = list(SeqIO.parse(filename, "fasta"))
	oligo_len = int(length)
	oligo_offset = int(offset)
	genomeOligo(records, oligo_len, oligo_offset)

if __name__ == "__main__":
	import sys
	oligo_gen(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))
