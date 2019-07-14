

def log_deco(logger):
    def d_log(func):
        def call(*args, **kwargs):
            res = func(*args, **kwargs)
            logger.info(
                f'Функция {func.__name__}  получила {args,kwargs} вернула {res}')
            return res
        return call
    return d_log
