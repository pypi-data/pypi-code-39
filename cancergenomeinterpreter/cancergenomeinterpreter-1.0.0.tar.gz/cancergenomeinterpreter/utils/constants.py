####################################
# names of the ouputed files:

# tmp:
INPUT_CNAS = 'input_cnas.txt'
MALFORMED_CNAS = 'malformed_cnas.txt'
REFORMATED_CNAS = 'reformated_cnas.txt'
DRIVERS_CNAS = 'driver_cnas.txt'

INPUT_FUS = 'input_fus.txt'
REFORMATED_FUS = 'reformated_fus.txt'
DRIVER_FUS = 'driver_fus.txt'

# root:
CGI_CNAS = 'cna_analysis.tsv'
CGI_FUS = 'fusion_analysis.tsv'
DRIVER_ARRANGED_MUTATIONS = 'mutation_analysis.tsv'
DRUG_PRESCRIPTION = 'drug_prescription.tsv'
NOT_MAPPED = 'not_mapped_entries.txt'

####################################
# names of the possible cna input formats

CNA_FREE_FORMAT = 'free'
CNA_MAT_FORMAT = 'mat'
FUS_FORMAT = 'fus'

####################################
# separators of the fusions:

FUS_SEP = '__'

####################################
# name of columns

# these are not outputed by the pipeline but required as input depending on the format
SAMPLE = 'sample'
GENE = 'gene'  # remember that this is for gene symbol
CNA = 'cna'
FUS = 'fus'
FUS_EFFECTOR = 'effector_gene'
GENE_ROLE = 'gene_role'
LOCUS, CYTOBAND = 'Locus ID', 'Cytoband'  # these are the columns to recognize CNA calls from the gistic output

# columns created by the pipeline
INTERNAL_ID = 'internal_id'
KNOWN_IN_TUMORS = 'known_in_tumors'
PREDICTED_IN_TUMORS = 'predicted_in_tumors'
KNOWN_MATCH = 'known_match'
PREDICTED_MATCH = 'predicted_match'
ONCOGENIC = 'driver'  # the boolean
ONCOGENIC_CLASSIFICATION = 'driver_statement'

# columns required in the in silico prescription
CANCER = 'cancer'
ALT_TYPE = 'alt_type'

####################################
# labels of column values

# accepted labels for CNA column
CNA_ALTERATIONS = ['AMP', 'DEL']

# the generic tumor type label
PANCANCER = 'CANCER'

# the default sample id inserted if none
DEFAULT_SAMPLE = 'cgi'

# of the oncogenic classification (kown or predicted)
KNOWN = 'known'
PREDICTED = 'predicted'

# gene role
AMBIGUOUS = 'ambiguous'

####################################


# in case an original column has the same name than a pipeline outputed column, put a suffic in the former
ORIGINAL_COLUMNS_SUFFIX = '_orig'
