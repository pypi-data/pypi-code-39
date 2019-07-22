import urllib.request
from urllib.request import urlopen
import requests
import pymongo
import os.path


def load_protein_pdb(name_protein):
    fileDownload = "https://files.rcsb.org/download/" + name_protein + ".pdb" #Get the link
    request = requests.get(fileDownload) #Here is where im getting the status_code
    
    if request.status_code == 200: #Check out if a file exists
        Download = urlopen(fileDownload) #Open url
        file = open(name_protein, "wb") #Open the file, write binary
        file.write(Download.read()) #Read Download and write in file

def load_protein_fasta(name_protein):
    url = "https://www.rcsb.org/pdb/download/downloadFastaFiles.do?structureIdList=" + name_protein + "&compressionType=uncompressed"
    request = requests.get(url)
    
    if os.path.isfile(name_protein):
        if request.status_code == 200: #Check out if a file exists
                Download = urlopen(url) #Open url
                file = open(name_protein + '_fasta', "wb") #Open the file, write binary
                file.write(Download.read())

