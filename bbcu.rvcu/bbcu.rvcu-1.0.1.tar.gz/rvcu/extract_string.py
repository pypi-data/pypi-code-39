import sys

file= sys.argv[1]
string= sys.argv[2]
with open(file) as f:
    j=1
    for i in f:
        i=i.rstrip()
        if j%4 == 2:
            indx = i.find(string)
            if indx >= 30 and not i.endswith(string):
                print i[indx+len(string):indx+len(string)+21]
        else:
            j+=1
