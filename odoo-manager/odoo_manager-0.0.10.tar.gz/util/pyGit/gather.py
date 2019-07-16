import os
from datetime import datetime, timezone
import humanize
from itertools import cycle
from git import Repo


def lastDir(aString):
    return aString.split("/")[-2]


# Set the directory you want to start from
rootDir = "/home/pbuller/"
gitRepos = []
today = datetime.now(timezone.utc)

for dirName, subdirList, fileList in os.walk(rootDir):
    if dirName[-4:] == ".git":
        print("Found directory: %s" % dirName[:-4])
        gitRepos.append(dirName[:-4])

all_four = 'style="border: 1px solid black"'
left = 'style="border-left: 1px solid black; border-top: 1px solid black; border-bottom: 1px solid black;"'
right = 'style="border-right: 1px solid black; border-top: 1px solid black; border-bottom: 1px solid black;"'
topbot = 'style="border-top: 1px solid black; border-bottom: 1px solid black;"'

side_color = cycle(["#ffa500", "#005aff"])

f = open("git_report.html", "w")
f.write('<TABLE border=0 cellspacing=0 style="border-collapse: collapse">')

f.write(
    '<TR><TD bgcolor="#87CEEB" style="width:9px;"><TD colspan=7 %s>filesystem location of repo. Red indicates uncommited changes.'
    % all_four
)
f.write('<TR><TD bgcolor="#87CEEB"><TD colspan=4 %s>Local Branch' % all_four)
f.write("    <TD colspan=3 %s>Remote Branch" % all_four)
f.write('<TR><td bgcolor="#87CEEB"><TD %s>Branch name. Gray -> current branch' % left)
f.write("    <TD %s>Author" % topbot)
f.write("    <TD %s>Last Commit" % topbot)
f.write("    <TD %s>Summary" % right)
f.write("    <TD %s>Author" % left)
f.write("    <TD %s>Last Commit" % topbot)
f.write("    <TD %s>Summary" % right)

gitRepos.sort(key=lastDir)
for gitdir in gitRepos:
    sc = next(side_color)
    repo = Repo(gitdir)
    print(gitdir)
    if repo.is_dirty():
        f.write('<TR><TD bgcolor="%s"><TD colspan=7 bgcolor="red" %s>%s' % (sc, all_four, gitdir))
    else:
        f.write('<TR><TD bgcolor="%s"><TD colspan=7 bgcolor="gray" %s>%s' % (sc, all_four, gitdir))

    for branch in repo.branches:
        if branch == repo.head.ref:
            f.write('<TR bgcolor="#dddddd"><td bgcolor="%s"><TD %s>%s' % (sc, left, branch))
        else:
            f.write('<TR bgcolor="#ffffff"><td bgcolor="%s"><TD %s>%s' % (sc, left, branch))
        f.write("<TD %s>%s" % (topbot, branch.commit.author))
        f.write("<TD %s>%s" % (topbot, humanize.naturaltime(today - branch.commit.committed_datetime)))
        f.write("<TD %s>%s" % (right, branch.commit.summary))
        trbranch = branch.tracking_branch()
        if trbranch:
            f.write("<TD %s>%s" % (left, trbranch.commit.author))
            f.write("<TD %s>%s" % (topbot, humanize.naturaltime(today - trbranch.commit.committed_datetime)))
            f.write("<TD %s>%s" % (right, trbranch.commit.summary))

f.write("</TABLE>")
f.close()
