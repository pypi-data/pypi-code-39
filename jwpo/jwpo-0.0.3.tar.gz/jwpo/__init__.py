"""Jared Warner's Personalized Opportunitites

Written by Grant Jenks
Copyright 2019

"""

import argparse
import logging
import os

import openpyxl


log = logging.getLogger('jwpo')  # pylint: disable=invalid-name


def main(argv=None):
    "Main entry-point for Jared Warner's Personalized Opportunities."
    description = __doc__.splitlines()[0]
    parser = argparse.ArgumentParser('jwpo', description=description)
    parser.add_argument('opportunities_file', type=argparse.FileType('r'))
    parser.add_argument('gradebook_file', type=argparse.FileType('rb'))
    parser.add_argument('opportunity_number', type=int)
    parser.add_argument('opportunity_name')
    parser.add_argument('output_directory')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--verbose', action='store_true')
    group.add_argument('--quiet', action='store_true')

    args = parser.parse_args(argv)
    setup_logging(args)

    log.info("Starting Jared Warner's Personalized Opportunities")
    create_output_dir(args.output_directory)
    opportunities = parse_opportunities_file(args.opportunities_file)
    gradebook = parse_gradebook_file(args.gradebook_file)
    generate_opportunities(args, opportunities, gradebook)
    log.info("Finishing Jared Warner's Personalized Opportunities")


def setup_logging(args):
    "Setup logging."
    if args.verbose:
        level = logging.DEBUG
    elif args.quiet:
        level = logging.WARNING
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format='%(levelname)s:%(message)s',
    )


def create_output_dir(output_directory):
    "Create output directory."
    log.info('Creating output directory: %s', output_directory)
    os.makedirs(output_directory, exist_ok=True)


def parse_opportunities_file(opportunities_file):
    "Parse opportunities file."
    log.info('Parsing opportunities file: %s', opportunities_file.name)
    return {}


def parse_gradebook_file(gradebook_file):
    "Parse gradebook file."
    log.info('Parsing gradebook file: %s', gradebook_file.name)
    return {}


def generate_opportunities(args, opportunities, gradebook):
    "Generate opportunities."
    # pylint: disable=unused-argument
    output_directory = args.output_directory
    opportunity_number = args.opportunity_number
    opportunity_name = args.opportunity_name
    log.info('Generating opportunities in %s', output_directory)
    log.info('Using opportunity number: %d', opportunity_number)
    log.info('Using opportunity name: %s', opportunity_name)


__title__ = "Jared Warner's Personalized Opportunities"
__version__ = '0.0.3'
__build__ = 0x000003
__author__ = 'Grant Jenks'
__license__ = 'Apache 2.0'
__copyright__ = '2019, Grant Jenks'
