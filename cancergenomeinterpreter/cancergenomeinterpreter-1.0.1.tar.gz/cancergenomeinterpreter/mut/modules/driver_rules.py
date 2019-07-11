import numpy as np

import cancergenomeinterpreter.mut.utils.constants as ct


def get_cond_missense(cond_t1_mis1, cond_t1_mis2, cond_t1_mis3, cond_t2_mis1, cond_t2_mis2, cond_miss):
    cond_missense_l = []
    for c11, c12, c13, c21, c22, cmiss in zip(cond_t1_mis1, cond_t1_mis2, cond_t1_mis3, cond_t2_mis1, cond_t2_mis2,
                                              cond_miss):
        cond = []
        if not cmiss:
            cond_missense_l.append('')
            continue
        if c13:
            cond += ['MISSENSE_in_CLUSTER_in_any_role_gene']
        if c11 or c12:
            cond += ['MISSENSE_with_stringent_FI_in_any_role_gene']
        elif c21:
            cond += ['MISSENSE_with_loose_FI_in_any_role_gene']
        if c22:
            cond += ['MISSENSE_with_DELICATE_domain_FI_in_any_role_gene']
        cond_missense_l.append(','.join(cond))

    return cond_missense_l


def get_cond_disrupting(cond_t1_trunc1, cond_t2_trunc1, cond_t2_trunc2, cond_disr):
    cond_disrupting_l = []
    for c11, c21, c22, cdisr in zip(cond_t1_trunc1, cond_t2_trunc1, cond_t2_trunc2, cond_disr):
        cond = []
        if not cdisr:
            cond_disrupting_l.append('')
            continue
        if c11:
            cond += ['DISRUPTING_not_distal_in_LoF_role_gene']
        elif c21:
            cond += ['DISRUPTING_not_distal_in_Ambigous_role_gene']
        if c22:
            cond += ['DISRUPTING_in_CLUSTER_in_ACT_role_gene']
        cond_disrupting_l.append(','.join(cond))

    return cond_disrupting_l


def get_cond_inframe(cond_t2_chang1, cond_t2_chang2, cond_t2_chang3, cond_chang):
    cond_inframe_l = []
    for c21, c22, c23, cch in zip(cond_t2_chang1, cond_t2_chang2, cond_t2_chang3, cond_chang):
        cond = []
        if not cch:
            cond_inframe_l.append('')
            continue
        if c21:
            cond += ['INFRAME_with_loose_FI_in_LoF/Ambigous_role_gene']
        if c22:
            cond += ['INFRAME_with_loose_FI_in_Delicate_Domain_in_LoF/Ambigous_role_gene']
        if c23:
            cond += ['INFRAME_in_CLUSTER_in_any_role_gene']
        cond_inframe_l.append(','.join(cond))

    return cond_inframe_l


############################################################################################
############################################################################################


def do_driver_rules(df):
    ########################################################################################
    # conditions related with the consequence type
    cond_miss_ct = df[ct.CONSEQUENCE_TYPE].isin(ct.MISSENSE_CT)
    cond_disr_ct = df[ct.CONSEQUENCE_TYPE].isin(ct.DISRUPTING_CT)
    cond_infr_ct = df[ct.CONSEQUENCE_TYPE].isin(ct.INFRAME_CT)
    cond_not_considered_ct = np.invert(df[ct.CONSEQUENCE_TYPE].isin(ct.MISSENSE_CT + ct.DISRUPTING_CT + ct.INFRAME_CT))

    # condition that the fiscore is not available for some reason, unless it s a fs
    # (it can have no fiscore because the rev mapping to dna is not available)
    cond_fiscore_not_available = (df[ct.FISCORE_SCORE].isnull()) & (np.invert(df[ct.CONSEQUENCE_TYPE].isin(ct.FRAMESHIFT_CT)))

    ########################################################################################
    # TIER 1 conditions

    # -> MISSENSE

    cond_t1_mis_1 = (df[ct.DRIVER_GENE].isin([ct.TUMOR_DRIVER])) & (df[ct.FISCORE_SCORE] >= ct.FISCORE_LOOSE_TH)
    cond_t1_mis_2 = (df[ct.DRIVER_GENE].isin([ct.OTHER_TUMOR_DRIVER])) & (df[ct.FISCORE_SCORE] >= ct.FISCORE_DEMANDING_TH)
    cond_t1_mis_3 = (df[ct.DRIVER_GENE].isin([ct.TUMOR_DRIVER, ct.OTHER_TUMOR_DRIVER])) & \
                    (df[ct.IS_IN_CLUSTER].isin([ct.IN_CLUSTER]))

    cond_t1_mis = cond_miss_ct & (cond_t1_mis_1 | cond_t1_mis_2 | cond_t1_mis_3)

    # -> DISRUPTING

    cond_t1_trunc_1 = (df[ct.DRIVER_GENE].isin([ct.TUMOR_DRIVER, ct.OTHER_TUMOR_DRIVER])) & (
        df[ct.GENE_ROLE].isin([ct.LOF])) & (np.invert(df[ct.PROTEIN_AFFECTED].isin([ct.LAST_PORTION])))

    cond_t1_trunc = cond_disr_ct & cond_t1_trunc_1

    # (no tier_1 chances for inframe indels)

    ########################################################################################
    # TIER 2 conditions

    # -> MISSENSE

    cond_t2_mis_1 = (df[ct.DRIVER_GENE].isin([ct.TUMOR_DRIVER, ct.OTHER_TUMOR_DRIVER])) & (
            df[ct.FISCORE_SCORE] >= ct.FISCORE_LOOSE_TH)
    cond_t2_mis_2 = (df[ct.DRIVER_GENE].isin([ct.TUMOR_DRIVER, ct.OTHER_TUMOR_DRIVER])) & \
                    (df[ct.IS_IN_DELICATE_DOMAIN].isin([ct.IN_DELICATE_DOMAIN])) & (
                            df[ct.FISCORE_SCORE] >= (ct.FISCORE_LOOSE_TH - 5))

    cond_t2_mis = cond_miss_ct & (cond_t2_mis_1 | cond_t2_mis_2)

    # -> DISRUPTING

    cond_t2_trunc_1 = (df[ct.DRIVER_GENE].isin([ct.TUMOR_DRIVER, ct.OTHER_TUMOR_DRIVER])) & (
        df[ct.GENE_ROLE].isin([ct.AMBIGUOUS])) & (np.invert(df[ct.PROTEIN_AFFECTED].isin([ct.LAST_PORTION])))
    cond_t2_trunc_2 = (df[ct.DRIVER_GENE].isin([ct.TUMOR_DRIVER, ct.OTHER_TUMOR_DRIVER])) & \
                      (df[ct.IS_IN_CLUSTER].isin([ct.IN_CLUSTER]))

    cond_t2_trunc = cond_disr_ct & (cond_t2_trunc_1 | cond_t2_trunc_2)

    # -> INFRAME

    cond_t2_infr_1 = (df[ct.DRIVER_GENE].isin([ct.TUMOR_DRIVER, ct.OTHER_TUMOR_DRIVER])) & \
                     (df[ct.GENE_ROLE].isin([ct.LOF, ct.AMBIGUOUS])) & (df[ct.FISCORE_SCORE] >= ct.FISCORE_LOOSE_TH)
    cond_t2_infr_2 = (df[ct.DRIVER_GENE].isin([ct.TUMOR_DRIVER, ct.OTHER_TUMOR_DRIVER])) & \
                     (df[ct.GENE_ROLE].isin([ct.LOF, ct.AMBIGUOUS])) & (
                         df[ct.IS_IN_DELICATE_DOMAIN].isin([ct.IN_DELICATE_DOMAIN])) & \
                     (df[ct.FISCORE_SCORE] >= (ct.FISCORE_LOOSE_TH - 5))
    cond_t2_infr_3 = (df[ct.DRIVER_GENE].isin([ct.TUMOR_DRIVER, ct.OTHER_TUMOR_DRIVER])) & (
        df[ct.IS_IN_CLUSTER].isin([ct.IN_CLUSTER]))

    cond_t2_infr = cond_infr_ct & (cond_t2_infr_1 | cond_t2_infr_2 | cond_t2_infr_3)

    ########################################################################################
    # combine conditions for the final decision TIER1/2 and PASSENGER

    not_considered_mutation = cond_not_considered_ct

    tier1 = (cond_t1_mis | cond_t1_trunc) & (np.invert(not_considered_mutation))

    tier2 = (np.invert(tier1)) & (cond_t2_mis | cond_t2_trunc | cond_t2_infr) & (np.invert(not_considered_mutation))

    fiscore_not_available = cond_fiscore_not_available & (
        np.invert(not_considered_mutation | tier1 | tier2))  # if already predicted, do not state fiscore N/A

    considered_but_not_driver = np.invert(not_considered_mutation | tier1 | tier2 | fiscore_not_available)

    final_condlist = [tier1, tier2, considered_but_not_driver, fiscore_not_available, not_considered_mutation]
    final_choicelist = [ct.TIER_1, ct.TIER_2, ct.PASSENGER, ct.FISCORE_NA, ct.CT_NOT_CONSIDERED]

    cond_driver_prediction = np.select(final_condlist, final_choicelist)

    ########################################################################################
    # insert the resulting columns in the dataframe to return

    # construct the informative condition columns
    df[ct.MISSENSE_PREDICTION] = get_cond_missense(cond_t1_mis_1, cond_t1_mis_2, cond_t1_mis_3, cond_t2_mis_1,
                                                   cond_t2_mis_2, cond_miss_ct)
    df[ct.DISRUPTING_PREDICTION] = get_cond_disrupting(cond_t1_trunc_1, cond_t2_trunc_1, cond_t2_trunc_2, cond_disr_ct)
    df[ct.INFRAME_PREDICTION] = get_cond_inframe(cond_t2_infr_1, cond_t2_infr_2, cond_t2_infr_3, cond_infr_ct)

    df[ct.DRIVER_MUT_PREDICTION] = cond_driver_prediction

    return df
