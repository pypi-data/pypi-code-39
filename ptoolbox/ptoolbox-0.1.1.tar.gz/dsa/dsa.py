import codecs
import os
from helpers.clog import CLog


def create_problem(folder, problem_code, overwrite=False):
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

    f = codecs.open(problem_folder + ("/%s.md" % problem_code), "w", "utf-8")
    f.write(
        f"""[//]: http://source.link

## {problem_code}
Nhập vào số nguyên dương `N`. 

In ra số thứ tự của số Fibonacci đầu tiên có `N` chữ số.   
 
## Input
Dòng đầu chứa số tự nhiên `T` - số lượng các testcase

`T` dòng sau, mỗi dòng chứa một số tự nhiên `N`

## Constraints
- 1 ≤ T ≤ 10<sup>9</sup>
- 10 ≤ N ≤ 10<sup>9</sup>

## Output
`T` dòng, dòng thứ i chứa kết quả của test case thứ i: số thứ tự của số Fibonacci đầu tiên có `N` chữ số.

## Sample input 1
```
2    
```

## Sample output 1
```
7
```

## Explanation 1
Giải thích cho test case 1
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
        f"""def {problem_code}(n):
    return n


if __name__ == "__main__":
    N = int(input())
    result = {problem_code}(N)
    print(result)
""")
    f.close()

    f = open(problem_folder + ("/%s_generator.py" % problem_code), 'w')
    f.write(
        """import random

for test in range(20):
    maxn = 1000
    maxval = 100000
    if test < 5:
        maxn = 10
        maxval = 30
    n = random.randint(1, maxn)
    a = []
    for i in range(n):
        a.append(random.randint(0, maxval))      
    print("###")
    print(n)
    print(*a)
    print("---")
    result = {}(a)
    print(result)
        """.format(problem_code)
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


if __name__ == '__main__':
    # create_problem('../problems', 'prob1', overwrite=True)

    tcs = read_testcases_from_file('../problems/prob1/testcases.txt')
    print(*tcs, sep='\n')
