import argparse
import csv
import glob
import json
import logging
import os
import shutil
import subprocess
import sys
from os.path import join
from tempfile import mkdtemp

import cancergenomeinterpreter.cna.main as cna
import cancergenomeinterpreter.fus.main as fus
import cancergenomeinterpreter.utils.constants as ct
from cancergenomeinterpreter.cna.modules.input_preprocessing import which_cna_file
from cancergenomeinterpreter.fus.modules.input_preprocessing import is_fus_file
from cancergenomeinterpreter.utils import summary
from cancergenomeinterpreter.utils.lib import concat_files, create_folder, copytree


def cmdline():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input_files', action='append', default=[], required=True)
    parser.add_argument('-o', dest='output_directory', default="output")
    parser.add_argument('-l', '--local', dest='temporal_directory', default=os.getenv('TCGI_LOCAL_FOLDER', None),
                        help="Run in a local temporal folder and copy to output folder at the end")
    parser.add_argument('-t', dest='cancer_type', default='CANCER')
    parser.add_argument('--debug', dest='debug', default=False, action='store_true', help="Show more progress details")
    parser.add_argument('--temporal', dest='temporal_output', default=False, action='store_true',
                        help="Keep temporal files at the output")
    parser.add_argument('--json', dest='json', default=False, action='store_true',
                        help="Store results as a complete JSON file")
    parser.add_argument('--skip-bioactivities', dest='skip_bioactivities', default=False, action='store_true',
                        help="Skip bioactivities prescription")

    options = parser.parse_args()

    # Set output and run folders
    output_dir = create_folder(options.output_directory) if options.temporal_directory is None else mkdtemp(
        dir=options.temporal_directory)
    run_dir = join(output_dir, 'run')

    # Configure the logging
    handler_stdout = logging.StreamHandler(stream=sys.stdout)
    handler_file = logging.FileHandler(os.path.join(output_dir, 'cgi.log'))
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S',
                        handlers=[handler_stdout, handler_file])
    logging.getLogger().setLevel(logging.DEBUG if options.debug else logging.INFO)
    logging.debug(options)

    # Check valid cancer type
    cancer_type = options.cancer_type
    with open('/data/cgi/cancertypes/cancer_types.tsv', 'rt') as fd:
        tumors = {tumor['ID']: tumor for tumor in csv.DictReader(fd, delimiter='\t')}
        if cancer_type not in tumors:
            for t in tumors.values():
                logging.info("\t{} = {}".format(t['ID'], t['NAME']))
            logging.error("{} is not a valid cancer type. Check the list above.".format(cancer_type))
            sys.exit(-1)

    # Classify input files
    cna_files = []
    fus_files = []
    mut_files = []
    prescription_files = []
    for file in options.input_files:

        if which_cna_file(file) is not None:
            cna_files.append(file)
        elif is_fus_file(file):
            fus_files.append(file)
        else:
            mut_files.append(file)

    # OncodriveMUT
    if len(mut_files) > 0:
        mut_output = run_mut(mut_files, cancer_type, output_dir, join(run_dir, 'mut'), debug=options.debug)
        prescription_files.append(mut_output)
    else:
        mut_output = None

    # CNA
    if len(cna_files) > 0:
        cna_output = run_cna(cna_files, cancer_type, output_dir, join(run_dir, 'cna'))
        prescription_files.append(cna_output)

    # FUS
    if len(fus_files) > 0:
        fus_output = run_fus(fus_files, cancer_type, output_dir, join(run_dir, 'fus'))
        prescription_files.append(fus_output)

    # Drug prescription
    run_prescription(prescription_files, output_dir, json=options.json, write_mutations=mut_output, debug=options.debug,
                     skip_bioactivities=options.skip_bioactivities)

    # Summary statistics
    run_summary(cancer_type, output_dir)

    # Compress everything
    run_compress(output_dir)

    # Clean
    if not options.temporal_output:
        shutil.rmtree(os.path.join(output_dir, 'run'))
        os.unlink(os.path.join(output_dir, 'results_details.zip'))

    # Move everything
    if options.temporal_directory is not None:
        copytree(output_dir, options.output_directory)


def run_prescription(input_files, output_dir, write_mutations=None, json=False, debug=False, skip_bioactivities=False):
    logging.info("Running drug prescription")

    output_file = join(output_dir, ct.DRUG_PRESCRIPTION)

    cmd = ["cgi-prescription", "-o", output_file]
    for file in input_files:
        cmd += ['-i', file]

    if json:
        cmd.append("--json")
    if debug:
        cmd.append("--debug")
    if skip_bioactivities:
        cmd.append("--skip-bioactivities")

    if write_mutations is not None:
        cmd.append("--write-mutations {}".format(write_mutations))

    logging.debug(" ".join(cmd))
    ret_code = subprocess.call(" ".join(cmd), shell=True)
    if ret_code != 0:
        logging.error("Running '{}'".format(" ".join(cmd)))
        sys.exit(-1)

    return output_file


def run_compress(output_dir):
    logging.info("Compress results")
    cmd = [
        "cd", output_dir, ";"
                          "zip -q results.zip *.tsv *.txt; ",
        "zip -x *.zip -q -r results_details.zip *;"
    ]
    logging.debug(" ".join(cmd))
    ret_code = subprocess.call(" ".join(cmd), shell=True)
    if ret_code != 0:
        logging.error("Running '{}'".format(" ".join(cmd)))
        sys.exit(-1)


def run_summary(cancer_type, output_dir):
    # Create summary
    if os.path.exists(join(output_dir, 'metadata.json')):
        with open(join(output_dir, 'metadata.json'), 'rt') as fd:
            metadata = json.load(fd)
    else:
        metadata = {}
    metadata = summary.run(metadata, join(output_dir, ct.DRIVER_ARRANGED_MUTATIONS),
                           join(output_dir, ct.DRUG_PRESCRIPTION))
    metadata['cancer_type'] = cancer_type
    with open(join(output_dir, 'metadata.json'), 'wt') as fd:
        json.dump(metadata, fd, indent=4)


def run_mut(input_files, cancer_type, output_dir, run_dir, debug=False):
    logging.info("Running mutation analysis with OncodriveMUT")
    oncodrivemut_outputs = []
    not_mapped_lines = []

    for i, input_file in enumerate(input_files):
        run_dir_file = os.path.join(run_dir, '{:02d}'.format(i))
        os.makedirs(run_dir_file, exist_ok=True)

        # Calling oncodrivemut
        cmd = ["cgi-mut",
               "-i", input_file,
               "-o", run_dir_file,
               "-t", cancer_type,
               ]

        if debug:
            cmd.append("--debug")

        logging.debug(" ".join(cmd))
        ret_code = subprocess.call(" ".join(cmd), shell=True)
        if ret_code != 0:
            logging.error("Running '{}'".format(" ".join(cmd)))
            sys.exit(-1)

        # Read not mapped files
        for nmf in glob.glob(os.path.join(run_dir_file, "tmp", "not_mapped_*")):
            with open(nmf, 'rt') as fd:
                not_mapped_lines += fd.readlines()[1:]

        oncodrivemut_outputs.append(join(run_dir_file, ct.DRIVER_ARRANGED_MUTATIONS))

    output_file = join(output_dir, ct.DRIVER_ARRANGED_MUTATIONS)
    concat_files(oncodrivemut_outputs, output_file)

    if len(not_mapped_lines) > 0:
        notmapped_file = join(output_dir, ct.NOT_MAPPED)
        with open(notmapped_file, "wt") as fd:
            fd.writelines(not_mapped_lines)

    logging.info("Alteration analysis finished")
    return output_file


def run_cna(input_files, cancer_type, output_dir, run_dir):
    logging.info("Running CNA")
    cna_outputs = []
    malformed_lines = []

    for i, input_file in enumerate(input_files):
        run_dir_file = os.path.join(run_dir, '{:02d}'.format(i))
        os.makedirs(run_dir_file, exist_ok=True)
        cna.run(input_file, cancer_type, run_dir_file)
        cna_outputs.append(join(run_dir_file, ct.CGI_CNAS))

        # Read not mapped files
        for nmf in glob.glob(os.path.join(run_dir_file, "malformed_*")):
            with open(nmf, 'rt') as fd:
                malformed_lines += fd.readlines()[1:]

    output_file = join(output_dir, ct.CGI_CNAS)
    concat_files(cna_outputs, output_file)

    if len(malformed_lines) > 0:
        malformed_file = join(output_dir, ct.MALFORMED_CNAS)
        with open(malformed_file, "wt") as fd:
            fd.writelines(malformed_lines)

    logging.info("Alteration analysis finished")
    return output_file


def run_fus(input_files, cancer_type, output_dir, run_dir):
    logging.info("Running fusions")
    fus_outputs = []
    for i, input_file in enumerate(input_files):
        run_dir_file = os.path.join(run_dir, '{:02d}'.format(i))
        os.makedirs(run_dir_file, exist_ok=True)
        fus.run(input_file, cancer_type, run_dir_file)
        fus_outputs.append(join(run_dir_file, ct.CGI_FUS))

    output_file = join(output_dir, ct.CGI_FUS)
    concat_files(fus_outputs, output_file)

    logging.info("Alteration analysis finished")
    return output_file


if __name__ == "__main__":
    cmdline()
