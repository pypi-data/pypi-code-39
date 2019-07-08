import csv as _csv #To keep csv and os out of autocomplete
import os as _os
import pandas as _pd

__all__=['load_icd']


def load_hosp_locat():
    """
    Load a Pandas dataframe w/ hospital locations
    ##CONFIDENTIAL, dont put on GitHub
    
    """
    
    package_dir, init_file = _os.path.split(__file__)
    
    #fname = _os.path.join(package_dir, 'data','ca_coords.csv')
    return(1)
    #return(_pd.read_csv(fname))
    
    
def load_ca_locat():
    """
    Loads Geopandas dataframe with the the requisite type of data
    
    """
    return(1)
    


def load_icd(icd_ver = 9, icd_type = 'diagnosis', out_val = 'icd'):
    """
    Load ICD-9/10 codes, either procedure or diagnosis
    
    This function loads ICD-9/10 codes and returns either the full description or
    the description of the associated CCS category. Loads data from package. Function written by Marinka
    Zitnik and modified by Daniel Helkey
    
    Parameters:  
    icd_ver (int): This function supports ICD-9 and ICD-10
    
    icd_type (str): 'diagnosis'/'procedure'
    
    out_val (str): 'icd'/'ccs'
    """
    #CSV files are stored in the package subdirectory data/
    package_dir, init_file = _os.path.split(__file__)
   
  
    #Extract correct line length and location of code description
    options = { (9, 'procedure'):(3,2,4,'$prref 2015.csv'),
                    (9, 'diagnosis'):(3,2,6, '$dxref 2015.csv'),
                    (10, 'procedure'):(2,3,8, 'ccs_pr_icd10pcs_2017.csv'),
                    (10, 'diagnosis'):(2,3,8,'ccs_dx_icd10cm_2017.csv')
                    }
    descr_locat, ccs_locat, line_len, csv_name = options[(icd_ver, icd_type)]
    
    fname = _os.path.join(package_dir, 'data', 'icd', csv_name)

    code2descr = {}
    code2ccs = {}

    with open(fname) as fin:
        fin.readline()
        fin.readline()
        fin.readline() #First 3 lines don't have data
        csvreader = _csv.reader(fin)
        for line in csvreader:
            assert len(line) == line_len, 'Line not expected length'
            code = line[0].replace("'",'').strip()
            code2descr[code] = line[descr_locat]
            code2ccs[code] = line[ccs_locat]
        
        #Return either ICD code description or CCS category description
        out = {
            'icd':code2descr,
            'ccs':code2ccs
        }
        
        return(out[out_val])
