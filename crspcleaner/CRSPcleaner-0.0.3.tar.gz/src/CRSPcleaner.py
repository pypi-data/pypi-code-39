"""
This programme cleans the CRSP (csv) database and returns it as a pandas dataframe.
It extracts CIK identifers for firms, too.

"""



def cleanCRSP(withCIKonly=False):
    # Import package dependencies
    import pandas as pd
    import os
    from dateutil.relativedelta import relativedelta

    path_to_file = os.path.join(input("Please specify path to CRSP csv file including the file."))
    # path_to_db = os.path.join(r"/Volumes/d$/PhD/Research/databases/")
    print("Importing CRSP database now...")
    crsp_raw = pd.read_csv(path_to_file)
    # crsp_raw = pd.read_csv(path_to_db + 'crsp/crsp_fullUniverse_19251231_20181231.csv')

    print("CRSP imported. Cleaning now...")
    # Convert all columns to lowercase and add crsp suffix
    crsp_raw.rename(columns = lambda name : name.lower() + '_crsp',
                    inplace=True)

    # Convert dates to pd datetime objects
    if isinstance(crsp_raw['date_crsp'][0], str):
        crsp_raw['date_crsp'] = pd.to_datetime(crsp_raw['date_crsp'], format="%Y-%m-%d")
    else:
        crsp_raw['date_crsp'] = pd.to_datetime(crsp_raw['date_crsp'], format='%Y%m%d')

    # Clean numerical data
    numeric_col_names = ['dlprc_crsp', 'dlret_crsp', 'dlretx_crsp',
                         'prc_crsp', 'ret_crsp', 'retx_crsp',
                         'shrout_crsp', 'vwretd_crsp', 'vwretx_crsp',
                         'ewretd_crsp', 'ewretx_crsp', 'sprtrn_crsp',
                         'siccd_crsp']

    for col in numeric_col_names:
        if col in crsp_raw.columns:
            crsp_raw[col] = pd.to_numeric(crsp_raw[col], errors='coerce')

    for col in crsp_raw[['dlprc_crsp', 'prc_crsp']]:
        crsp_raw[col] = abs(crsp_raw[col])

    crsp_raw.dropna(subset=['retx_crsp'], inplace=True)
    crsp_raw.reset_index(inplace=True, drop=True)

    # Extract CUSIPs and merge with CRSP
    print("Extracting CIKs and CUSIPs now...")
    crsp_compu_firm_matches = pd.read_csv('http://vash.uk/wp-content/uploads/2019/07/crsp_compu_firm_identifiers_match_main-1.csv')

    # Convert cik to string, set all NaN to 0
    crsp_compu_firm_matches.dropna(subset=['cik'], inplace=True)

    # Convert Cusip to string, then extract 1st 8 characters in a separate column
    # This is necessary because CRSP only uses the 1st 8 characters as its Cusip
    crsp_compu_firm_matches['cusip'] = crsp_compu_firm_matches['cusip'].astype(str)

    crsp_compu_firm_matches['cusip_first8Characters'] = crsp_compu_firm_matches['cusip'].apply(
    	lambda cusip : cusip[:-1]
    )

    # Extract identifiers only
    crsp_compu_firm_matches = crsp_compu_firm_matches[['cusip', 'cusip_first8Characters', 'cik', 'conm', 'tic']]
    crsp_compu_firm_matches.drop_duplicates(inplace=True)
    crsp_compu_firm_matches = crsp_compu_firm_matches[
        crsp_compu_firm_matches['cusip_first8Characters'] != 'na']

    crsp_compu_firm_matches.reset_index(inplace=True, drop=True)

    print("Merging CIK identifiers with CRSP")
    # Merge CRSP with CUSIP and CIK list
    crsp_cleaned = crsp_raw.merge(crsp_compu_firm_matches, left_on = 'cusip_crsp',
    										right_on = 'cusip_first8Characters',
    										how = 'left')
    del crsp_raw
    del crsp_compu_firm_matches

    crsp_cleaned['date_crsp_shifted'] = crsp_cleaned['date_crsp'].apply(
        lambda date : date + relativedelta(day = 1, months = +1, days = -1))


    crsp_cleaned = crsp_cleaned[~crsp_cleaned['siccd_crsp'].between(
        6000, 6999, inclusive=True)]
    crsp_cleaned = crsp_cleaned[crsp_cleaned['prc_crsp'] >= 1]
    crsp_cleaned = crsp_cleaned[crsp_cleaned['retx_crsp'] < 2]

    crsp_cleaned.drop_duplicates(inplace=True)

    crsp_cleaned.drop_duplicates(subset=['date_crsp_shifted', 'permno_crsp', 'retx_crsp'],
                                 inplace=True)

    crsp_cleaned.reset_index(inplace=True, drop=True)

    print("Cleaning complete. Exporting as df now...")

    if withCIKonly:
        crsp_cleaned.dropna(subset=['cik'], inplace=True)
        crsp_cleaned.reset_index(inplace=True, drop=True)

    return crsp_cleaned



if __name__ == '__main__':
    cleanCRSP()
