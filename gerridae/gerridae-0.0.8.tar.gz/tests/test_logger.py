from gerridae.log import logger


def test_log():
    """test gerridae logger"""
    assert not logger.info('hello world')
