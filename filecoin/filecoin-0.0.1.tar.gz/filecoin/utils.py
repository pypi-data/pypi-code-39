# coding: utf8
import os


def run_command(command):
    try:
        f = os.popen(command)
        result = f.read().strip()
        f.close()
        return result
    except:
        return None


def get_filecoin_bin_filepath():
    bin_filepaths = [
        '/usr/local/bin/go-filecoin',
        '/usr/bin/go-filecoin',
        '/usr/local/bin/filecoin',
        '/usr/bin/filecoin',
    ]
    for filepath in bin_filepaths:
        if os.path.isfile(filepath):
            return filepath
    # at last
    return bin_filepaths[-1]



def run_filecoin_cmd(cmd, split_into_lines=False):
    bin_filepath = get_filecoin_bin_filepath()
    cmd = '%s %s' % (bin_filepath, cmd)
    result = run_command(cmd)
    if not split_into_lines:
        result = result.strip()
        return result
    else:
        lines = []
        if result:
            raw_lines = result.split('\n')
            for line in raw_lines:
                line = line.strip()
                if line: lines.append(line)
        return lines

