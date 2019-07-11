import argparse
import csv
import json
import logging
import os
from collections import defaultdict

from cancergenomeinterpreter.prescription.entities.alteration import load_alterations
from cancergenomeinterpreter.prescription.entities.bioactivity import load_bioactivities
from cancergenomeinterpreter.prescription.entities.biomarker import load_biomarkers
from cancergenomeinterpreter.prescription.entities.genemarks import MATCH_LEVEL_COMPLETE, MATCH_LEVEL_NONE
from cancergenomeinterpreter.prescription.entities.tumor import Tumor

level_map = {
    1: 'only gene',
    2: 'only alteration type',
    3: 'complete'
}


def run(input_files: list, output_file: str, biomarkers_file: str, bioactivities_file: str, cancer_types_file: str,
        write_mutations: str, store_json: bool):
    # Load cancer type hierarchy
    Tumor.load_family(cancer_types_file)

    # Load biomarkers
    logging.info("Loading biomarkers")
    biomarkers = load_biomarkers(biomarkers_file)

    # Load bioactivities
    if bioactivities_file is not None:
        logging.info("Loading bioactivities")
        bioactivities = load_bioactivities(bioactivities_file)
        logging.info("{} genes have bioactivities".format(len(bioactivities)))

    # Load input alterations
    logging.info("Loading alterations")
    all_alterations = load_alterations(input_files)

    # Find prescriptions
    logging.info("Checking prescriptions")

    # Match alterations
    biomarkers_prescriptions = {}
    bioactivities_prescriptions = {}
    for (sample, cancer_type), alterations in all_alterations.items():

        # Match biomarkers
        logging.debug("Matching biomarkers")
        biomarkers_prescriptions[(sample, cancer_type)] = match_biomarkers(alterations, biomarkers, cancer_type, sample)

        if bioactivities_file is not None:
            # Match bioactivities
            logging.debug("Matching bioactivities")
            bioactivities_prescriptions[(sample, cancer_type)] = match_bioactivities(alterations, bioactivities,
                                                                                     cancer_type, sample)

            # Write mutations files correcting the driver_statement
        if write_mutations is not None:
            logging.info("Write mutations results")

            # Find mutations headers
            headers = None
            for file in input_files:
                with open(file, 'rt') as rows:
                    for row in rows:
                        if row.startswith('#'):
                            continue
                        else:
                            fields = row.split('\t')
                            if 'fus' not in fields and 'cna' not in fields:
                                headers = [f.strip() for f in fields]
                        break

            with open(write_mutations, "wt") as fd:
                writer = csv.writer(fd, delimiter='\t')
                writer.writerow(headers)
                for (_, _), alterations in all_alterations.items():
                    for a in alterations:
                        if a.mark_type != 'MUT':
                            continue

                        # Correct the driver_statement column
                        if not a.driver and len(a.biomarker_tumors) > 0:
                            a.driver = True
                            a.row['driver_statement'] = "known in: {}".format(";".join(a.biomarker_tumors))

                        writer.writerow([a.row[h] for h in headers])

    logging.info("Write biomarkers results")
    with open(output_file, 'wt') as fd:
        writer = csv.writer(fd, delimiter='\t')
        writer.writerow([
            'SAMPLE', 'CANCER_TYPE', 'SAMPLE_ALTERATION', 'ALTERATION_MATCH',
            'TUMOR_MATCH', 'DRUG', 'BIOMARKER', 'EFFECT', 'BIOMARKER_IDX', 'RESISTANCE_LIST', 'RESISTANCE_TYPE',
            'TESTED_TUMOR', 'EVIDENCE', 'SOURCE'
        ])

        for key, prescriptions in biomarkers_prescriptions.items():
            sample, cancer_type = key
            for sp in prescriptions:
                biomarker, match_alterations = sp['biomarker'], sp['match']
                sample_alterations = ', '.join([str(a) for a in match_alterations])
                source = biomarker.row['Source']
                biomarker_tumors = ', '.join([str(t) for t in biomarker.tumors])
                biomarker_drugs = biomarker.row['Drug full name']
                biomarker_title = biomarker.row['Biomarker']
                evidence = biomarker.row['Evidence level']
                resistances = ','.join([str(s.idx) for s in sp['resistance_list']])
                resistance_type = ','.join([b.row['Association'] for b in sp['resistance_list']])
                effect = biomarker.row['Association']

                alteration_match = level_map[sp['alteration_match']]

                writer.writerow([
                    sample, cancer_type, sample_alterations, alteration_match,
                    sp['tumor_match'], biomarker_drugs, biomarker_title, effect, biomarker.idx, resistances,
                    resistance_type, biomarker_tumors, evidence, source
                ])

    if bioactivities_file is not None:
        logging.info("Write bioactivities results")
        output_folder = os.path.dirname(output_file)
        output_filename = os.path.basename(output_file).replace(".tsv", "") + "_bioactivities.tsv"
        with open(os.path.join(output_folder, output_filename), "wt") as fd:
            writer = csv.writer(fd, delimiter='\t')
            writer.writerow([
                'SAMPLE', 'CANCER_TYPE', 'SYMBOL', 'SAMPLE_ALTERATION', 'MOA_MATCH',
                'MOLECULE_NAME', 'PACTIVITY_LABEL', 'MOA', 'DIRECTION', 'PACTIVITY_MEDIAN', 'MOLECULE_TYPE',
                'MOLECULE_STATUS'
            ])

            for (sample, cancer_type), prescriptions in bioactivities_prescriptions.items():
                for p in prescriptions:
                    row, match_alterations = p['bioactivity'].row, p['match']
                    sample_alterations = ', '.join([str(a) for a in match_alterations])

                    writer.writerow([
                        sample, cancer_type, row['SYMBOL'], sample_alterations, p['moamatch'],
                        row['MOLECULE_NAME'], row['PACTIVITY_LABEL'], row['MOA'], row['DIRECTION'],
                        row['PACTIVITY_median'], row['MOLECULE_TYPE'], row['MOLECULE_STATUS']
                    ])

    if store_json:
        logging.info("Write JSON results")
        with open(output_file + ".json", "wt") as fp:
            json_prescriptions = []
            for key, prescriptions in biomarkers_prescriptions.items():
                sample, cancer_type = key
                for sp in prescriptions:
                    item = {'sample': sample, 'cancer_type': cancer_type,
                            'sample_alterations': [a.row for a in sp['match']], 'biomarker': sp['biomarker'].row,
                            'alteration_match': level_map[sp['alteration_match']], 'tumor_match': sp['tumor_match'],
                            'resistances': [a.row for a in sp['resistance_list']]}
                    json_prescriptions.append(item)

            json.dump(json_prescriptions, fp)

    logging.info("Prescription finished")


def match_biomarkers(alterations, biomarkers, cancer_type, sample):
    tumor_type = Tumor(cancer_type)
    prescriptions = []
    for biomarker in biomarkers:

        level, matched_alterations = biomarker.match_alteration(alterations)
        match_cancer_type = biomarker.match_tumor(tumor_type)

        # Skip biomarkers with no match
        if level == MATCH_LEVEL_NONE:
            continue

        # Correct oncogenic classification
        if level == MATCH_LEVEL_COMPLETE:
            for a in matched_alterations:
                if a.perfect_match:
                    a.biomarker_tumors.update([t.name for t in biomarker.tumors])

        prescriptions.append({
            'sample': sample,
            'cancer_type': cancer_type,
            'biomarker': biomarker,
            'match': matched_alterations,
            'tumor_match': 1 if match_cancer_type else 0,
            'alteration_match': level,
        })

    # Check drug resistance
    resistances = [b for b in biomarkers if b.association in ["Resistant"]]
    check_drug_resistances(prescriptions, resistances, alterations)
    return prescriptions


def match_bioactivities(alterations, bioactivities, cancer_type, sample):
    # Driver alterations by gene
    driver_alterations_by_gene = defaultdict(list)
    for a in alterations:
        if a.driver:
            driver_alterations_by_gene[a.gene[0]].append(a)

    prescriptions = []
    for gene, driver_alterations in driver_alterations_by_gene.items():
        if gene in bioactivities:
            for bioactivity in bioactivities[gene]:
                level, matched_alterations = bioactivity.match_alteration(driver_alterations)

                # Skip biomarkers with no match
                if level == MATCH_LEVEL_NONE:
                    continue

                prescriptions.append({
                    'sample': sample,
                    'cancer_type': cancer_type,
                    'bioactivity': bioactivity,
                    'match': matched_alterations,
                    'moamatch': level == MATCH_LEVEL_COMPLETE
                })

    return prescriptions


def check_drug_resistances(prescriptions, resistances, sample_alterations):
    prescriptions_to_remove = []
    for prescription in prescriptions:

        # Set default values to NO resistance
        prescription['resistance'] = False
        prescription['resistance_list'] = []

        # Don't check resistances of negative prescriptions and resistances
        prescription_assoc = prescription['biomarker'].row['Association']
        if prescription_assoc in ['Resistant', 'No Responsive']:
            continue

        # Check if any resistance has any prescribed drugs
        for resistance in resistances:

            # Resistance has to do a complete match with sample alteration
            level, m = resistance.match_alteration(sample_alterations)
            match_cancer_type_resistance_biomarker = False

            if level == MATCH_LEVEL_COMPLETE:

                # Check if there is a perfect match between prescribed drugs and resistance drugs.
                drug_match = False
                if len(prescription['biomarker'].drugs) == len(resistance.drugs):
                    drug_match = True
                    for prescribed_drug in prescription['biomarker'].drugs:
                        is_prescribed_drug_a_resistance = False
                        for resistant_drug in resistance.drugs:
                            if prescribed_drug.match(resistant_drug):
                                is_prescribed_drug_a_resistance = True

                        if not is_prescribed_drug_a_resistance:
                            drug_match = False
                            break

                if drug_match:
                    # Match tumor types. Resistant tumor type can match either to sample or prescription tumor type
                    for t in prescription['biomarker'].tumors:
                        if resistance.match_tumor(t):
                            match_cancer_type_resistance_biomarker = True
                    if resistance.match_tumor(Tumor(prescription['cancer_type'])):
                        match_cancer_type_resistance_biomarker = True

                    if match_cancer_type_resistance_biomarker:
                        prescription['resistance'] = True
                        prescription['resistance_list'].append(resistance)
                        for resistance_alteration in m:
                            if resistance_alteration in prescription['match']:
                                prescription['match'].remove(resistance_alteration)
                                if len(prescription['match']) == 0:
                                    prescriptions_to_remove.append(prescription)
                        break

    for to_remove in prescriptions_to_remove:
        if to_remove in prescriptions:
            prescriptions.remove(to_remove)


def cmdline():
    # Parse the arguments
    parser = argparse.ArgumentParser()

    # Mandatory
    parser.add_argument('-i', '--input', dest='input_file', action='append', default=[], required=True,
                        help="Input alterations")
    parser.add_argument('-o', '--output', dest='output_file', default='output.tsv', help="Output file")

    # Optional
    parser.add_argument('-m', '--biomarkers', dest='biomarkers_file', default=None, help="Biomarkers file (optional)")
    parser.add_argument('-a', '--bioactivities', dest='bioactivities_file', default=None,
                        help="Bioactivities file (optional)")
    parser.add_argument('-t', '--tumors', dest='cancer_types_file', default=None, help="Cancer types file (optional)")
    parser.add_argument('--debug', dest='debug', default=False, action='store_true', help="More detailed execution")
    parser.add_argument('--json', dest='json', default=False, action='store_true',
                        help="Store results as a complete JSON file")
    parser.add_argument('--skip-bioactivities', dest='skip_bioactivities', default=False, action='store_true',
                        help="Skip bioactivities prescription")
    parser.add_argument('--write-mutations', dest='write_mutations', default=None,
                        help="Write mutations file correcting the driver statement if detected as known")

    args = parser.parse_args()

    # FIXME
    args.cancer_types_file = "/data/cgi/cancertypes/cancer_types.tsv"
    args.bioactivities_file = "/data/cgi/bioactivities/biomarkers_bioactivities_db.tsv.gz"
    args.biomarkers_file = "/data/cgi/biomarkers/cgi_biomarkers.tsv"

    # Configure the logging
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.debug(args)

    # Log version
    if __name__ != "__main__":
        from cancergenomeinterpreter import __version__
    else:
        __version__ = "DEVELOPMENT"
    logging.info("TCGI prescription version {}".format(__version__))

    bioactivities_file = None if args.skip_bioactivities else args.bioactivities_file

    # Run sample by sample
    run(args.input_file, args.output_file, args.biomarkers_file, bioactivities_file, args.cancer_types_file,
        args.write_mutations, store_json=args.json)


if __name__ == "__main__":
    cmdline()
