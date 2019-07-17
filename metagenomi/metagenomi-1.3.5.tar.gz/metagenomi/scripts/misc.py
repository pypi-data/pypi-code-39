# from abc import ABCMeta
# import json
# import pandas as pd
import boto3

# from boto3.dynamodb.conditions import Key

# from metagenomi.base import MgObj
# from metagenomi.logger import logger
# from metagenomi.helpers import get_time
from metagenomi.helpers import check_s3file
# from metagenomi.db import batch_client


def write_old_filepath(old, new):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('old-filepaths-map')

    d = {'olds3path': old, 'news3path': new}
    response = table.put_item(Item=d)
    return response


def check_object(a):
    '''
    Given an Assembly() object, check if the paths are correct
    '''
    s3fa = f's3://mg-assembly/{a.mgproject}/{a.mgid}/{a.mgid}.fa'
    s3min1000 = f's3://mg-assembly/{a.mgproject}/{a.mgid}/{a.mgid}_min1000.fa'
    s3faa = f's3://mg-features/{a.mgproject}/{a.mgid}/{a.mgid}_min1000.fa.genes.faa'
    s3genes = f's3://mg-features/{a.mgproject}/{a.mgid}/{a.mgid}_min1000.fa.genes'
    if a.s3path != s3fa:
        # print('Contigs are fucked')
        return False
    if a.prodigal.pullseq_contigs != s3min1000:
        # print('Min1000 is fucked')
        return False
    if a.prodigal.protein_file != s3faa:
        # print('Proteins is fucked')
        return False
    if not check_s3file(s3genes):
        # print('Genes are fucked')
        return False
    return True


def update_faa(p):
    '''
    p = MgProject()
    '''
    bad = []
    for a in p.assemblies:
        s3faa = f's3://mg-features/{a.mgproject}/{a.mgid}/{a.mgid}_min1000.fa.genes.faa'
        if a.prodigal.protein_file != s3faa:
            try:
                a.prodigal.protein_file = s3faa
                a.prodigal.write()
                write_old_filepath(a.prodigal.protein_file, s3faa)
            except ValueError:
                bad.append(a)
    return bad


def get_kaiju(p, outfile):
    with open(outfile, 'w') as f:
        for a in p.assemblies:
            cmd = f'python submit_kaiju_job.py --mgid {a.mgid} '
            cmd += '--kaijudb s3://metagenomi/biodb/kaiju/kaiju_db_nr_11042018.fmi '
            cmd += '--taxnodes s3://metagenomi/biodb/kaiju/nodes_11042018.dmp '
            cmd += '--taxnames s3://metagenomi/biodb/kaiju/names_11042018.dmp '
            cmd += '--contigs\n'
            f.write(cmd)

    return outfile
