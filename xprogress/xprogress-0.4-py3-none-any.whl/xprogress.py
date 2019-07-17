import shutil
import time
"""
import xprogress 

>> pbar = xprogress.bar()
>> N = 200000
>> for i in range(i, N+1): pbar(i, N, f'{i}')
>> pbar = xprogress.bar(True)
>> for i in range(i, N+1): pbar(i, N, f'{i}', size=40)

pbar(n, total, desc='', size=None)
    n: i-th of the loop
    total: size of loop
    desc(optional): any string describing current i-th of the loop 
    size(optional): set width of the progress bar

"""

def bar(eta=False):
    ts = eta and time.time() or None

    def fmt(s): 
        m, s = divmod(int(s), 60)
        h, m = divmod(m, 60)
        h = h and f'{h}h ' or ''
        m = m and f'{m}m ' or ''
        return h + m + f'{s}s'

    def progress(n, total, desc='', size=None):
        cols = shutil.get_terminal_size().columns
        if not size: size = int(0.7*cols) - len(desc) 
        size = min(max(10, size), int(0.7*cols))
        done = round(1. * size * n / total)
        percents = round(100. * n / total, 1)
        FILL = ' ' + ''.join(map(chr, range(0x258F, 0x2587, -1)))
        BAR = FILL[-1] * done + FILL[0] * (size - done)
        dt = ts and time.time() - ts or None
        dt = dt and (total-n) / n * dt or None
        dt = (ts and n == total) and time.time() - ts or dt
        desc = dt and f'{desc} [{fmt(dt)}]' or desc
        end = n == total and '\n' or '\r'
        print(f'{percents: 8.1f}% |{BAR}|  {desc}'.ljust(cols), end=end)
    return progress
