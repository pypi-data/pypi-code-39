import os, argparse#, textwrap
from PyAxe import ALog, AOS, APyInstaller, ACompress, AUtil

DESCRIPTION = """\
【注意】
1. 执行前，需关闭杀软，否则可能失败
2. 此外，Windows上的explorer.exe有时也可能造成失败（概率较低）

【spec.py】
若当前目录下存在 目标.spec.py，则该目标支持特殊的打包方式。
spec.py的内容，主要应包含设置APyInstaller.ExtraOptions的代码，比如：
extraOptions.datas=[('a.txt', 'res.dir')]
"""

def initArgs(subparsers):

    subparser = subparsers.add_parser('PyInstaller', help='制作可执行文件', description=DESCRIPTION, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparser.add_argument('Targets', nargs='+', help='目标列表')
    subparser.add_argument('--OneFile', action='store_true', help='单文件形式（默认为文件夹形式）')
    subparser.add_argument('--Pack', choices=['none', 'zip', 'tar'], help='打包方式（默认为tar）')
    subparser.add_argument('--NonInteractive', action='store_true', help='非交互模式（默认为交互模式）')


def getTargetsFromInput(args):
    targetMap = [['1', '所有', 'All']]
    index = 2
    for target in args.Targets:
        targetMap.append([('%d' % index), target, target])
        index += 1

    if args.NonInteractive:
        action = 'All'
    else:
        action = AUtil.inputChoice(targetMap, '*** 编译目标 ***')[2]

    if action == 'All':
        return [item[2] for item in targetMap if item[2] != 'All']
    else:
        return [action]


def makePackageFromDist(target, args):
    AOS.makeDir(os.path.join('Installer', 'dist'))
    AOS.removeDir(os.path.join('Installer', 'dist', target))

    # 如果存在杀软，dist/target/*文件可能被杀软占用，进而move失败
    AOS.move(os.path.join('dist', target), os.path.join('Installer', 'dist', target))

    if args.Pack is None:
        packStyle = 'tar'
    else:
        packStyle = args.Pack

    if packStyle != 'none':
        with AOS.ChangeDir(os.path.join('Installer', 'dist')):
            if packStyle == 'zip':
                ACompress.zip(target, target+'.zip')
            elif packStyle == 'tar':
                ACompress.tar(target, target+'.tar.gz')
            else:
                assert False


def makeTarget(target, args):
    extraOptions = APyInstaller.ExtraOptions()
    specFile = target+'.spec.py'
    if os.path.exists(specFile):
        with open(specFile) as fp:
            exec(fp.read(), {}, {'extraOptions':extraOptions})
    with AOS.ChangeDir('..'):
        AOS.removeDir('build')
        AOS.removeDir('dist')
        APyInstaller.execCommand(target+'.py', target, oneFile=args.OneFile, extraOptions=extraOptions)
        makePackageFromDist(target, args)
        AOS.removeDir('build')
        AOS.removeDir('dist')


def main(args):
    if args.SubCommand == 'PyInstaller':
        ALog.enableFileSink(False)
        finalTargets = getTargetsFromInput(args)
        for target in finalTargets:
            makeTarget(target, args)
    else:
        return False
    return True
