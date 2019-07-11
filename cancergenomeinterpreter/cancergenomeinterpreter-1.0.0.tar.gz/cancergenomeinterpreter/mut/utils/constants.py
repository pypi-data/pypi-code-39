####################################
# names of the ouputed files:

# main output folder
INPUT_MUTS = 'input_mutations.tsv'
TRANSVAR_REVPROT_INPUT = 'transvar_revprotein_input.tsv'  # note that _ens and _refseq will be created
TRANSVAR_REVPROT_OUTPUT = 'transvar_revprotein_output.tsv'
TRANSVAR_DNA_INPUT = 'transvar_dna_input.tsv'
TRANSVAR_DNA_OUTPUT = 'transvar_dna_output.tsv'
ANNOTATED_MUTS = 'annotated_mutations.tsv'
FISCORE_INPUT = 'fiscore_input.tsv.gz'
FISCORE_OUTPUT = 'fiscore_output.tsv.gz'
METADATA_MUTS = 'metadata_mutations.tsv'
DRIVER_MUTS = 'driver_prediction_mutations.tsv'
FINAL_MUTS = 'mutation_analysis.tsv'
REPORT = 'summary.tsv'

PANNO_NOT_MAPPED = 'not_mapped_protein_mutations.tsv'
GANNO_NOT_MAPPED = 'not_mapped_dna_mutations.tsv'
MALFORMED_INPUT = 'malformed_input.tsv'

FS_NOT_MAPPED = 'not_mapped_frameshift.tsv'

####################################
# names of the possible input formats

VCF_FORMAT = 'vcf'
FREE_FORMAT = 'gtf'  # genomic tabulated format
GDNA_FORMAT = 'gdna'
PROT_FORMAT = 'prot'

####################################
# name of columns

# these are not outputed by the pipeline but required as input depending on the format
SAMPLE = 'sample'
CHR = 'chr'
POS = 'pos'
REF = 'ref'
ALT = 'alt'
GDNA = 'gdna'  # this is also used as an output column
PROT = 'protein'  # this is also used as an output column
STRAND = 'strand'

# this can not be changed since is the name used by transvar
GENE = 'gene'  # remember that this is for gene symbol

# columns created by the pipeline
CONSEQUENCE_TYPE = 'consequence'
CDNA = 'cdna'
AA_POS = 'protein_pos'
AA_CHANGE = 'protein_change'
TRANSCRIPT = 'transcript'
EXON = 'exon'
INTERNAL_ID = 'default_id'

# only when input is protein
REV_TRANSCRIPT = 'reverse_transcript'
REV_MAP_ISSUE = 'revmap_issue'

# oncodriveMUT columns
KNOWN_ONCOGENIC = 'known_oncogenic'
KNOWN_PREDISPOSING = 'known_predisposing'
KNOWN_NEUTRAL = 'known_neutral'
PFAM_DOMAIN = 'Pfam_domain'
TRANSCRIPT_EXONS = 'transcript_exons'
TRANSCRIPT_AMINOACIDS = 'transcript_aminoacids'
EXAC_AF = 'exac_af'

FISCORE_SCORE = 'cadd_phred'
DRIVER_GENE = 'driver_gene'
DRIVER_GENE_SOURCE = 'driver_gene_source'
GENE_ROLE = 'gene_role'
IS_IN_CLUSTER = 'is_in_cluster'
IS_IN_DELICATE_DOMAIN = 'is_in_delicate_domain'
PROTEIN_AFFECTED = 'mutation_location'

MISSENSE_PREDICTION = 'missense_driver_mut_prediction'
DISRUPTING_PREDICTION = 'disrupting_driver_mut_prediction'
INFRAME_PREDICTION = 'inframe_driver_mut_prediction'
DRIVER_MUT_PREDICTION = 'driver_mut_prediction'
DRIVER_MUT_BOOL = 'driver'
DRIVER_MUT_STATEMENT = 'driver_statement'
KNOWN_MATCH = 'known_match'  # whether the tumor of the known mutation match with the tumor sample

# columns required in the in silico prescription
CANCER = 'cancer'
ALT_TYPE = 'alt_type'

# final columns combining the values of the known oncogenic/predisposing variants reference/source column
KNOWN_VARIANT_SOURCE = 'known_variant_source'
KNOWN_VARIANT_REFERENCE = 'known_variant_reference'

# the separator to display e.g. a list of cancers as a string
SEPARATOR = '__'
TUMORS_SEP = SEPARATOR

####################################
# labels of column values

# the generic tumor type label
PANCANCER = 'CANCER'

# the default sample id inserted if none
DEFAULT_SAMPLE = 'cgi_sample'

# gene driver
TUMOR_DRIVER = 'tumor_driver'
OTHER_TUMOR_DRIVER = 'other_tumor_driver'

IN_CLUSTER = 'in_cluster'
IN_DELICATE_DOMAIN = 'in_delicate_domain'

# protein portion affected
BEFORE_LAST_EXON = 'before_last_exon'
BEFORE_LAST_PORTION = 'before_last_portion'
LAST_PORTION = 'last_portion'

# gene role category names
ACT = 'Act'
LOF = 'LoF'
AMBIGUOUS = 'ambiguous'

# driver mut boolean categories
KNOWN = 'known'
PREDICTED = 'predicted'
OTHER = 'other'

# driver mut prediction categories names
TIER_1 = 'TIER 1'
TIER_2 = 'TIER 2'
FISCORE_NA = 'Functional Impact score not available'
PASSENGER = 'passenger'
CT_NOT_CONSIDERED = 'not protein-affecting'

POLYM = 'polymorphism'

# tags in transvar info column stating bad reverse mapping (panno utility)
INVALID_TRANSVAR_MAP_TAGS = ['no_valid_transcript_found', 'CSQN=Unclassified', 'CSQN=Frameshift;imprecise']

####################################
# oncodriveMUT parameters

# if a max percentage of the input can not be mapped, stop the execution
MAX_NONMAPPED_RATIO = 0.3

# for ct taxonomy in TransVar, check: https://github.com/zwdzwd/transvar/wiki/Interpret-consequence-labels-%28CSQN%29
MISSENSE_SIMPLE_CT = ['Missense']
MISSENSE_COMPLEX_CT = ['MultiAAMissense']
MISSENSE_CT = MISSENSE_SIMPLE_CT + MISSENSE_COMPLEX_CT
FRAMESHIFT_CT = ['Frameshift']
DISRUPTING_CT = ['Nonsense', 'Frameshift', 'CdsStartLoss', 'CdsStopLoss', 'CdsStopSNV', 'CdsStartSNV',
                 'SpliceDonorDeletion', 'SpliceAcceptorDeletion', 'SpliceDonorSNV', 'SpliceAcceptorSNV',
                 # 'SpliceDonorSubstitution', 'SpliceAcceptorSubstitution',
                 'SpliceDonorBlockSubstitution', 'SpliceAcceptorBlockSubstitution',
                 'SpliceDonorInsertion', 'SpliceAcceptorInsertion']
INFRAME_CT = ['InFrameDeletion', 'InFrameInsertion']
PAM_CT = MISSENSE_CT + DISRUPTING_CT + INFRAME_CT

# oncodriveMUT customizable thresholds
FISCORE_DEMANDING_TH = 30
FISCORE_LOOSE_TH = 25
PROTEIN_TIP = 0.05
POLYM_AF = 0.01

# in case an original column has the same name than a pipeline outputed column, put a suffic in the former
ORIGINAL_COLUMNS_SUFFIX = '_orig'
