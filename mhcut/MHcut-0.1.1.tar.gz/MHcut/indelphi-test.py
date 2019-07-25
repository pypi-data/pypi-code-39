import inDelphi.inDelphi

inDelphi.inDelphi.init_model(celltype='mESC')
inDelphi.inDelphi.init_model(celltype='K562')

left_seq = 'AGAATCGCCCGCGGTCCATCCTTTATCAGCGGGAATTCAAGCGCACCAGCCAG'
right_seq = 'CCTCAAGCGCACCAGCAACATAATATTCGCACTAGATCCATCCCCATACCTGACC'
seq = left_seq + right_seq
cutsite = len(left_seq)

pred_df, stats = inDelphi.inDelphi.predict(seq, cutsite)

target_size = 18
freq_l = 0
len_max = 0
freq_max = 0
for row in pred_df.iterrows():
    if row[1]['Length'] == target_size:
        freq_l += row[1]['Predicted frequency']
    if row[1]['Predicted frequency'] > freq_max:
        freq_max = row[1]['Predicted frequency']
        len_max = row[1]['Length']

pred_gt_df = inDelphi.inDelphi.add_genotype_column(pred_df, stats)

# Any duplicates? not in this example
dups = {}
for row in pred_gt_df.iterrows():
    if row[1]['Genotype'] in dups:
        dups[row[1]['Genotype']] += 1
    else:
        dups[row[1]['Genotype']] = 1

for x in dups:
    if dups[x]>1:
        print x


# Debug

seq = 'TAGCTGATCGTGTGGTGAGTGTGTGGTGTGTGTTTGTGGNGTGTGTGTGGGGTGGATCAGTCAGCTAGCATCGACTAC'
cutsite = 33
pred_df, stats = inDelphi.inDelphi.predict(seq, cutsite)


left_seq = 'TAAGTAGTTACTCTCTAGCCTATT'
right_seq = 'TTATCAGTTATTATCCCAGCA'
seq = left_seq + right_seq
cutsite = len(left_seq)

pred_df, stats = inDelphi.inDelphi.predict(seq, cutsite)
