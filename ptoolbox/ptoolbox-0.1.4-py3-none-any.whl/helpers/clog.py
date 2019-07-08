import click


class CLog:
    @staticmethod
    def _log(msg, fg=None, bg=None, bold=None, dim=None, underline=None, blink=None, reverse=None):
        click.echo(click.style(msg, fg=fg, bg=bg, bold=bold, dim=dim,
                               underline=underline, blink=blink, reverse=reverse))

    @staticmethod
    def trivial(msg, **kwargs):
        if 'dim' not in kwargs:
            kwargs['dim'] = True
        CLog._log(msg, **kwargs)

    @staticmethod
    def echo(msg, **kwargs):
        CLog._log(msg, **kwargs)

    @staticmethod
    def info(msg, **kwargs):
        if 'fg' not in kwargs:
            kwargs['fg'] = 'bright_blue'
        CLog._log(msg, **kwargs)

    @staticmethod
    def important(msg, **kwargs):
        if 'fg' not in kwargs:
            kwargs['fg'] = 'green'
        if 'bold' not in kwargs:
            kwargs['bold'] = True
        CLog._log(msg, **kwargs)

    @staticmethod
    def warn(msg, **kwargs):
        if 'fg' not in kwargs:
            kwargs['fg'] = 'yellow'
        CLog._log(msg, **kwargs)

    @staticmethod
    def error(msg, **kwargs):
        if 'fg' not in kwargs:
            kwargs['fg'] = 'bright_red'
        CLog._log(msg, **kwargs)

    @staticmethod
    def fatal(msg, **kwargs):
        if 'fg' not in kwargs:
            kwargs['fg'] = 'bright_red'
        if 'bold' not in kwargs:
            kwargs['bold'] = True
        if 'reverse' not in kwargs:
            kwargs['reverse'] = True
        CLog._log(msg, **kwargs)


if __name__ == '__main__':
    CLog._log('log')
    CLog.trivial('trivial')
    CLog.echo('echo')
    CLog.info('info')
    CLog.info('info', bold=True)
    CLog.important('important')
    CLog.warn('warn')
    CLog.error('error')
    CLog.fatal('fatal')

