import requests
import urllib.request
from urllib.request import urlopen
from xml.dom import minidom
from Bio.SeqUtils import seq1
from Bio import SeqIO
from itertools import groupby
import string
import os.path as path
import string

import pymongo
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client["project"]
collection = db["proteins"]

from projest import atom, model, chain, protein, extract_atoms_information, aminoacid

class Protein(object):

    def __init__(self, protein_name):
        self.protein_name = protein_name
        extract_atoms_information.load_protein_pdb(self.protein_name) #It creates automatically so, we dont have to do it. #Protein_pdb
        extract_atoms_information.load_protein_fasta(self.protein_name) #Protein_fasta
        try: #Check it if exists in mongodb to insert
            self.general_dictionary()
        except: 
            db.protein.find({"_id":self.protein_name}) == True
    
    def get_sequence_aminoacids (self): #Returns a list with chain and the sequence
        sequences = {}
        open_fasta = list(SeqIO.parse(self.protein_name + "_fasta", 'fasta')) #Show all sequences with information in the file
        chain = (len(open_fasta)-1) #Counts how many chains there are, but we have to keep in mind the 0. We subtract 1 
        chains = self.get_chain_list()
        while chain >=0:
            sequence = open_fasta[chain].seq
            sequences[chains[chain]] = str(sequence)
            chain -=1
        return sequences

    def get_chain_list(self): #Return the differents chains there are
        list_differents_chains = []
        with open(self.protein_name, 'r+') as text_file:
            for line in text_file:
                if line.startswith("ATOM"):
                    chain.Chain.chain_identifier = line[21]
                    chain_identifier = chain.Chain.chain_identifier.strip()
                    if chain_identifier not in list_differents_chains:
                        list_differents_chains.append(chain_identifier)
            return list_differents_chains

    def get_aminoacid_list(self): #Return the differents aminoacids with the differents sequence number classified in chains
        protein = {}
        with open(self.protein_name, 'r+') as text_file:
            for line in text_file:
                if line.startswith("ATOM"):
                    chain.Chain.chain_identifier = line[21]
                    chain_identifier = chain.Chain.chain_identifier.strip()

                    aminoacid.Aminoacid.residue_name = line[17:20]
                    residue_name = aminoacid.Aminoacid.residue_name.strip()

                    aminoacid.Aminoacid.residue_sequence_number = line[22:26]
                    residue_sequence_number = aminoacid.Aminoacid.residue_sequence_number.strip()
                    
                    chain_letter = protein.setdefault(chain_identifier, {})
                    residue_letter = chain_letter.setdefault(residue_name, [])
                    if residue_sequence_number not in residue_letter:
                        residue_letter.append(residue_sequence_number)
        return protein

    def get_similar_protein(self): 
        #SALE LA MISMA PROTEINA QUE INTRODUZCO EN ALGUNAS (EJ. 2F40)
        dicc_hit_def = {}
        open_fasta = list(SeqIO.parse(self.protein_name + "_fasta", 'fasta')) #Show all sequences with information in the file
        chain = (len(open_fasta)-1) #Counts how many chains there are, but we have to keep in mind the 0. We subtract 1 
        while chain >=0:
            fasta_sequence = open_fasta[chain].seq #We want the sequence
            url = "https://www.rcsb.org/pdb/rest/getBlastPDB1?sequence=" + str(fasta_sequence) + "&eCutOff=10.0&matrix=BLOSUM62&outputFormat=XML" #TENGO QUE HACER QUE ME DIGA EL NOMBRE DE LA PROTEINA
            request = requests.get(url) #Here is where im getting the status_code
            file_protein_pdb = "similar_protein_" + self.protein_name #The name that the file will have

            if request.status_code == 200: #Check out if a file exists
                Download = urlopen(url) #Download pdb
                file = open(file_protein_pdb, "wb") #I want to write in bytes in file_protein_pdb
                file.write(Download.read()) 
                file.close()
                doc = minidom.parse(file_protein_pdb) #This is for read the xml
                hits = doc.getElementsByTagName("Hit") #Keep what find in the tag hit in hits.
                if hits != []: #There are wrong chains so they are empty because of there isnt "hit"
                    hit_def = hits[0].getElementsByTagName("Hit_def")[0] #Define Hit_def
                    hit_def = hit_def.firstChild.data #I want values of hit_def
                    hit_def = hit_def[0:4] #I only want 4 first values of hit_def
                    dicc_hit_def[open_fasta[chain].id[5]]=hit_def #Add to the dictionary
                    chain = chain-1
                else: 
                    dicc_hit_def[open_fasta[chain].id[5]] = None
                    chain = chain-1
        return dicc_hit_def

    def general_dictionary(self): #To insert in mongodb. Its automatically

        model_count = 0

        protein = {"_id":self.protein_name}
        model_dictionary = {}

        with open(self.protein_name, 'r+') as text_file:
            for line in text_file:
                if line.startswith("MODEL"):
                    #MODEL
                    model_count +=1

                    model.Model.model_identifier = line[11:17]
                    model_identifier = model.Model.model_identifier.strip() #Model identifier has blanks, I want this value without them
                    model_dictionary.setdefault("MODEL " + model_identifier, {})
                    #setdefault equals the first value to the second if it doesnt exist

                if not model_count: #When we have only one model we dont have any model count neither model_identifier
                    model_identifier = "1"
                    model_dictionary["MODEL 1"]={}

                if line[:4] == 'ATOM':
                    #CHAIN
                    chain.Chain.chain_identifier = line[21]
                    chain_identifier = chain.Chain.chain_identifier.strip()

                    #AMINOACID
                    aminoacid.Aminoacid.residue_name = line[17:20]
                    residue_name = aminoacid.Aminoacid.residue_name.strip()

                    aminoacid.Aminoacid.residue_sequence_number = line[22:26]
                    residue_sequence_number = aminoacid.Aminoacid.residue_sequence_number.strip()

                    #ATOM
                    atom.Atom.atom_name = line[12:16]
                    atom_name = atom.Atom.atom_name.strip()

                    atom.Atom.x_coordinate = line[30:38]
                    x_coordinate = float(atom.Atom.x_coordinate.strip())

                    atom.Atom.y_coordinate = line[38:46]
                    y_coordinate = float(atom.Atom.y_coordinate.strip())

                    atom.Atom.z_coordinate = line[46:54]
                    z_coordinate = float(atom.Atom.z_coordinate.strip())

                    atom.Atom.occupancy = line[54:60]
                    occupancy = float(atom.Atom.occupancy.strip())

                    atom.Atom.temperature_factor = line[60:66]
                    temperature_factor = float(atom.Atom.temperature_factor.strip())

                    atom.Atom.element_symbol = line[76:78]
                    element_symbol = atom.Atom.element_symbol.strip()

                    model_id = protein.setdefault("MODEL " + model_identifier, {})
                    chain_letter = model_id.setdefault(chain_identifier, {})
                    residue_letter = chain_letter.setdefault(residue_name, {})
                    residue_number = residue_letter.setdefault(residue_sequence_number, {})
                    atom_letter = residue_number.setdefault(element_symbol, {})

                    atom_letter[atom_name] = {
                        "x_coordinate":x_coordinate, 
                        "y_coordinate":y_coordinate, 
                        "z_coordinate":z_coordinate, 
                        "occupancy":occupancy, 
                        "temperature_factor":temperature_factor,
                    }
            collection.insert_one(protein) #Insert in mongodb
