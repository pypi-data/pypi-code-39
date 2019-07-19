import os
import sys
import time
def main():
    os.popen('cd ' + os.getcwd() + '\n')
    try:
        if sys.argv[1] == 'tags':
            print('push tags\n')
            os.popen('git push --tags\n')
        elif sys.argv[1] == 'all':
            os.popen('git add .\n')
            os.popen('git commit -m "update"\n')
            print('push commit')
            os.popen('git push\n')
            print('push tags')
            os.popen('git push --tags\n')
        elif sys.argv[1] == 'commit':
            print('push commit')
            os.popen('git add .\n')
            os.popen('git commit -m "update"\n')
            os.popen('git push\n')
    except IndexError:
        if(os.path.exists(os.getcwd()+'\.git')):
            pass
        else:
            choose = input('未检测到.git文件夹，是否生成(yes or no) |yes| ')
            if choose == 'y':
                os.popen('git init\n')
            elif choose == 'yes':
                os.popen('git init\n')
        os.popen('git add .\n')
        print('请输入提交理由')
        commit = input('提交理由: ')
        if commit == '' :
            os.popen('git commit -m update\n')
        else:
            os.popen(('git commit -m "'+commit+'"'))
        os.popen('git push\n')