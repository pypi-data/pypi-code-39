#!/usr/bin/python
import shelve
import sys
import re
import os
import datetime
import time


#def touch(fname, times=None):
#    with open(fname, 'a'):
#        os.utime(fname, times)

def new_entry(fname, entry, ticket=''):
    if '#' in entry:
        entry, ticket = entry.split('#')
    d = datetime.datetime.now()
    with shelve.open(fname) as prot:
        if not 'last' in prot:
            prot['last'] = '%s-%s-%s-%s' % (str(d.hour).zfill(2), str(d.minute).zfill(2), str(d.second).zfill(2), d.microsecond)
            return

        l = prot['last'].split('-')
        prot[prot['last']] = {
            'from': '%s:%s' % (l[0], l[1]),
            'to': '%s:%s' % (str(d.hour).zfill(2), str(d.minute).zfill(2)),
            'ticket': ticket,
            'text': entry
        }
        prot['last'] = '%s-%s-%s-%s' % (str(d.hour).zfill(2), str(d.minute).zfill(2), str(d.second).zfill(2), d.microsecond)



def print_history(fname):

    with shelve.open(fname) as hist:
        for entry in reversed(sorted(hist)):
            if entry == 'last':
                continue
            e = hist[entry]
            print('{:<6}{:<2}{:<10}{:<10}{:<50}'.format(e['from'], '-', e['to'],e['ticket'], e['text']))

def delete_newest_entry(fname):

    with shelve.open(fname) as f:
        try:
            del f[((sorted(dict(f).keys())[0]))]
        except Exception as e:
            pass
#        newest = sorted(f)[0]
#        print(newest)



if __name__ == "__main__":

    da = datetime.datetime.now()
    protocol = os.path.join(os.getenv("HOME"), 'protocol', '%s-%s-%s.shelve' % (da.day, da.month, da.year))
#    print(protocol)
#    for i in range(10):
#        print("new entry")
#        time.sleep(0.1)
#        new_entry(protocol, 'test')
#    pass
    args = sys.argv
    args.pop(0)

    if(args):
        print('{:<8}{:<10}{:<10}{:<50}'.format('von', 'bis','Ticket', 'Kommentar'))
        operation = args.pop(0)
        suffix = ' '.join(args)
        if re.match('start', operation):
            print("starting time messuring")
            new_entry(protocol, suffix)
            pass
        elif re.match('d', operation):
            delete_newest_entry(protocol)
            print_history(protocol)
        elif re.match('[0-9]*', operation):
            new_entry(protocol, suffix)
            print_history(protocol)

#        print_history(protocol)
    else:
        print('{:<8}{:<10}{:<10}{:<50}'.format('von', 'bis','Ticket', 'Kommentar'))
        print_history(protocol)
        sys.exit(0)


    exit
#    for arg in args:
#        if(arg.startswith('#')):
#            arg = arg.strip('#')
#            del_todo(int(list(arg).pop(0)))
#            break
#        elif arg.startswith('!remove_all'):
#            os.remove(Todo)
#            print('cleared todos')
#            break
#        else:
#            arg = arg.split(',')
#            if(len(arg) == 1):
#                t = arg[0]
#                p = 0
#            elif(len(arg) == 2):
#                t, p = arg
#    
#        save_todo(t, p)
#
#    with shelve.open(protocol) as s:
#        for index,k in enumerate(s):
#            if index==0:
#                buf=k
#                continue
#            t1 = k.split('-')
#            t2 = buf.split('-')
#
#            print('%s:%s - %s:%s %s' % (t2[0], t2[1], t1[0], t1[1],s[buf]))
#            buf=k
