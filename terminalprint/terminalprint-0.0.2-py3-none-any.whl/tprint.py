# coding: utf-8

def table_print(table, has_caption=True, align_type="LEFT"):
    """table_print"""
    # copy table
    table = table[0:]

    # max length of each field data in the table
    fields_len = fields_length_max(table)

    # convert align type to pad type
    pad_type = convert_align_type_to_pad_type(align_type)

    # make tpl and separation field pad data
    content_tpl = "| "
    separation_tpl = "+-"
    separation_data = []
    for (index, fmlen) in fields_len.items():
        content_tpl = content_tpl + "{} | "
        separation_tpl = separation_tpl + "{}-+-"
        separation_data.append(str_pad("", fmlen, "-", pad_type))
    content_tpl = content_tpl.rstrip()
    separation_tpl = separation_tpl.rstrip("-")

    # output data
    print(separation_tpl.format(*separation_data))
    if has_caption:
        caption = table.pop(0)
        content = [str_pad(item, fields_len[index], " ", pad_type) for index, item in enumerate(caption)]
        print(content_tpl.format(*content))
        print(separation_tpl.format(*separation_data))
    for row in table:
        content = [str_pad(item, fields_len[index], " ", pad_type) for index, item in enumerate(row)]
        print(content_tpl.format(*content))
    print(separation_tpl.format(*separation_data))

def fields_length_max(table):
    """fields_length_max"""
    fields_len = {}

    for row in table:
        for index, item in enumerate(row):
            item_len = str_len(item)
            if index not in fields_len:
                fields_len[index] = item_len
                continue

            if fields_len[index] < item_len:
                fields_len[index] = item_len

    return fields_len

def convert_align_type_to_pad_type(align_type):
    """convert_align_type_to_pad_type"""
    pad_type = ''

    align_type = align_type.upper()
    if align_type == 'RIGHT':
        pad_type = 'STR_PAD_LEFT'
    elif align_type == 'LEFT':
        pad_type = 'STR_PAD_RIGHT'
    else:
        pad_type = 'STR_PAD_BOTH'

    return pad_type

def str_pad(istr, pad_len, pad_char, pad_type):
    """str_pad"""
    istr_len = str_len(istr)
    if (istr_len < pad_len):
        diff = pad_len - istr_len
        pad_type = pad_type.upper()
        if pad_type == "STR_PAD_RIGHT":
            istr = istr + pad_char * diff
        elif pad_type == "STR_PAD_LEFT":
            istr = pad_char * diff + istr
        else: # STR_PAD_BOTH
            ll = int(diff / 2)
            rl = diff - ll
            istr = pad_char * ll + istr + pad_char * rl

    return istr

def str_len(istr):
    """str_len"""
    # 一个汉字占2个字符，一个英文占1个字符
    return int((len(istr.encode("utf-8")) + len(istr)) / 2)


if __name__ == '__main__':
    istr = ['你好呀', 'abcd', 'ab哈哈cd']
    for s in istr:
        # sl = str_len(s)
        # print(s + ': ' + str(sl))
        print('|' + str_pad(s, 12, ' ', 'STR_PAD_BOTH') + '|')
        print('|' + str_pad(s, 12, ' ', 'STR_PAD_RIGHT') + '|')
        print('|' + str_pad(s, 12, ' ', 'STR_PAD_LEFT') + '|')
    print()

    table = [
        ["测试表头1", "测试表头2", "测试表头3", '测试表头4'],
        ["哈哈d", "dasfd12f", "哈哈哈哈", '123你好'],
        ["dalfja", "啦啦啦啦短发就是佛的", '大方nmm', '的沙发啊的'],
    ]
    table_print(table)
    print()
    table_print(table, has_caption=False)
    print()
    table_print(table, has_caption=False, align_type="RIGHT")
    print()
    table_print(table, has_caption=False, align_type="CENTER")
    print()
