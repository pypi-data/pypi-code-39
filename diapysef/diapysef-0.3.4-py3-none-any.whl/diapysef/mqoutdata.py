#!/usr/bin/env python
from __future__ import print_function
import os, sys
import pandas as pd
import numpy as np
import sqlite3
#from .timsdata import TimsData #!!change!!#

class MQData:
    def __init__ (self, maxquant_directory):
        if(not os.path.exists(maxquant_directory)):
            raise ValueError("Directory: %s not found. Please make sure that you specified the right directory." % maxquant_directory)
        self.evidence_data = os.path.join(maxquant_directory, "evidence.txt")
        print(self.evidence_data)
        print(os.path.exists(self.evidence_data))
        self.msms_data = os.path.join(maxquant_directory, "msms.txt")
        print(self.msms_data)
        self.all_peptides_data = os.path.join(maxquant_directory, "allPeptides.txt")
        print(self.all_peptides_data)

    def get_evidence (self):
        """Reads the evidence output of maxquant as pandas dataframe."""
        try:
            self.evidence = pd.read_table(self.evidence_data)
        except:
            print("Data File %s not found. Make sure you specified the right directory." % self.evidence_data)

    def get_msms (self):
        """Reads the msms output of maxquant as pandas dataframe."""
        try:
            self.msms = pd.read_table(self.msms_data)
        except:
            print("Data File %s not found. Make sure you specified the right directory." % self.msms_data)

    def get_all_peptides (self):
        """Reads the allPeptides output of maxquant as pandas dataframe."""
        try:
            self.all_peptides = pd.read_table(self.all_peptides_data)
        except:
            print("Data File %s not found. Make sure you specified the right directory." % self.all_peptides_data)

class PasefMQData:

    def __init__ (self, maxquant_directory):
        if(not os.path.exists(maxquant_directory)):
            raise ValueError("Directory: %s not found. Please make sure that you specified the right directory." % maxquant_directory)
        self.evidence_data = os.path.join(maxquant_directory, "evidence.txt")
        self.msms_data = os.path.join(maxquant_directory, "msms.txt")
        self.all_peptides_data = os.path.join(maxquant_directory, "allPeptides.txt")

    def get_evidence (self, timsdata = None):
        """Reads the evidence output of maxquant as pandas dataframe."""
        try:
            self.evidence = pd.read_table(self.evidence_data)
        except:
            print("Data File %s not found. Make sure you specified the right directory." % self.evidence_data)
        if timsdata is not None:
            self.annotate_ion_mobility(timsdata)

    def get_msms (self):
        """Reads the msms output of maxquant as pandas dataframe."""
        try:
            self.msms = pd.read_table(self.msms_data)
        except:
            print("Data File %s not found. Make sure you specified the right directory." % self.msms_data)

    def get_all_peptides (self, timsdata = None):
        """Reads the allPeptides output of maxquant as pandas dataframe."""
        try:
            self.all_peptides = pd.read_table(self.all_peptides_data)
        except:
            print("Data File %s not found. Make sure you specified the right directory." % self.all_peptides_data)
        if timsdata is not None:
            self.annotate_ion_mobility(timsdata)

    def annotate_ion_mobility (self, pasef_data):
        """Adds ion mobility colums to the maxquant results that are currently loaded."""
        if hasattr(self, 'all_peptides'):
            self.all_peptides['IonMobilityIndexK0'] = pasef_data.scanNumToOneOverK0(1,self.all_peptides['Ion mobility index'])

        if hasattr(self, 'evidence'):
            self.evidence['IonMobilityIndexK0'] = pasef_data.scanNumToOneOverK0(1,self.evidence['Ion mobility index'])
    def convert_to_lib(self, irt_file):
        if hasattr(self, 'msms') & hasattr(self, 'evidence'):
            pasef_to_lib(self.evidence, self.msms, irt_file)
        else:
            print("Msms and evidence need to be present for library generation")
            sys.exit()

