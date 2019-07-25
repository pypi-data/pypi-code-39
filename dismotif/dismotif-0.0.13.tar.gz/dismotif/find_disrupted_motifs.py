#!/usr/bin/env python3

import os
import sys
import math

infile = sys.argv[1]

def load_motif(motif):
	motif_file = os.path.join('/home/joshchiou/references/combined_motifs/', motif + '.db')
	pwm = {}
	with open(motif_file) as mf:
		ls = mf.read().splitlines()
		for i,l in enumerate(ls):
			n = i+1
			bases = list(map(float, l.split(' ')))
			pwm[n] = {'A':bases[0], 'C':bases[1], 'G':bases[2], 'T':bases[3]} 
	return pwm

def calc_entropy(pwm, vpos):
	entropy = 0
	for freq in pwm[vpos].values():
		if freq > 0:
			entropy += freq * math.log2(freq)
	if entropy < 0:
		entropy *= -1
	return entropy

with open(infile) as f:
	for line in f:
		fields = line.rstrip('\n').split('\t')
		mstart, mend = int(fields[5]) + 1, int(fields[6]) + 1
		mname = fields[7]
		mstrand = fields[9]
		vpos = int(fields[2])
		pwm = load_motif(mname)
		if mstrand == '+':
			vmpos = vpos - mstart + 1
		elif mstrand == '-':
			vmpos = mend - vpos
		entropy = calc_entropy(pwm, vmpos)
		fields.append(str(entropy))
		print('\t'.join(fields))

