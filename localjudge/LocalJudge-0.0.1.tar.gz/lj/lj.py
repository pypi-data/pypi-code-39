# -*-coding:utf-8-*-

import datetime
import json
import logging
import platform
import shutil
import sys
from sys import exit
from pathlib import Path
from string import Template
import subprocess
import argparse
import colorful
from lj.utils import get_now_ms

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.NOTSET)
fmt = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)s]: %(message)s")
handler.setFormatter(fmt)
logger = logging.getLogger(__name__)
logger.addHandler(handler)

JSON_OUTPUT = False


def compile_source(src_file: str, temp_exe, command) -> (int, str):
    src_file = Path(src_file).resolve()
    command = Template(command).substitute(
        src=src_file.resolve(),
        temp_exe=temp_exe)
    code, out = subprocess.getstatusoutput(command)
    logger.debug("compile command: %s" % command)
    logger.debug("compile result: code=%d %s" % (code, out))
    return code, out


def judge_run(exe_path=None, stdin=None, expected_out=None):
    t1 = get_now_ms()
    logger.debug("t1: %d" % t1)
    ps = subprocess.Popen(exe_path,
                          shell=False,
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    t2 = get_now_ms()
    logger.debug("t2: %d" % t2)
    logger.debug("t2-t1: %d" % (t2 - t1))

    logger.debug("exe path: %s" % exe_path)
    logger.debug("stdin: %s" % stdin)
    logger.debug("expected_out: %s" % expected_out)

    stdout, _ = ps.communicate(stdin)
    # TODO: 处理 Runtime Error 等

    t3 = get_now_ms()
    logger.debug("t3: %d" % t3)
    logger.debug("t3- t2: %d" % (t3 - t2))
    logger.debug("t3- t1: %d" % (t3 - t1))

    logger.debug("stdout: %s" % stdout)

    stdout = stdout.decode().rstrip()
    expected_out = expected_out.rstrip()
    if expected_out == stdout:
        return True, stdout, t2 - t1
    else:
        return False, stdout, t2 - t1


def judge(src=None, case_index=None, time_limit=0):
    src_path = Path(src).resolve()
    data_dir = get_data_dir(src)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_dir = data_dir / "temp" / timestamp
    temp_dir.mkdir(parents=True, exist_ok=True)

    temp_exe = str(temp_dir / src_path.stem)
    if platform.system() == "Windows":
        temp_exe += ".exe"

    options = load_options()
    lang = None
    if src_path.suffix == ".c":
        lang = "c"
    elif src_path.suffix in [".cpp", ".cc", "cxx"]:
        lang = "c++"

    json_result = {
        "compile": {"code": 0, "errmsg": "", "command": options[lang],
                    "src": str(src_path), "dest": temp_exe, },
        "cases": [],
        "time_limit": time_limit,
        "memory_limit": -1,
        "all": 0, "ac": 0, "wa": 0,
        "tle": 0, "mle": 0, "ole": 0
    }

    code, out = compile_source(str(src_path), temp_exe, options[lang])
    json_result["compile"]["code"] = code
    json_result["compile"]["errmsg"] = out
    if code != 0:
        return json_result

    ac_count = 0
    wa_count = 0
    tle_count = 0
    # TODO: memory limit
    mle_count = 0
    # TODO: output limit
    ole_count = 0

    cases = get_cases(data_dir) if case_index is None else [case_index]
    case_count = len(cases)
    logger.debug("cases (%d): %s" % (case_count, cases))

    json_result["all"] = case_count
    for case in cases:

        with open(str(data_dir / (case + ".in")), "rb") as inf, \
                open(str(data_dir / (case + ".out")), "r") as outf:

            stdin = inf.read()
            expected_out = outf.read()
            result, out, ms = judge_run(exe_path=temp_exe,
                                        stdin=stdin,
                                        expected_out=expected_out
                                        )

            case_result = {
                "index": case,
                "status": "UNKNOWN",
                "time": ms, "memory": -1,
                "in": stdin.decode(), "out": out, "expected": expected_out
            }

            is_timeout = time_limit != 0 and ms >= time_limit
            if is_timeout:
                tle_count += 1
                case_result["status"] = "Time Limit Exceeded"
            elif not result:
                case_result["status"] = "Wrong Answer"
                wa_count += 1
            else:
                case_result["status"] = "Accepted"
                ac_count += 1
            json_result["cases"].append(case_result)

    json_result["ac"] = ac_count
    json_result["wa"] = wa_count
    json_result["tle"] = tle_count
    json_result["mle"] = mle_count
    json_result["ole"] = ole_count
    return json_result


def get_data_dir(src):
    src_path = Path(src)
    stem = str(src_path.stem)
    return (src_path.parent / stem).resolve()


def load_options():
    default_options = {
        "c": "gcc ${src} -o ${temp_exe}",
        "c++": "g++ ${src} -o ${temp_exe}"
    }

    file = Path.home() / ".localjudge.json"
    if file.exists():
        with open(str(file.resolve()),"rt") as f:
            options = json.load(f)
    else:
        logger.debug("config file not found!")
        options = default_options
        with open(str(file.resolve()), "w") as f:
            f.write(json.dumps(default_options, indent=4))

    return options


def get_cases(data_dir):
    cases = map(lambda x: str(x.stem), data_dir.glob("*.in"))
    return sorted(cases)


def show(src: Path):
    data_dir = get_data_dir(src)
    cases = get_cases(data_dir)

    print("case count:%d", len(cases))
    readme_file = data_dir / "README.md"
    if readme_file.exists():
        with open(readme_file, "r") as f:
            print(f.read())
    else:
        print("no readme!")
    for case in cases:
        with open(str(data_dir / (case + ".in")), "rb") as inf, \
                open(str(data_dir / (case + ".out")), "r") as outf:
            print("-> case [%s]" % case)
            stdin = inf.read()
            expected_out = outf.read()
            print("   stdin:\n" +
                  "   " + stdin.decode())
            print("   expected out:\n" +
                  "   " + expected_out)


def main():
    parser = argparse.ArgumentParser(description="Local Judge")
    parser.add_argument("src",
                        help="source file")
    parser.add_argument("-c",
                        "--case",
                        help="index of test case")
    parser.add_argument("-t",
                        "--timelimit",
                        type=int,
                        default=0,
                        help="time limit (ms)")

    parser.add_argument("-d", "--debug", dest="debug", action="store_true",
                        help="debug mode")
    parser.add_argument("-s", "--show", dest="show", action="store_true",
                        help="show cases")
    parser.add_argument("--clean", dest="clean", action="store_true",
                        help="clean temp directory")
    # TODO: 输出json数据，便于测试
    parser.add_argument("--json", dest="json", action="store_true",
                        help="output as json")

    args = parser.parse_args()
    JSON_OUTPUT = args.json

    if args.debug:
        logger.setLevel(logging.DEBUG)

    logger.debug("args: %s" % args)

    src = Path(args.src)

    if not src.is_file():
        print("file does not exist.")
        exit(-1)

    if args.show:
        show(src=src)
        exit()

    if args.clean:
        data_dir = get_data_dir(args.src)
        dir_path = str((data_dir / "temp").resolve())
        print("clean temp dir" + dir_path)
        shutil.rmtree(dir_path)
        exit()

    judge_result = judge(src=src,
                         case_index=args.case,
                         time_limit=args.timelimit)

    if JSON_OUTPUT:
        print(json.dumps(judge_result, indent=4, ensure_ascii=False))
        exit()
    else:
        compile_result = judge_result["compile"]
        if compile_result["code"] != 0:
            print(colorful.red("Compile Error"))
            print(colorful.red("command: %s" % compile_result["command"]))
            print(colorful.red("src: %s" % compile_result["src"]))
            print(colorful.red("dest: %s" % compile_result["dest"]))
            print(colorful.red("code: %d" % compile_result["code"]))
            print(colorful.red("error:\n%s" % compile_result["errmsg"]))
            exit()

        for case in judge_result["cases"]:
            status = case["status"]
            color_func = colorful.green \
                if status == "Accepted" else colorful.red

            print(color_func("-> case [%s] <- %s in %d ms"
                             % (case["index"], case["status"], case["time"])))
            if status == "Wrong Answer":
                print("   stdin:\n" +
                      "   " + case["in"])
                print("   stdout:\n" +
                      "   " + case["out"])
                print("   expected:\n" +
                      "   " + case["expected"])
            if status == "Time Limit Exceeded":
                print("   [time] spent: %d, limit: %d" % (case["time"], judge_result["time_limit"]))
        print("=====summary=====")
        print("All(%d): " % judge_result["all"], end=" ")
        for case in judge_result["cases"]:
            color_func = colorful.green \
                if case["status"] == "Accepted" else colorful.red
            print(color_func(case["index"]), end=" ")
        print()
        print("Wrong Answer: %d" % judge_result["wa"],
              "Time Limit Exceeded : %d" % judge_result["tle"],
              "Memory Limit Exceeded : %d" % judge_result["mle"]
              )
        ac_rate = (judge_result["ac"] / float(judge_result["all"]) * 100)
        color_func = colorful.green if ac_rate == 100 else colorful.red

        print(color_func("Accepted: %d (%f %%)" %
                         (judge_result["ac"], ac_rate)))


if __name__ == "__main__":
    main()
