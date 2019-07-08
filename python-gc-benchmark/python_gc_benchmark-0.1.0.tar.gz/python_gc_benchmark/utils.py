import sys, os, re, time, six

def cmd_run(outname, args):
    childpid = os.fork()
    if childpid == 0:
        os.execvp(args[0], args)
        sys.exit(1)

    r = re.compile("VmRSS:\s*(\d+)")

    filename = '/proc/%d/status' % childpid
    rss_max = 0
    rss_sum = 0
    rss_count = 0

    f = open(outname, 'w')
    while os.waitpid(childpid, os.WNOHANG)[0] == 0:
        g = open(filename)
        s = g.read()
        g.close()
        match = r.search(s)
        if not match:     # VmRSS is missing if the process just finished
            break
        rss = int(match.group(1))
        #print (rss, file=f)
        print >> f, rss
        if rss > rss_max: rss_max = rss
        rss_sum += rss
        rss_count += 1
        time.sleep(1)
    f.close()

    if rss_count > 0:
        print (args)
        print ('Memory usage:')
        print ('\tmaximum RSS: %10d kb' % rss_max)
        print ('\tmean RSS:    %10d kb' % (rss_sum / rss_count))
        print ('\trun time:    %10d s' % rss_count)