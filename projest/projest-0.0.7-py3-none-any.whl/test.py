import unittest
import os

import pymongo
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client["project"]
collection = db["proteins"]

from projest import protein

class TestProject(unittest.TestCase):

    def test_get_sequence_aminoacids(self):
        p = protein.Protein("5iz6")
        sequence = p.get_sequence_aminoacids()
        self.assertEqual({'B': 'XAGEALYEX', 'A': 'MGHHHHHHMLHLLEQIRAYCETCWEWQEAHEPGMDQDKNPMPAPVEHQICPAVCVLMKLSFDEEHRHAMNELGGLQAIAELLQVDCEMYGLTNDHYSITLRRYAGMALTNLTFGDVANKATLCSMKGCMRALVAQLKSESEDLQQVIASVLRNLSWRADVNSKKTLREVGSVKALMECALEVKKESTLKSVLSALWNLSAHCTENKADICAVDGALAFLVGTLTYRSQTNTLAIIESGGGILRNVSSLIATNEDHRQILRENNCLQTLLQHLKSHSLTIVSNACGTLWNLSARNPKDQEALWDMGAVSMLKNLIHSKHKMIAMGSAAALRNLMANRPAKYKDANIMSPGSSLPS'}, sequence)

    def test_get_chain_list(self):
        p = protein.Protein("5iz6")
        chain_list = p.get_chain_list()
        self.assertEqual(['A', 'B'], chain_list) 

    def test_get_aminoacid_list(self):
        p = protein.Protein("5iz6")
        aminoacid_list = p.get_aminoacid_list()
        self.assertEqual({'A': {'HIS': ['403', '404', '405', '408', '427', '444', '462', '464', '492', '598', '652', '668', '672', '712', '715'], 'MET': ['406', '438', '454', '466', '485', '503', '522', '526', '573', '701', '706', '717', '720', '730'], 'LEU': ['407', '409', '410', '453', '456', '469', '472', '478', '479', '488', '497', '505', '508', '519', '529', '533', '540', '548', '551', '563', '572', '577', '585', '589', '592', '595', '613', '616', '620', '629', '639', '645', '656', '662', '665', '666', '669', '674', '684', '687', '698', '707', '710', '726', '729'], 'GLU': ['411', '418', '422', '425', '443', '460', '461', '468', '477', '484', '536', '538', '565', '574', '578', '582', '601', '633', '650', '658', '696'], 'GLN': ['412', '424', '445', '473', '480', '532', '541', '542', '625', '654', '663', '667', '695'], 'ILE': ['413', '446', '475', '495', '544', '606', '631', '632', '638', '646', '655', '676', '711', '718'], 'ARG': ['414', '463', '498', '499', '527', '549', '554', '564', '623', '640', '653', '657', '690', '727', '733'], 'ALA': ['415', '426', '440', '449', '465', '474', '476', '501', '504', '514', '517', '528', '531', '545', '555', '571', '576', '591', '597', '604', '608', '612', '614', '630', '647', '680', '689', '697', '703', '719', '723', '724', '725', '731', '735', '740'], 'TYR': ['416', '486', '493', '500', '622', '737'], 'CYS': ['417', '420', '447', '451', '483', '520', '525', '575', '599', '607', '661', '681'], 'THR': ['419', '489', '496', '506', '509', '518', '562', '584', '600', '619', '621', '626', '628', '648', '664', '675', '683'], 'TRP': ['421', '423', '553', '593', '685', '699'], 'ASN': ['436', '467', '490', '507', '515', '550', '558', '594', '602', '627', '641', '649', '659', '660', '679', '686', '691', '709', '728', '732', '741'], 'PRO': ['437', '439', '441', '448', '692', '734'], 'VAL': ['442', '450', '452', '481', '513', '530', '543', '547', '557', '566', '569', '579', '588', '609', '617', '642', '677', '704'], 'LYS': ['455', '516', '523', '534', '560', '561', '570', '580', '581', '586', '603', '670', '693', '708', '714', '716', '736', '738'], 'SER': ['457', '494', '521', '535', '537', '546', '552', '559', '568', '583', '587', '590', '596', '624', '634', '643', '644', '671', '673', '678', '688', '705', '713', '722'], 'PHE': ['458', '510', '615'], 'ASP': ['459', '482', '491', '512', '539', '556', '605', '610', '651', '694', '700', '739'], 'GLY': ['470', '471', '487', '502', '511', '524', '567', '611', '618', '635', '636', '637', '682', '702', '721']}, 'B': {'ALA': ['1', '4'], 'GLY': ['2'], 'GLU': ['3', '7'], 'LEU': ['5'], 'TYR': ['6']}}
, aminoacid_list) 

    def test_get_similar_protein(self):
        p = protein.Protein("5iz6")
        similarity = p.get_similar_protein()
        self.assertEqual({'B': None, 'A': '5IZA'}, similarity) 

    def test_general_dictionary(self):
        protein.Protein("5iz6")
        variable = False
        if db.proteins.count({"_id":"5iz6"}) == 1:
            variable = True
        self.assertTrue(variable)

    def test_load_protein_pdb(self):
        name = protein.Protein("5iz6").protein_name
        path = name

        if os.path.isfile(path):
            variable = True
        else: 
            variable = False
        self.assertTrue(variable)

    def test_load_protein_fasta(self):
        name = protein.Protein("5iz6").protein_name
        path = name + "_fasta"

        if os.path.isfile(path):
            variable = True
        else: 
            variable = False
        self.assertTrue(variable)

if __name__ == '__main__':
    unittest.main()