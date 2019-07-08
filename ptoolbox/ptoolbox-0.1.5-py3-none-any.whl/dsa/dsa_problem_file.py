import codecs
import os
import re

from helpers.clog import CLog


def create_problem(folder, problem_code, overwrite=False):
    problem_code = problem_code.replace('-', '_').replace(' ', '_').lower()

    problem_folder =  os.path.join(folder, problem_code)

    if os.path.exists(problem_folder):
        if not overwrite:
            CLog.error('Problem folder existed! Delete the folder or use `overwrite` instead.')
            return
        else:
            CLog.warn('Problem folder existed! Content will be overwritten.')

    if not os.path.exists(problem_folder):
        os.makedirs(problem_folder)

    # if not os.path.exists(problem_folder + "/testcases"):
    #     os.makedirs(problem_folder + "/testcases")

    problem_name = (' '.join(problem_code.split('_'))).title()

    f = codecs.open(problem_folder + ("/%s.md" % problem_code), "w", "utf-8")
    f.write(
        f"""[//]: # (http://source.link)
[//]: # (hackerrank_id: )  

# {problem_name}
[//]: # ({problem_code})

Nhập vào `3` số nguyên `B`, `P`, `M`. Hãy tính:

$$R = B^P \mod M$$   
 
## Input

- Dòng đầu chứa số tự nhiên `T` - số lượng các testcase
- `T` dòng sau, mỗi dòng chứa `3` số nguyên không âm `B`, `P`, `dM`.

## Constraints

- $0 ≤ B, P ≤ 2^{{31}} - 1$
- $1 ≤ M ≤ 46340$

## Output

`1` số `R` là kết quả phép tính $R = B^P \mod M$

## Tags

- Number Theory 
- Recursion

## Sample input 1

```
3 18132 17  
```

## Sample output 1

```
13
```

## Explanation 1

Giải thích cho sample test case 1
""")

    f.close()

    open(problem_folder + "/testcases.txt", 'w').close()
    f = open(problem_folder + "/testcases_manual.txt", 'w')
    f.write("""### 0
input 0
---
output 0
### 1
input 1
---
output 1
### 2
input 2
---
output 2
""")
    f.close()

    f = open(problem_folder + ("/%s.py" % problem_code), 'w')
    f.write(
        f"""def pmod(a, b, mod):
	if b == 0:
		return 1
	res = pmod(a, int(b / 2), mod)
	res = (res * res) % mod
	if b % 2 == 1:
		return (res * a) % mod
	return res


def {problem_code}(b, p, m):
	return pmod(b, p, m)


if __name__ == "__main__":
	[b, p, m] = map(int, input().split())
	result = {problem_code}(b, p, m)
	print(result)
""")
    f.close()

    f = open(problem_folder + ("/%s_generator.py" % problem_code), 'w')
    f.write(
        ("""from contextlib import redirect_stdout
from helpers.clog import CLog
from helpers.crandom import CRandom


manual_tests_input = [
	(3, 18132, 17),
	(17, 1765, 3),
	(2374859, 3029382, 36123)
]

test_number = 0

CLog.echo("Writing manual testcases...")

with open('testcases_manual.txt', "w") as f:
	with redirect_stdout(f):
		for test in manual_tests_input:
			print(f"### {test_number} - manual")
			print(*test)
			print("---")
			result = %s(*test)
			print(result)
			test_number += 1

CLog.echo("DONE")
CLog.echo("Generating testcases...")

NUMBER_OF_TESTCASES = 20
test_number = 0
with open('testcases.txt', "w") as f:
	with redirect_stdout(f):
		for test in range(NUMBER_OF_TESTCASES):
			if test < 5:
				vmax = 100
			elif test < 10:
				vmax = 100000
			elif test < 15:
				vmax = 1000000
			else:
				vmax = 2**31-1

			a = CRandom.int(0, vmax)
			b = CRandom.int(0, vmax)
			m = CRandom.int(1, 46340)

			print(f"### {test_number}")
			print(a, b, m)
			print("---")
			result = %s(a, b, m)
			print(result)
			test_number += 1
CLog.echo("DONE")

""" % (problem_code, problem_code))
    )
    f.close()

    problem_folder = os.path.abspath(problem_folder)

    CLog.important(f'Problem created at `{problem_folder}`')


def read_testcases_from_file(testcase_file):
    count = 0
    inputi = ""
    outputi = ""
    is_output = False

    testcases = []

    with open(testcase_file, 'r') as fi:
        for line in fi:
            if line.startswith("###"):

                if count > 0:
                    testcases.append({'input': inputi.strip(), 'output': outputi.strip()})

                count += 1

                is_output = False

                inputi = outputi = ""

                continue
            elif line.startswith("---"):
                is_output = True
            else:
                if is_output:
                    outputi += line
                else:
                    inputi += line

        testcases.append({'input': inputi.strip(), 'output': outputi.strip()})

    return testcases


def find_section(pattern, lines, start_index=0):
    indices = []
    content = []
    for i in range(start_index, len(lines)):
        if re.match(pattern, lines[i], re.I):
            indices.append(i)
            for j in range(i+1, len(lines)):
                if lines[j].startswith('#'):
                    break
                content.append(lines[j])

    return indices, content


def check_section(name, pattern, lines, proper_line, unique=True, start_index=0, log_error=True):
    lines, content = find_section(pattern, lines, start_index)
    if log_error:
        flog = CLog.error
    else:
        flog = CLog.warn
    if not lines:
        flog(f'{name} is missing or invalid: {name} should has style: `{proper_line}`')
        return None, None
    if unique and len(lines) > 1:
        CLog.error(f'Only one {name} allowed!')

    empty = True
    for line in content:
        if line.strip() and not line.startswith('[//]:'):
            empty = False
    if empty:
        flog(f'{name} is empty!')

    return lines[0], content


def check_problem(problem_folder):
    problem_code = os.path.basename(problem_folder.rstrip(os.path.sep))

    statement_file = os.path.join(problem_folder, f"{problem_code}.md")
    solution_file = os.path.join(problem_folder, f"{problem_code}.py")
    test_generator_file = os.path.join(problem_folder, f"{problem_code}_generator.py")
    testcase_file = os.path.join(problem_folder, f"testcases.txt")
    testcase_manual_file = os.path.join(problem_folder, f"testcases_manual.txt")

    # if not os.path.isfile(statement_file):
    #     raise SyntaxError(f'Problem statement file `{problem_code}.md` is missing!')

    if not os.path.isfile(solution_file):
        CLog.error(f"Solution file `{problem_code}.py` is missing!")
    if not os.path.isfile(test_generator_file):
        CLog.error(f"Testcase generator file `{problem_code}_generator.py` is missing!")
    if not os.path.isfile(testcase_file):
        CLog.error(f"Testcases file `testcases.txt` is missing!")
    else:
        file_size = os.stat(testcase_file).st_size
        if file_size > 50*1024*1024:
            CLog.error(f"Testcases file `testcases.txt` should not be > 50MB!")

    if not os.path.isfile(testcase_manual_file):
        CLog.warn(f"Manual testcases file `testcases_manual.txt` is missing!")

    with open(statement_file) as fi:
        statement = fi.read()
        # print(statement)
        lines = statement.splitlines()

        if not lines[0].startswith('[//]: # ('):
            CLog.error('The first line should be the source of the problem, ex. `[//]: # (http://source.link)`')

        title_line, statement = check_section('Title', '# \S*', lines, '# Problem Title (heading 1)')

        if title_line:
            title = lines[title_line]
            proper_title = (' '.join(title.split('_'))).title()
            if title != proper_title:
                CLog.warn(f'Improper title: `{title}`, should be `{proper_title}`')
            proper_problem_code = f'[//]: # ({problem_code})'
            if lines[title_line+1] != proper_problem_code:
                CLog.error(f'Title should be followed by proper problem code: `{proper_problem_code}`')

        input_line, input = check_section('Input', '## Input\s*$', lines, '## Input')
        if input_line and title_line and input_line<title_line:
            CLog.error('Input should go after the Problem Statement.')

        constraints_line, constraints = check_section('Constraints', '## Constraints\s*$',
                                                      lines, '## Constraints')
        if constraints_line and input_line and constraints_line < input_line:
            CLog.error('Constraints should go after the Input.')

        output_line, output = check_section('Output', '## Output\s*$', lines, '## Output')
        if output_line and constraints_line and output_line < constraints_line:
            CLog.error('Output should go after the Constraints.')

        tag_line, tag = check_section('Tags', '## Tags\s*$', lines, '## Tags')
        if tag_line and output_line and tag_line < output_line:
            CLog.error('Tags should go after the Output.')

        list_lines, list = find_section('- .*', lines)
        for i in list_lines:
            if i>0:
                prev_line = lines[i-1]
                if prev_line.strip() and not prev_line.startswith('- '):
                    CLog.error(f'There should be an empty line before the list, line {i}: {lines[i]}')

        check_section('Sample input', '## Sample input', lines, '## Sample input 1', unique=False)
        check_section('Sample output', '## Sample output', lines, '## Sample output 1', unique=False)
        check_section('Explanation', '## Explanation', lines, '## Explanation 1', unique=False, log_error=False)


if __name__ == '__main__':
    # create_problem('../problems', 'Array001 Counting-Sort2', overwrite=True)

    check_problem('/home/thuc/teko/online-judge/dsa-problems/array1d/arr005_merge_arrays')
    # check_problem('/home/thuc/teko/online-judge/dsa-problems/array1d/arr001_counting_sort')

    # tcs = read_testcases_from_file('../problems/prob1/testcases.txt')
    # print(*tcs, sep='\n')
