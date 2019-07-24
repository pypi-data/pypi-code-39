# from abc import ABCMeta
# import json
# import pandas as pd
import os
import datetime
import boto3
import subprocess
import shlex
import collections

from Bio import AlignIO

from metagenomi.db import (S3resource, S3)
from metagenomi.helpers import download_file, upload_file

from metagenomi.helpers import check_s3file, most_frequent, get_lca, get_taxonomy
DTSTR = datetime.datetime.now().strftime("%Y_%m_%d_%s")


def write_old_filepath(old, new):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('old-filepaths-map')

    d = {'olds3path': old, 'news3path': new}
    response = table.put_item(Item=d)
    return response


# def update_old_filepaths_table():
#     dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
#     table = dynamodb.Table('old-filepaths-map')
#
#     response = table.update_item(
#                         Key={
#                             'mgid':
#                         },
#                         UpdateExpression=f"set {key} = :r",
#                         ExpressionAttributeValues={
#                             ':r': value
#                         },
#                         ReturnValues="UPDATED_NEW"
#                     )

def remove_s3file(s3file):
    bucket = s3file.split('/')[2]
    key = '/'.join(s3file.split('/')[3:])
    if check_s3file(s3file):
        S3resource.Object(bucket, key).delete()
        return True
    else:
        print(f'{s3file} does not exist')
        return False


def check_object(a, wd, dryrun=False):
    '''
    Given an Assembly() object, check if the paths are correct
    '''
    print(f'Working on {a.mgid}')
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

    # DOWNLOADS
    fa = download_file(s3fa, wd, overwrite=False)
    min1000 = download_file(s3min1000, wd, overwrite=False)
    faa = download_file(s3faa, wd, overwrite=False)
    genes = download_file(s3genes, wd, overwrite=False)

    if check_file(fa) is False:
        rn = rename(fa, a.mgid, f'{a.mgid}_contig')
        if dryrun:
            print(f'\tRenamed {fa}')
        else:
            print(f'\tRenamed & uploaded{fa}')
            upload_file(rn, s3fa+'.gz', compress=True)
            if not s3fa.endswith('.gz'):
                print(f'\tRemoving original {s3fa}')
                remove_s3file(s3fa)
            os.remove(rn+'.gz')
    else:
        print(f'\tPASS {fa}')

    if check_file(min1000) is False:
        rn = rename(min1000, a.mgid, f'{a.mgid}_contig')
        if dryrun:
            print(f'\tRenamed {min1000}')
        else:
            print(f'\tRenamed & uploaded {min1000}')
            # remove_s3file(s3min1000)
            upload_file(rn, s3min1000+'.gz', compress=True)
            if not s3min1000.endswith('.gz'):
                print(f'\tRemoving original {s3min1000}')
                remove_s3file(s3min1000)
            os.remove(rn+'.gz')
    else:
        print(f'\tPASS {min1000}')

    if check_file(faa) is False:
        rn = rename(faa, a.mgid, f'{a.mgid}_contig')
        if dryrun:
            print(f'\tRenamed {faa}')
        else:
            print(f'\tRenamed & uploaded {faa}')
            upload_file(rn, s3faa+'.gz', compress=True)
            if not s3faa.endswith('.gz'):
                print(f'\tRemoving original {s3faa}')
                remove_s3file(s3faa)
            os.remove(rn+'.gz')
    else:
        print(f'\tPASS {faa}')

    if check_file(genes) is False:
        rn = rename(genes, a.mgid, f'{a.mgid}_contig')
        if dryrun:
            print(f'\tRenamed {genes}')
        else:
            print(f'\tRenamed & uploaded {genes}')
            upload_file(rn, s3genes)
            os.remove(rn)
    else:
        print(f'\tPASS {genes}')

    os.remove(fa)
    os.remove(genes)
    os.remove(faa)
    os.remove(min1000)

    return True


def check_file(file):
    with open(file) as f:
        first_line = f.readline()
        if '_contig_' in first_line:
            return False
    return True


def rename(file, mgid, basename):
    outfile = file+'.renamed'
    if file.endswith('.bam'):
        pass
    else:
        cmd = f"sed 's/{basename}/{mgid}/' {file}"

        with open(outfile, 'w') as f:
            subprocess.check_call(shlex.split(cmd), stdout=f)

    return outfile


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


def get_kaiju_cmds(mgids, outfile='kaiju.sh', n=2000, wd='/Users/audra/work/mginfra/mg-kaiju'):
    mgid_sets = [mgids[i * n:(i + 1) * n] for i in range((len(mgids) + n - 1) // n )]

    count = 1
    with open(f'{wd}/{outfile}', 'w') as f:
        for i in mgid_sets:
            mgidfile = f'{wd}/set{len(i)}_{count}.txt'
            with open(mgidfile, 'w') as mgids:
                for mgid in i:
                    mgids.write(mgid+'\n')
            count += 1

            cmd = f'python submit_kaiju_job.py --mgid {mgidfile} '
            cmd += '--kaijudb s3://metagenomi/biodb/kaiju/kaiju_db_nr_11042018.fmi '
            cmd += '--taxnodes s3://metagenomi/biodb/kaiju/nodes_11042018.dmp '
            cmd += '--taxnames s3://metagenomi/biodb/kaiju/names_11042018.dmp'
            f.write(cmd+'\n')


def compare_lca_winner(d):

    for k, v in d.items():
        lca = get_lca(v)
        winner = most_frequent(v)
        if lca != winner:
            print(get_taxonomy(lca))
            print(get_taxonomy(winner))

            print(k)


def avg_perc_identity(aln):
    avgs = []
    for a in range(0, len(aln[0])):
        s = aln[:, a]
        consensus = collections.Counter(s).most_common(1)[0]
        perc_consensus = consensus[1]/len(s)
        avgs.append(perc_consensus)
    return sum(avgs)/len(avgs)


def perc_identity(alnfile):
    aln = AlignIO.read(alnfile, "fasta")
    i = 0
    for a in range(0, len(aln[0])):
        s = aln[:, a]
        if s == len(s) * s[0]:
            i += 1
    return 100*i/float(len(aln[0]))
