import os
import sys
import time
def main():
    try:
        file = open('./temp/shell.cmd','w')
    except FileNotFoundError:
        os.mkdir('./temp')
        file = open('./temp/shell.cmd','w')
    file.write('cd ' + os.getcwd() + '\n')
    try:
        if sys.argv[1] == 'tags':
            print('push tags\n')
            file.write('git push --tags\n')
        elif sys.argv[1] == 'all':
            file.write('git add .\n')
            file.write('git commit -m "update"\n')
            print('push commit')
            file.write('git push\n')
            print('push tags')
            file.write('git push --tags\n')
        elif sys.argv[1] == 'commit':
            print('push commit')
            file.write('git add .\n')
            file.write('git commit -m "update"\n')
            file.write('git push\n')
    except IndexError:
        if(os.path.exists(os.getcwd()+'\.git')):
            pass
        else:
            choose = input('未检测到.git文件夹，是否生成(yes or no) |yes|')
            if choose == 'y':
                file.write('git init\n')
            elif choose == 'yes':
                file.write('git init\n')
        file.write('git add .\n')
        print('请输入提交理由')
        commit = input('提交理由: ')
        if commit == '' :
            file.write('git commit -m update\n')
        else:
            file.write(('git commit -m "'+commit+'"\n'))
        file.write('git push\n')
    finally:
        file.write('exit')
        os.popen('start '+os.getcwd()+'/temp/shell.cmd')
main()