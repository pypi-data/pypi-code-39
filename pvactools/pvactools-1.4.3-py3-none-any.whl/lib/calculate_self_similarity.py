import csv
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML

class CalculateSelfSimilarity:
    def __init__(self, input_file, output_file, species='human', file_type='pVACseq'):
        self.input_file = input_file
        self.output_file = output_file
        self.species = species
        self.file_type = file_type
        self.species_to_organism = {
            'human': 'Homo Sapiens',
            'mouse': 'Mus musculus',
        }

    def reference_match_headers(self):
        return [
            'Reference Matches',
        ]

    def execute(self):
        if self.species not in self.species_to_organism:
            print("Species {} not supported for Reference Proteome Similarity search. Skipping.".format(self.species))
            shutil.copy(self.input_file, self.output_file)
            return

        with open(self.input_file) as input_fh, open(self.output_file, 'w') as output_fh:
            reader = csv.DictReader(input_fh, delimiter = "\t")
            writer = csv.DictWriter(output_fh, delimiter = "\t", fieldnames=reader.fieldnames + self.reference_match_headers(), extrasaction='ignore')
            writer.writeheader()
            for line in reader:
                if self.file_type == 'pVACbind':
                    peptide = line['Epitope Seq']
                else:
                    peptide = line['MT Epitope Seq']
                result_handle = NCBIWWW.qblast("blastp", "nr", peptide, entrez_query="{} [Organism]".format(self.species_to_organism[self.species]))
                for blast_record in NCBIXML.parse(result_handle):
                    if len(blast_record.alignments) == 0:
                        line['Reference Matches'] = "0"
                    else:
                        reference_matches = 0
                        for alignment in blast_record.alignments:
                            best_alignment = alignment.hsps[0]
                            if len(peptide) == best_alignment.identities:
                                reference_matches += 1
                        line['Reference Matches'] = reference_matches
                writer.writerow(line)
