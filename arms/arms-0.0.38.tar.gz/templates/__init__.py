import requests


def level_list():
    index_text = requests.get('http://gitlab.parsec.com.cn/qorzj/chiji-tool/raw/master/templates/.index.txt').text
    return [line.strip() for line in index_text.splitlines() if line.strip()]


def out_levels():
    return list(set(x.split('-', 1)[0] for x in level_list()))


def inner_levels(prefix):
    return list(set(x.split('-', 1)[-1] for x in level_list() if x.startswith(prefix + '-')))
