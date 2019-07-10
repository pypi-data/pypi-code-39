#!/usr/bin/env python
"""
usage:  bcl2fq-local -i <seq_dir> -o <ou_dir>

optional arguments:
    --sample-sheet Path  Using custom sample sheet file
    --mismatch N         Mismatch for barcode, default: 1
    --process N          Process number for demultiplexing and processing
    --io-process N       Process number for reading and writing
    --binpath   Path     Bcl2fastq binary file path
    --dry-run            Only print the cmd without running it
    --mask String        Use self defined mask, instead of
    --mask-reads         Mask last few base of reads, default is: 0,0
    --mask-index         Mask last few base of index, default is: 0,0
    --version            Show  version info
"""
import xmltodict
import subprocess
import argparse
import os
import sys
import time
import shutil
# import json

VERSION = '0.1.5'

settings = {}


def parse_params(xml_file):
    if not os.path.exists(xml_file):
        print(f'{xml_file} not found!')
        return {}
    with open(xml_file) as f:
        contents = f.read()
    try:
        params = xmltodict.parse(contents)
    except Exception as e:
        print(e)
    else:
        return params


def gen_conf():
    params_info_file = os.path.join(settings['seq_dir'], 'RunInfo.xml')
    params = parse_params(params_info_file)
    if not settings['mask']:
        settings['mask'] = gen_mask(params.get('RunInfo', {}).get('Run', {}).get('Reads', {}).get('Read', []))


def gen_mask(reads):
    mask = []
    for item in reads:
        if item['@IsIndexedRead'] == 'N':
            length = int(item["@NumCycles"])
            m = int(settings['mask_reads'][0])
            settings['mask_reads'] = settings['mask_reads'][1:]
            if m == 0:
                mask.append('y*')
            elif m == 1:
                mask.append('y*n')
            else:
                mask.append('y{}n{}'.format(length-m, m))
        elif item['@IsIndexedRead'] == 'Y':
                length = int(item["@NumCycles"])
                m = int(settings['mask_indexs'][0])
                settings['mask_indexs'] = settings['mask_indexs'][1:]
                if m == 0:
                    mask.append('i*')
                elif m == 1:
                    mask.append('i*n')
                else:
                    mask.append('i{}n{}'.format(length - m, m))
        else:
            continue
    return ','.join(mask)


def gen_commmand():
    template = '{bin} -r {read_process_num} -p {parse_process_num} -w {write_process_num} ' + \
        '--barcode-mismatches {mismatch} --no-lane-splitting -R {seq_dir} --output-dir {out_dir} ' + \
        '--use-bases-mask {mask} --sample-sheet {sample_sheet_path}'

    return template.format(read_process_num=settings['ioprocess'],
                           parse_process_num=settings['process'],
                           write_process_num=settings['ioprocess'],
                           mismatch=settings['mismatch'],
                           seq_dir=settings['seq_dir'],
                           out_dir=settings['out_dir'],
                           mask=settings['mask'],
                           sample_sheet_path=settings['sample_sheet'],
                           bin=settings['binpath']
                           )


def wait_sequence_finish():
    while not os.path.exists(os.path.join(settings['seq_dir'], 'RTAComplete.txt')):
        print('Sequence not finished! Wait for finishing...')
        time.sleep(60)


def check_sample_sheet_existence():
    if not os.path.exists(settings['sample_sheet']):
        sys.exit('{path} not found!'.format(path=settings['sample_sheet']))


def move_undetermined_files():
    dest_dir = os.path.join(settings['out_dir'], 'UndeterminedReads')
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)
    shutil.move(os.path.join(settings['out_dir'], 'Undetermined_S0_R1_001.fastq.gz'), dest_dir)
    shutil.move(os.path.join(settings['out_dir'], 'Undetermined_S0_R2_001.fastq.gz'), dest_dir)


def run_bcl2fq(cmd):
    check_sample_sheet_existence()
    wait_sequence_finish()
    res = subprocess.Popen(cmd,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           encoding='utf-8',
                           shell=True)
    while True:
        output = res.stdout.readline()
        if res.poll() is not None:
            break
        if output:
            print(output.strip())
    return_code = res.poll()
    return return_code


def parse_args():
    usage = ''' bcl2fq-local -i <seq_dir> -o <ou_dir>
    
optional arguments:
    --sample-sheet Path  Using custom sample sheet file
    --mismatch N         Mismatch for barcode, default: 1
    --process N          Process number for demultiplexing and processing
    --io-process N       Process number for reading and writing
    --binpath   Path     Bcl2fastq binary file path
    --dry-run            Only print the cmd without running it
    --mask String        Use self defined mask, instead of 
    --mask-reads         Mask last few base of reads, default is: 0,0
    --mask-index         Mask last few base of index, default is: 0,0
    --version            Show  version info
    '''
    parser = argparse.ArgumentParser(usage=usage, add_help=False)
    parser.add_argument('-i', metavar='DirPath', help='Sequence run dir')
    parser.add_argument('-o', metavar='DirPath', help='Output dir for fastq files')
    parser.add_argument('--sample-sheet', dest='sample_sheet', metavar='File', help='Using custom sample sheet file')
    parser.add_argument('--mismatch', metavar='Num', type=int, default=1, help='Mismatch for barcode, default: 1')
    parser.add_argument('--process', metavar='Num', type=int, default=24,
                        help='Process number for demultiplexing and processing')
    parser.add_argument('--io-process', metavar='Num', type=int, dest='ioprocess', default=4,
                        help='Process number for reading and writing')
    parser.add_argument('--binpath', metavar='File', help='bcl2fastq binary file path')
    parser.add_argument('--dry-run', dest='dry_run', action='store_true', default=False,
                        help='Only print the cmd without running it')
    parser.add_argument('--mask', dest='mask', help='using self defined mask')
    parser.add_argument('--mask-reads', dest='mask_reads', help='set reads mask base count, default is: 0,0',
                        default='0,0')
    parser.add_argument('--mask-index', dest='mask_index', help='set index mask base count, default is: 0,0',
                        default='0,0')
    parser.add_argument('--version', action='store_true', default=False, help='show version info')
    args = parser.parse_args(sys.argv[1:])

    # judge args
    if args.version:
        raise SystemExit(f'bcl2fq-local V{VERSION}')

    if not args.i or not args.o:
        raise SystemExit(parser.usage)

    settings['seq_dir'] = os.path.abspath(args.i)
    settings['out_dir'] = os.path.abspath(args.o)
    settings['sample_sheet'] = args.sample_sheet if args.sample_sheet else os.path.join(settings['seq_dir'],
                                                                                        'SampleSheet.csv')
    settings['mismatch'] = args.mismatch
    settings['process'] = args.process
    settings['ioprocess'] = args.ioprocess

    # resolve bcl2fastq bin pathy
    bcl2fastq_sys_path = os.popen('which bcl2fastq').read().strip()
    if args.binpath and os.path.exists(args.binpath):
        settings['binpath'] = args.binpath
    elif os.path.exists('/usr/bin/bcl2fastq'):
        settings['binpath'] = '/usr/bin/bcl2fastq'
    elif os.path.exists(bcl2fastq_sys_path):
        settings['binpath'] = bcl2fastq_sys_path
    else:
        sys.exit('bcl2fastq path not found, please specify the dir!')

    settings['dry_run'] = args.dry_run

    settings['mask_reads'] = args.mask_reads.split(',')
    settings['mask_indexs'] = args.mask_index.split(',')
    settings['mask'] = args.mask


def main():
    parse_args()
    gen_conf()
    cmd = gen_commmand()
    print(cmd)
    if not settings['dry_run']:
        run_bcl2fq(cmd)
        move_undetermined_files()


if __name__ == '__main__':
    main()
