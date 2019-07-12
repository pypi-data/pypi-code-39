from utils.datetime import Now


def test_datetime_log_format():
    assert Now.datetime.log_format() == '2019-11-20'
