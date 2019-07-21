filename = "test/test_parsers/test_rst/test_directives/utf-16.csv"
filename = "utf-16_win.csv"
filename = "utf-16_macosx.csv"

with open(filename, encoding='utf-16') as f:
    for line in f:
        print(repr(line))
