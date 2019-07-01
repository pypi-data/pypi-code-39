# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.gis.db.models.fields import GeometryField


class EsciFinal(models.Model):
    ogc_fid = models.AutoField(primary_key=True)
    cartodb_id = models.IntegerField(blank=True, null=True)
    ecsi_ge_32 = models.IntegerField(blank=True, null=True)
    ecsi_ge_24 = models.IntegerField(blank=True, null=True)
    ecsi_ge_22 = models.IntegerField(blank=True, null=True)
    ecsi_ge_20 = models.IntegerField(blank=True, null=True)
    ecsi_ge_18 = models.IntegerField(blank=True, null=True)
    ecsi_ge_15 = models.IntegerField(blank=True, null=True)
    ecsi_ge_14 = models.IntegerField(blank=True, null=True)
    ecsi_ge_11 = models.IntegerField(blank=True, null=True)
    ecsi_ge_10 = models.IntegerField(blank=True, null=True)
    ecsi_geo_8 = models.IntegerField(blank=True, null=True)
    ecsi_geo_7 = models.IntegerField(blank=True, null=True)
    ecsi_geo_6 = models.IntegerField(blank=True, null=True)
    ecsi_geo_4 = models.IntegerField(blank=True, null=True)
    ecsi_geo_2 = models.IntegerField(blank=True, null=True)
    ecsi_geoco = models.IntegerField(blank=True, null=True)
    substance1 = models.TextField(blank=True, null=True)
    site_inv_1 = models.TextField(blank=True, null=True)
    medium_f_1 = models.TextField(blank=True, null=True)
    ecsi_ge_31 = models.TextField(blank=True, null=True)
    ecsi_ge_30 = models.TextField(blank=True, null=True)
    ecsi_ge_27 = models.TextField(blank=True, null=True)
    ecsi_ge_23 = models.TextField(blank=True, null=True)
    ecsi_ge_21 = models.TextField(blank=True, null=True)
    ecsi_ge_19 = models.TextField(blank=True, null=True)
    ecsi_ge_17 = models.TextField(blank=True, null=True)
    ecsi_geo_1 = models.TextField(blank=True, null=True)
    ecsi_ge_16 = models.FloatField(blank=True, null=True)
    ecsi_ge_13 = models.FloatField(blank=True, null=True)
    ecsi_ge_12 = models.FloatField(blank=True, null=True)
    ecsi_geo_9 = models.FloatField(blank=True, null=True)
    click_for_more_information = models.TextField(blank=True, null=True)
    wkb_geometry = GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'esci_final'


class LustNotOilClip(models.Model):
    ogc_fid = models.AutoField(primary_key=True)
    cartodb_id = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    objectid_1 = models.IntegerField(blank=True, null=True)
    objectid = models.IntegerField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    region = models.TextField(blank=True, null=True)
    site_city = models.TextField(blank=True, null=True)
    site_addre = models.TextField(blank=True, null=True)
    site_name = models.TextField(blank=True, null=True)
    log_number = models.TextField(blank=True, null=True)
    arc_zip = models.TextField(blank=True, null=True)
    arc_state = models.TextField(blank=True, null=True)
    arc_city = models.TextField(blank=True, null=True)
    arc_street = models.TextField(blank=True, null=True)
    user_fld = models.TextField(blank=True, null=True)
    comp_score = models.TextField(blank=True, null=True)
    addr_type = models.TextField(blank=True, null=True)
    street_id = models.TextField(blank=True, null=True)
    side = models.TextField(blank=True, null=True)
    match_addr = models.TextField(blank=True, null=True)
    match_type = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    loc_name = models.TextField(blank=True, null=True)
    zipcode = models.IntegerField(blank=True, null=True)
    site_zipco = models.IntegerField(blank=True, null=True)
    match_time = models.FloatField(blank=True, null=True)
    disp_lat = models.FloatField(blank=True, null=True)
    disp_lon = models.FloatField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    work_compl = models.DateTimeField(blank=True, null=True)
    cleanup_st = models.DateTimeField(blank=True, null=True)
    cleanup_re = models.DateTimeField(blank=True, null=True)
    wkb_geometry = GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lust_not_oil_clip'


class PortlandMsaNcdb(models.Model):
    ogc_fid = models.AutoField(primary_key=True)
    statefp10 = models.TextField(blank=True, null=True)
    countyfp10 = models.TextField(blank=True, null=True)
    tractce10 = models.TextField(blank=True, null=True)
    geoid10 = models.TextField(blank=True, null=True)
    name10 = models.TextField(blank=True, null=True)
    namelsad10 = models.TextField(blank=True, null=True)
    mtfcc10 = models.TextField(blank=True, null=True)
    funcstat10 = models.TextField(blank=True, null=True)
    aland10 = models.IntegerField(blank=True, null=True)
    awater10 = models.IntegerField(blank=True, null=True)
    intptlat10 = models.TextField(blank=True, null=True)
    intptlon10 = models.TextField(blank=True, null=True)
    ncdb_pdx_msa_tractpopulation2010 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_medinc_90 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_medinc_00 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_medinc_10 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_medinc_17 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_medhomeval_90 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_medhomeval_00 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_medhomeval_10 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_medhomeval_17 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_medrentval_90 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_medrentval_00 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_medrentval_10 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_medrentval_17 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_ownshare_90 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_ownshare_00 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_ownshare_10 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_ownshare_17 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_whiteshare_90 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_whiteshare_00 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_whiteshare_10 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_whiteshare_17 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_blackshare_90 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_blackshare_00 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_blackshare_10 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_blackshare_17 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_hispshare_90 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_hispshare_00 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_hispshare_10 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_hispshare_17 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_asothshare_90 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_asothshare_00 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_asothshare_10 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_asothshare_17 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_rentcbshare_90 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_rentcbshare_00 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_rentcbshare_10 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_rentcbshare_17 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_povrate_90 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_povrate_00 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_povrate_10 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_povrate_17 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_bachshare_90 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_bachshare_00 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_bachshare_10 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_bachshare_17 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chrent_9017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chrent_0017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chrent_1017 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_chinc_9017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chinc_0017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chinc_1017 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_chhomeval_9017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chhomeval_0017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chhomeval_1017 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_chbachshare_9017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chbachshare_0017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chbachshare_1017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chwhiteshare_9017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chwhiteshare_0017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chwhiteshare_1017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chblackshare_9017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chblackshare_0017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chblackshare_1017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chhispshare_9017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chhispshare_0017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chhispshare_1017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chasothshare_9017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chasothshare_0017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chasothshare_1017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chownshare_9017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chownshare_0017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chownshare_1017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chpovrate_9017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chpovrate_0017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chpovrate_1017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chrentcbshare_9017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chrentcbshare_0017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_chrentcbshare_1017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metmedinc_90 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_metmedinc_00 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_metmedinc_10 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_metmedinc_17 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_metmedhomeval_90 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_metmedhomeval_00 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_metmedhomeval_10 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_metmedhomeval_17 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_metmedrentval_90 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metmedrentval_00 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_metmedrentval_10 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_metmedrentval_17 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_metownshare_90 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metownshare_00 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metownshare_10 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metownshare_17 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metwhiteshare_90 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metwhiteshare_00 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metwhiteshare_10 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metwhiteshare_17 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metblackshare_90 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metblackshare_00 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metblackshare_10 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metblackshare_17 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_methispshare_90 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_methispshare_00 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_methispshare_10 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_methispshare_17 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metasothshare_90 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metasothshare_00 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metasothshare_10 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metasothshare_17 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metrentcbshare_90 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metrentcbshare_00 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metrentcbshare_10 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metrentcbshare_17 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metpovrate_90 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metpovrate_00 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metpovrate_10 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metpovrate_17 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metbachshare_90 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metbachshare_00 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metbachshare_10 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metbachshare_17 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchinc_9017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchinc_9000 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchinc_0010 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchinc_0017 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_metchinc_1017 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_metchinc_9016 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchbachshare_9017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchbachshare_9000 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchbachshare_0010 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchbachshare_0017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchbachshare_1017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchrent_9017 = models.FloatField(db_column='ncdb_pdx_msa_metchrent__9017', blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    ncdb_pdx_msa_metchrent_9000 = models.FloatField(db_column='ncdb_pdx_msa_metchrent__9000', blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    ncdb_pdx_msa_metchrent_0010 = models.FloatField(db_column='ncdb_pdx_msa_metchrent__0010', blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    ncdb_pdx_msa_metchrent_0017 = models.FloatField(db_column='ncdb_pdx_msa_metchrent__0017', blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    ncdb_pdx_msa_metchrent_1017 = models.IntegerField(db_column='ncdb_pdx_msa_metchrent__1017', blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    ncdb_pdx_msa_metchrent_9016 = models.FloatField(db_column='ncdb_pdx_msa_metchrent__9016', blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    ncdb_pdx_msa_metchhomeval_9017 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_metchhomeval_9000 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchhomeval_0010 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchhomeval_0017 = models.IntegerField(blank=True, null=True)
    ncdb_pdx_msa_metchhomeval_1017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchhomeval_9016 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchpovrate_9017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchpovrate_9000 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchpovrate_0010 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchpovrate_0017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchpovrate_1017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchownshare_9017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchownshare_9000 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchownshare_0010 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchownshare_0017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchownshare_1017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchrentcbshare_9017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchrentcbshare_9000 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchrentcbshare_0010 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchrentcbshare_0017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchrentcbshare_1017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchwhiteshare_9017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchwhiteshare_9000 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchwhiteshare_0010 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchwhiteshare_0017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchwhiteshare_1017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchblackshare_9017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchblackshare_9000 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchblackshare_0010 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchblackshare_0017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchblackshare_1017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchhispshare_9017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchhispshare_9000 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchhispshare_0010 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchhispshare_0017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchhispshare_1017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchasothshare_9017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchasothshare_9000 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchasothshare_0010 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchasothshare_0017 = models.FloatField(blank=True, null=True)
    ncdb_pdx_msa_metchasothshare_1017 = models.FloatField(blank=True, null=True)
    wkb_geometry = GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'portland_msa_ncdb'


class Superfund(models.Model):
    ogc_fid = models.AutoField(primary_key=True)
    cartodb_id = models.IntegerField(blank=True, null=True)
    accuracy_v = models.IntegerField(blank=True, null=True)
    active_sta = models.TextField(blank=True, null=True)
    program_ur = models.TextField(blank=True, null=True)
    interest_t = models.TextField(blank=True, null=True)
    pgm_sys_ac = models.TextField(blank=True, null=True)
    pgm_sys_id = models.TextField(blank=True, null=True)
    fac_url = models.TextField(blank=True, null=True)
    ref_point_field = models.TextField(db_column='ref_point_', blank=True, null=True)  # Field renamed because it ended with '_'.
    collect_mt = models.TextField(blank=True, null=True)
    huc8_code = models.TextField(blank=True, null=True)
    postal_cod = models.TextField(blank=True, null=True)
    state_code = models.TextField(blank=True, null=True)
    fips_code = models.TextField(blank=True, null=True)
    county_nam = models.TextField(blank=True, null=True)
    city_name = models.TextField(blank=True, null=True)
    location_a = models.TextField(blank=True, null=True)
    primary_na = models.TextField(blank=True, null=True)
    registry_i = models.TextField(blank=True, null=True)
    longitude8 = models.FloatField(blank=True, null=True)
    latitude83 = models.FloatField(blank=True, null=True)
    update_dat = models.DateTimeField(blank=True, null=True)
    create_dat = models.DateTimeField(blank=True, null=True)
    click_for_more_info = models.TextField(blank=True, null=True)
    wkb_geometry = GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'superfund'
