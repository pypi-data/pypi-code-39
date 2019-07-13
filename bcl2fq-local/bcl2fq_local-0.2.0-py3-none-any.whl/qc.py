#!/usr/bin/env python

"""
usage: qc-local [-h] [-r RAW_DIR] [-c CLEAN_DIR] [-q QC_DIR] [-2 ADAPTER_DIR]
                [-t THREADS] [--paired-end] [-v]

A qc wrapper

optional arguments:
  -h, --help      show this help message and exit
  -r RAW_DIR      Raw reads dir input
  -c CLEAN_DIR    Dir to write output clean reads
  -q QC_DIR       Dir to write qc info file, default: <clean_dir>/QC
  -2 ADAPTER_DIR  Dir to write removed reads, default: <clean_dir>/002
  -t THREADS      Threads number for parallel, default:8
  --paired-end    Use qc for paired end reads
  -v, --version   Show version info

"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import os
import glob


VERSION = 'bcl2fq-local V0.2.0'


cmd_template = "{bin} {reads} -f {clean_dir}/{sample} -2 {adapter_dir}/{sample} -q {qc_dir}/{sample} "
base_dir = os.path.dirname(os.path.abspath(__file__))

qc_pe_bin = os.path.join(base_dir, 'bin', 'fastqc_adapter_pe')
qc_se_bin = os.path.join(base_dir, 'bin', 'fastqc_adapter_se')


def handle_args():
    parser = argparse.ArgumentParser(description='A qc wrapper', prog='qc-local')
    parser.add_argument('-r', dest='raw_dir', help='Raw reads dir input', required=False)

    parser.add_argument('-c', dest='clean_dir', help='Dir to write output clean reads', required=False)

    parser.add_argument('-q', dest='qc_dir', required=False,
                        help='Dir to write qc info file, default: <clean_dir>/QC')

    parser.add_argument('-2', dest='adapter_dir', required=False,
                        help='Dir to write removed reads, default: <clean_dir>/002')

    parser.add_argument('-t', dest='threads', default=8, type=int,
                        help='Threads number for parallel, default:8')

    parser.add_argument('--paired-end', dest='pe', action='store_true', default=False,
                        help='Use qc for paired end reads')
    parser.add_argument('--dry-run', action='store_true', dest='dry_run', help='Only print cmd not running')

    parser.add_argument('-v', '--version', dest='version', action='store_true', default=False,
                        help='Show version info', required=False)

    args = parser.parse_args()

    if args.version:
        raise SystemExit(VERSION)

    if not all([args.raw_dir, args.clean_dir]):
        raise SystemExit(parser.print_help())

    if not args.qc_dir:
        args.qc_dir = os.path.join(args.clean_dir, 'QC')

    if not args.adapter_dir:
        args.adapter_dir = os.path.join(args.clean_dir, '002')

    return args


def make_cmds(args):
    samples = {}
    for file in glob.glob('%s/*.fastq.gz' % args.raw_dir):
        sample = file.split('_')[0]  # 下划线是bcl2fastq默认的分隔符
        samples.setdefault(sample, []).append(file)

    if args.pe:
        qc_bin = qc_pe_bin
    else:
        qc_bin = qc_se_bin
    if not os.path.exists(qc_bin):
        raise SystemExit('QC bin file: {qc_bin} not found!'.format(qc_bin=qc_bin))

    cmd_pool = {}

    for sample in samples:
        files = ' '.join(samples[sample])
        cmd = cmd_template.format(bin=qc_bin, reads=files, clean_dir=args.clean_dir, adapter_dir=args.adapter_dir,
                                  sample=sample, qc_dir=args.qc_dir)
        cmd_pool[sample] = cmd
    return cmd_pool


def runner(cmds, threads, required_dirs=None):
    if type(required_dirs) == list:
        for dir in required_dirs:
            os.makedirs(dir, exist_ok=True)
    result_pool = {}
    with ThreadPoolExecutor(max_workers=threads) as ex:
        for sample, cmd in cmds.items():
            result_pool[sample] = ex.submit(os.system, cmd)
    fails = []
    for sample, result in result_pool.items():
        if result.result() != 0:
            fails.append(sample)
    if len(fails) != 0:
        raise SystemExit('%d task failed!' % len(fails))


def main():
    args = handle_args()
    cmds = make_cmds(args)
    if args.dry_run:
        for cmd in cmds.values():
            print(cmd)
        raise SystemExit('Not running...')
    runner(cmds, args.threads, [args.clean_dir, args.qc_dir, args.adapter_dir])


if __name__ == '__main__':
    main()
