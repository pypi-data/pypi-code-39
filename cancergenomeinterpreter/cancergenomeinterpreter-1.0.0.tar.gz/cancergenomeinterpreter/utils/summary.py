import os

import pandas as pd


def run(metadata, oncodrivemut_file, prescriptions_file):
    if os.path.exists(oncodrivemut_file):
        oncodrivemut_dataset = pd.read_csv(oncodrivemut_file, sep='\t')
        drivers_dataset = oncodrivemut_dataset[oncodrivemut_dataset['driver'].isin(['known', 'predicted'])]
        metadata['analysed_mutations'] = len(oncodrivemut_dataset)
        metadata['drivers'] = len(drivers_dataset)
        metadata['known'] = len(oncodrivemut_dataset[oncodrivemut_dataset['driver'].isin(['known'])])
        metadata['predicted'] = len(oncodrivemut_dataset[oncodrivemut_dataset['driver'].isin(['predicted'])])
        metadata['samples'] = len(oncodrivemut_dataset['sample'].unique())
        metadata['mutations_per_sample'] = oncodrivemut_dataset.groupby('sample').size().median()
        metadata['drivers_per_sample'] = drivers_dataset.groupby('sample').size().median() if len(
            drivers_dataset) > 0 else 0
        metadata['samples_without_drivers'] = metadata['samples'] - len(drivers_dataset['sample'].unique())

    if os.path.exists(prescriptions_file):
        prescriptions_dataset = pd.read_csv(prescriptions_file, sep='\t')
        metadata['prescription_complete'] = len(prescriptions_dataset[(prescriptions_dataset['TUMOR_MATCH'] == 1) & (
                    prescriptions_dataset['ALTERATION_MATCH'] == 'complete')])
        metadata['prescription_repurposing'] = len(prescriptions_dataset[(prescriptions_dataset['TUMOR_MATCH'] == 0) & (
                    prescriptions_dataset['ALTERATION_MATCH'] == 'complete')])

    return metadata
