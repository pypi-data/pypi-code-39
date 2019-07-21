# coding=utf-8
'''provide class Path of type `str`.'''

import os


class Path(str):
    '''
    convenient to join file path in a chain manner:
    s = s.join('a', 'b').join('..')
    '''

    def join(self, *args, **kw):
        '''
        join file path, call this method like os.path.join

        Example: Path('./dir/sub').join('..')  ->  './dir'
        '''
        return Path(os.path.normpath(os.path.join(self, *args, **kw)))


__all__ = ['Path']
