from GetCCWarc import GetCCWarc


if __name__ == '__main__':
    off, len, file = 437157916, 884, \
                     "crawl-data/CC-MAIN-2019-22/segments/1558232256040.41/warc/" \
                     "CC-MAIN-20190520142005-20190520164005-00160.warc.gz"

    data = GetCCWarc.get_warc_file(file, len, off, gzip=False)
    print(GetCCWarc.get_response(data))
