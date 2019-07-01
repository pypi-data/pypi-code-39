import shutil
from zipfile import ZipFile
import os

from dsa import dsa
from helpers.clog import CLog


def chomp(s):
    # if s.endswith("\r\n"): return s[:-2]
    # if s.endswith("\n"): return s[:-1]
    return s.strip()


def save_testcase_file(testcase_folder, tc_number, tc_input, tc_output):
    inp_folder = os.path.join(testcase_folder, "input")
    out_folder = os.path.join(testcase_folder, "output")

    if not os.path.exists(inp_folder):
        os.makedirs(inp_folder)

    CLog.echo(f"Writing testcase #{tc_number}")
    CLog.echo("   input...")

    f = open(os.path.join(inp_folder ,"input%02d.in" % tc_number), "w")
    f.write(tc_input)
    f.close()

    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    CLog.echo("   output...")
    f = open(os.path.join(out_folder, "output%02d.out" % tc_number), "w")
    f.write(tc_output)
    f.close()


def prepare_testcases_from_file(tc_file, testcase_output_folder, start_number=0):
    testcases = dsa.read_testcases_from_file(tc_file)

    for i in range(len(testcases)):
        save_testcase_file(testcase_output_folder, start_number+i, testcases[i]['input'], testcases[i]['output'])

    return start_number + len(testcases)


def prepare_testcases(problem_folder, keep_zip_file_only=True):
    zipfilename = 'testcases_hackerrank.zip'
    testcase_output_folder = os.path.abspath(os.path.join(problem_folder, "testcases"))

    if os.path.exists(os.path.join(testcase_output_folder, zipfilename)):
        CLog.warn('`testcases.zip` file existed, will be overwritten.')

    testcase_file = os.path.abspath(os.path.join(problem_folder, "testcases_manual.txt"))

    count = 0
    if not os.path.exists(testcase_file):
        CLog.warn(f'`{testcase_file}` file not existed, skipping...')
    else:
        count = prepare_testcases_from_file(testcase_file, testcase_output_folder, count)

    testcase_file = os.path.abspath(os.path.join(problem_folder, "testcases.txt"))
    if not os.path.exists(testcase_file):
        CLog.warn(f'`{testcase_file}` file not existed, skipping...')
    else:
        count = prepare_testcases_from_file(testcase_file, testcase_output_folder, count)

    print("DONE")

    if count:
        zip_test_cases(problem_folder, count, zipfilename)

        if keep_zip_file_only:
            CLog.echo(f"Deleting intermediate files...")
            shutil.rmtree(testcase_output_folder)
            print("DONE")
    else:
        CLog.error(f'No testcases found in {os.path.abspath(problem_folder)}')

    return count


def zip_test_cases(problem_folder, count, zipfilename):
    problem_folder = os.path.abspath(os.path.join(problem_folder, "testcases"))
    zipfile = os.path.join(problem_folder, '..', zipfilename)
    print(f"creating `{os.path.abspath(zipfile)}`")

    os.chdir(problem_folder)
    with ZipFile(zipfile, 'w') as myzip:
        for i in range(count):
            myzip.write("input/input%02d.in" % i)
            myzip.write("output/output%02d.out" % i)

    print("DONE")


if __name__ == "__main__":
    prepare_testcases("../problems/prob1", True)

