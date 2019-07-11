import logging
import os

import numpy as np
import pandas as pd

import cancergenomeinterpreter.mut.modules.driver_rules as dr
import cancergenomeinterpreter.mut.modules.lib as lib
import cancergenomeinterpreter.mut.utils.constants as ct


def insert_gene_driver_category_and_source(mutations_df, config):
    def collapse_values(se):
        e = ct.SEPARATOR.join(list(se))
        s = e.split(ct.SEPARATOR) if ct.SEPARATOR in e else [e]
        return ct.SEPARATOR.join(list(set(s)))  # ct.SEPARATOR.join(list(set(list(se))))

    '''def is_driver_gene(gene, tumor_drivers, other_tumor_drivers):

        if gene in tumor_drivers:
            return ct.TUMOR_DRIVER
        elif gene in other_tumor_drivers:
            return ct.OTHER_TUMOR_DRIVER
        else:
            return np.nan'''

    logging.debug('Checking gene driver category..')

    def recode_sources(e):
        if 'tcga_update' in e:
            return 'intogen'
        return e

    # some formating of the file with the driver genes per cancer type info
    drivers_df = pd.read_csv(config['drivers_fp'], sep='\t')
    drivers_df = drivers_df.rename(columns={drivers_df.columns[0]: ct.GENE, drivers_df.columns[1]: ct.CANCER,
                                            drivers_df.columns[2]: ct.DRIVER_GENE_SOURCE})
    drivers_df[ct.CANCER] = drivers_df.apply(lambda row: row[ct.CANCER].replace(',', ct.SEPARATOR), axis=1)
    drivers_df[ct.DRIVER_GENE_SOURCE] = drivers_df.apply(
        lambda row: row[ct.DRIVER_GENE_SOURCE].replace(',', ct.SEPARATOR), axis=1)
    drivers_df[ct.DRIVER_GENE_SOURCE] = drivers_df[ct.DRIVER_GENE_SOURCE].map(recode_sources)

    # if cancer is pancancer, all the cancers are included (although this is probably unecessary,
    # since it has been already calculated this way)
    tumor_offspring = config['tumor_offspring'] if config['tumor_type'] != ct.PANCANCER else drivers_df[
        ct.CANCER].unique()

    # create the dataframe with the driver genes of the sample cancer type and another dataframe with
    # the driver genes of the remaining cancers
    tumor_drivers_df = drivers_df[drivers_df[ct.CANCER].isin(tumor_offspring)]
    other_tumor_drivers_df = drivers_df[np.invert(drivers_df[ct.CANCER].isin(tumor_offspring))]
    # in case (due to tumor offspring issues) there are more than one 'gene-tumor_type-evidence' entry,
    # collapse the info
    tumor_drivers_df = tumor_drivers_df.groupby(ct.GENE).agg(collapse_values).reset_index()
    other_tumor_drivers_df = other_tumor_drivers_df.groupby(ct.GENE).agg(collapse_values).reset_index()

    # put the column to allow the merge
    tumor_drivers_df[ct.DRIVER_GENE] = ct.TUMOR_DRIVER
    other_tumor_drivers_df[ct.DRIVER_GENE] = ct.OTHER_TUMOR_DRIVER

    # create the driver dataframe to be merged with the input mutations dataframe
    if len(tumor_drivers_df) == 0:
        logging.warning(
            'There are no drivers specific to sample tumor and offspring {0}'.format(config['tumor_offspring']))
        drivers_df = other_tumor_drivers_df
        config['sample_drivers'] = 'none'
    elif len(other_tumor_drivers_df) == 0:
        logging.warning(
            'The whole catalog of driver genes are considered as specific of the {0} sample under analysis '.format(
                config['tumor_type']))
        drivers_df = tumor_drivers_df
        config['sample_drivers'] = 'generic'
    else:
        logging.info('Considering as sample specific the {0} driver genes of tumors: {1}'
                     .format(len(tumor_drivers_df),
                             ','.join(lib.intersect_lists([tumor_offspring, drivers_df[ct.CANCER]]))
                             )
                     )

        drivers_df = tumor_drivers_df.append(
            other_tumor_drivers_df[np.invert(other_tumor_drivers_df[ct.GENE].isin(tumor_drivers_df[ct.GENE].unique()))])
        config['sample_drivers'] = len(tumor_drivers_df)

    # and then merge
    mutations_df = mutations_df.merge(drivers_df[[ct.GENE, ct.DRIVER_GENE, ct.DRIVER_GENE_SOURCE]], how='left',
                                      on=ct.GENE)

    # fill the column of driver_gene category
    # mutations_df[ct.DRIVER_GENE] = mutations_df.apply(lambda row: is_driver_gene(row[ct.GENE], tumor_drivers,
    #                                                                             other_tumor_drivers), axis=1)

    return mutations_df, config


def insert_gene_role(mutations_df, config):
    # if a gene stated as driver has no role, i state it as having an unknown (ambigous) role
    def solve_na_role(mutations_df):
        tmp_df = mutations_df[(np.invert(mutations_df[ct.DRIVER_GENE].isnull())) & (
            mutations_df[ct.GENE_ROLE].isnull())].drop_duplicates()
        if len(tmp_df) > 0:
            logging.debug(
                'The following genes have no role stated, default "ambigous" will be used for them: {0}'.format(
                    ','.join(tmp_df[ct.GENE].unique())))
            mutations_df[ct.GENE_ROLE] = np.where(mutations_df[ct.GENE].isin(tmp_df[ct.GENE]), ct.AMBIGUOUS,
                                                  mutations_df[ct.GENE_ROLE])

        return mutations_df

    logging.debug('Checking gene role..')

    role_df = pd.read_csv(config['gene_role_fp'], sep='\t')
    role_df = role_df.rename(columns={role_df.columns[0]: ct.GENE, role_df.columns[-1]: ct.GENE_ROLE})

    mutations_df = mutations_df.merge(role_df[[ct.GENE, ct.GENE_ROLE]], how='left', on=ct.GENE)

    mutations_df = solve_na_role(mutations_df)

    return mutations_df


def insert_mut_is_in_cluster(mutations_df, config):
    def check_in_cluster(aa_pos, gene_clusters):

        # awfulll, to improve
        if type(gene_clusters) == str and aa_pos != '.':
            gene_clusters = gene_clusters.replace('cluster', '').replace('[', '').replace(']', '').replace(' ',
                                                                                                           '').replace(
                '(', '')
            for clust in gene_clusters.split('),'):
                positions = clust.replace(')', '').split(',')
                try:
                    if int(positions[0]) <= int(aa_pos) <= int(positions[1]):
                        return ct.IN_CLUSTER
                except Exception:
                    logging.warning('Some problem when reading clister {0}'.format(gene_clusters))
                    return ''
        return ''

    logging.debug('Checking mutations in clusters..')

    # read the cluster file
    clusters_df = pd.read_csv(config['clusters_fp'], sep='\t')
    clusters_df = clusters_df.rename(columns={clusters_df.columns[0]: ct.GENE})

    # merge the info and retrieve per row the incluster condition
    mutations_df = mutations_df.merge(clusters_df, how='left', on=ct.GENE)
    mutations_df[ct.IS_IN_CLUSTER] = mutations_df.apply(lambda row: check_in_cluster(row[ct.AA_POS], row['cluster']),
                                                        axis=1)

    # drop tmp columns
    mutations_df = mutations_df.drop(['cluster'], 1)

    return mutations_df


def insert_mut_is_in_delicate_domain(mutations_df, run_info_d):
    def check_in_delicate_domain(aa_pos, start, end):
        try:
            if int(start) <= int(aa_pos) <= int(end):
                return ct.IN_DELICATE_DOMAIN
            return ''
        except Exception:
            return ''

    logging.debug('Checking mutations in delicate domains..')

    # read the delicate domains file
    delicate_domains_df = pd.read_csv(run_info_d['delicate_domains_fp'], sep='\t')
    delicate_domains_df = delicate_domains_df.rename(columns={delicate_domains_df.columns[0]: ct.GENE})

    # merge the info and retrieve per row the in delicate domain condition
    mutations_df = mutations_df.merge(delicate_domains_df[[ct.GENE, 'REGION_START', 'REGION_END']], how='left',
                                      on=ct.GENE)
    mutations_df[ct.IS_IN_DELICATE_DOMAIN] = mutations_df.apply(
        lambda row: check_in_delicate_domain(row[ct.AA_POS], row['REGION_START'], row['REGION_END']), axis=1
    )

    # drop tmp columns
    mutations_df = mutations_df.drop(['REGION_START', 'REGION_END'], 1)

    return mutations_df


def insert_protein_portion_affected(mutations_df):
    def get_protein_affected(aa_pos, exon, transcript_exons, transcript_aminoacids):

        try:
            exon, aa_pos, transcript_exons, transcript_aminoacids = int(exon), int(aa_pos), int(transcript_exons), int(
                transcript_aminoacids)
        except Exception:
            return '-'

        if exon < transcript_exons:
            return ct.BEFORE_LAST_EXON

        if ((transcript_aminoacids - aa_pos) / transcript_aminoacids) >= ct.PROTEIN_TIP:
            return ct.BEFORE_LAST_PORTION

        # warnings to remove?
        if exon > transcript_exons:
            logging.warning('There is a exon stated as {0}st in a transcript stated as having {1} exons'
                            .format(exon, transcript_exons)
                            )
        if aa_pos > transcript_aminoacids:
            logging.warning('There is a AA mut position {0} in a transcript stated as having {1} AAs'
                            .format(aa_pos, transcript_aminoacids)
                            )

        return ct.LAST_PORTION

    logging.debug('Checking protein portion affected..')
    mutations_df[ct.PROTEIN_AFFECTED] = mutations_df.apply(
        lambda row: get_protein_affected(row[ct.AA_POS], row[ct.EXON], row[ct.TRANSCRIPT_EXONS],
                                         row[ct.TRANSCRIPT_AMINOACIDS]), axis=1)

    return mutations_df


def run(config):
    logging.info('Running the driver prediction')

    # retrive the paths of the outputed files
    out_fp = os.path.join(config['tmp_folder'], ct.DRIVER_MUTS)
    config['driver_prediction_fp'] = out_fp

    # assess if i need to run this stage by checking whether the *final* outputed file already exists
    if not config['force_output'] and os.path.isfile(out_fp):
        logging.debug('Stage skipped: file {0} already exists'.format(out_fp))
        return config

    # note that the input file to analyse already have the fiscore scores
    mutations_df = pd.read_csv(config['metadata_output_fp'], sep='\t')

    # insert whether the gene is a driver of the tumor type under analysis in ct.GENE_DRIVER column
    mutations_df, config = insert_gene_driver_category_and_source(mutations_df, config)

    # insert role in ct.ROLE column
    mutations_df = insert_gene_role(mutations_df, config)

    # insert in_cluster in ct.IN_CLUSTER column
    mutations_df = insert_mut_is_in_cluster(mutations_df, config)

    # delicate domain
    mutations_df = insert_mut_is_in_delicate_domain(mutations_df, config)

    # proportion of protein affected
    mutations_df = insert_protein_portion_affected(mutations_df)

    # do the rules
    mutations_df = dr.do_driver_rules(mutations_df)

    # output
    mutations_df.to_csv(config['driver_prediction_fp'], sep='\t', index=False)
    logging.info('File created with {0} entries: {1}'.format(len(mutations_df),
                                                             os.path.basename(config['driver_prediction_fp'])))

    return config
