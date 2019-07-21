# -*- coding: utf-8 -*-
import os


def file_encode(file_location, original_encode, target_encode='utf-8'):
    """
    this function would help you product a new file with new encode without deleting the old file

    :param filelocation: would be like 'C:\\Users\\jachen\\Desktop\\projects\\dianping_web_crawler\\dianping_page_13.csv'
    :param original_encode:  would be like 'gb2312'
    :param targe_encode:  would be like  'utf-8'
    :return: None
    """
    # 从filelocation中分离出file和path，并命名新的file
    path_list = file_location.split('\\')
    file_name = path_list.pop()
    file_path = '\\'.join(path_list) + '\\'
    new_file_name = file_name.split('.')[0] + '_' + target_encode + "." + file_name.split('.')[1]
    new_file_location = file_path + new_file_name
    i = 0
    try:
        print('正在将文件由{}编码转换成{}编码，请稍后...'.format(original_encode, target_encode))
        with open(file_location, 'r', newline='', encoding=original_encode) as ori_file:
            with open(new_file_location, 'w', newline='', encoding=target_encode) as target_file:
                for row in ori_file:
                    i += 1
                    target_file.write(row)
            print('转码完毕，file总共有{0}行，新的file是{1}'.format(i, new_file_location))
    except (UnicodeDecodeError, UnicodeEncodeError, UnicodeError, UnicodeTranslateError, UnicodeWarning):
        raise UnicodeEncodeError('请检查原始文件的编码,同时注意，utf-8编码无法无缝转换成gb2312编码')
    except Exception as e:
        print(e)
        pass


def file_merge(file_list, path, encoding='utf-8', header=True):
    """
    this function would merge a list of files into just one file without changing encode and deleting old files

    :param file_list: should be list of file names without path
    :param path: should be the file location, like 'C:\\Users\\jachen\\', and don't forget the backslash in the end of
    the path
    :param encode: should be file encode, like 'utf-8'
    :param header: should be boolean, default is True
    :return: None
    """
    file_merge_name = file_list[0].split('.')[0] + '_merge.' + file_list[0].split('.')[1]

    # 判断下file是否有header，如果有的话，那么就需要把header忽略掉，默认是有header的
    if header:
        # 写入mergefile的header
        print('正在写入header...')
        with open(path + file_merge_name, 'w', newline='', encoding=encoding) as f_out:
            file = file_list[0]
            filename = '{}{}'.format(path, file)
            f = open(filename, 'r', newline='', encoding=encoding)
            header = f.readline()
            f_out.write(header)
            f.close()
        # 开始真正的往里面copy数据
        print('正在合并数据，请稍后...')
        with open(path + file_merge_name, 'a', newline='', encoding=encoding) as f_out:
            for file in file_list:
                filename = '{}{}'.format(path, file)
                f = open(filename, 'r', newline='', encoding=encoding)
                f.readline()
                content = f.read()
                f_out.write(content)
                f.close()
    # 如果没有header， 那么就直接往新的file上面copy就行了
    else:
        print('此file没有header')
        with open(path + file_merge_name, 'a', newline='', encoding=encoding) as f_out:
            for file in file_list:
                filename = '{}{}'.format(path, file)
                f = open(filename, 'r', newline='', encoding=encoding)
                content = f.read()
                f_out.write(content)
                f.close()
    with open(path + file_merge_name, 'r', newline='', encoding=encoding) as f_read:
        file_count = len(f_read.readlines())
        print('合并完毕，file总共count是{}(包括header),新的file是{}'.format(file_count, path + file_merge_name))


def file_split(file_location, divide_num, encoding='utf-8', header=True):
    """
    this function would help you split file to how many you want files evenly

    :param filelocation: would be like 'C:\\Users\\jachen\\Desktop\\projects\\dianping_web_crawler\\dianping_page_13.csv'
    :param divide_num: input the file nums you want to split, like 2,or 3
    :param encoding:  input the orininal file encoding, Default is 'utf-8'
    :param header:  should be boolean, default is True
    :return:  None
    """
    # 从fileloction 那里分离出文件的路径出来
    path_list = file_location.split('\\')
    file_name = path_list.pop()
    file_path = '\\'.join(path_list) + '\\'
    # 如果有header的情况下
    if header:
        print('此file有header，正在读取header...')
        # 读取header
        original_file = open(file_location, 'r', newline='', encoding=encoding)
        file_header = original_file.readline()
        original_file.close()
        # 根据要拆成file的数量，生成相等数量的file，并且添加表头
        print('正在生成新的files,并写入header...')
        new_file_list = []
        for file_number in range(divide_num):
            new_file_name = file_name.split('.')[0] + '_part' + str(file_number + 1) + "." + file_name.split('.')[1]
            new_file_location = file_path + new_file_name
            new_file_list.append(new_file_location)
            with open(new_file_location, 'w', newline='', encoding=encoding) as new_writer:
                new_writer.write(file_header)
        # 开始逐行的拆分文件
        print('正在逐行的拆分file，请稍后...')
        with open(file_location, 'r', newline='', encoding=encoding) as original_read:
            counter = 0
            for row in original_read:
                counter += 1
                # 然后一行一行的进行分拆操作
                if counter >= 2:  # 忽略第一行表头
                    pointer = int(counter % divide_num)
                    with open(new_file_list[pointer], 'a', newline='', encoding=encoding) as file_object:
                        file_object.write(row)
                else:
                    pass
            print('原始文件总共有{}行记录'.format(counter))
            split_records = counter // divide_num
            print('原始文件拆成{0}个文件，每个文件大约含有{1}条记录'.format(divide_num, split_records))
            print('新的files是{}'.format(new_file_list))
    # 如果没有header的情况下
    else:
        print('此file没有header')
        # 直接拆成三个file
        print('正在生成新的files...')
        new_file_list = []
        for file_number in range(divide_num):
            new_file_name = file_name.split('.')[0] + '_part' + str(file_number + 1) + "." + file_name.split('.')[1]
            new_file_location = file_path + new_file_name
            new_file_list.append(new_file_location)
        # 开始拆分文件
        print('正在逐行的拆分file，请稍后...')
        with open(file_location, 'r', newline='', encoding=encoding) as original_read:
            counter = 1
            for row in original_read:
                # 然后一行一行的进行分拆操作
                pointer = int(counter % divide_num)
                with open(new_file_list[pointer], 'a', newline='', encoding=encoding) as file_object:
                    file_object.write(row)
                counter += 1
            print('原始文件总共有{}行记录'.format(counter))
            split_records = counter // divide_num
            print('原始文件将会拆成{0}个文件，每个文件大约含有{1}条记录'.format(divide_num, split_records))
            print('新的files是{}'.format(new_file_list))


def file_dedup(file_location, encoding='utf-8'):
    """
    this function woule deduplicate the give file and return a new file named '_unique' with no duplicate without
    changing original file

    :based on rules: the keys in one dict should not have duplicates
    :param file_location: should be like 'C:\\Users\\jachen\\Desktop\\projects\\dianping_web_crawler\\dianping_page_13.csv'
    :param encoding: default is 'utf-8'
    :return: None
    """
    # 从filelocation中分离出file和path，并命名新的file
    path_list = file_location.split('/')
    file_name = path_list.pop()
    file_path = '/'.join(path_list) + '/'
    new_file_name = file_name.split('.')[0] + '_unique' + "." + file_name.split('.')[1]
    new_file_location = file_path + new_file_name

    # 根据dict的数据结构中，key是不可能有重复的这样的一个特点来进行file的去重
    print('正在根据字典键的不可重复性来去重file，请稍后...')

    # 读取原始file的数量
    fp_file_reader_count = open(file_location, 'r', newline='', encoding=encoding)
    original_file_count = len(fp_file_reader_count.readlines())
    print('原始文件的总共有{}条记录'.format(original_file_count))
    fp_file_reader_count.close()
    # 开始去重
    fp_file_reader = open(file_location, 'r', newline='', encoding=encoding)
    fp_file_new = open(new_file_location, 'w', newline='', encoding=encoding)
    try:
        search_records = fp_file_reader.readlines()
        clean_list = {}.fromkeys(search_records).keys()
        for search_rec in clean_list:
            fp_file_new.write(search_rec)
    except Exception as e:
        print(e)
    finally:
        fp_file_reader.close()
        fp_file_new.close()
    # 计算总共多少record被去重了
    with open(new_file_location, 'r', newline='', encoding=encoding) as fp_file_new_1:
        new_file_count = len(fp_file_new_1.readlines())
        print('新的文件总共有{}条记录'.format(new_file_count))
        print('新的文件删除了{}条重复数据'.format(original_file_count - new_file_count))


if __name__ == '__main__':
    pass
    # # 测试编码转换功能：
    # fileobject = FileHandle()
    # filelocation = r'C:\Users\jachen\PycharmProjects\jason_module\dianping_page1.csv'
    # original_encode = 'utf-8'
    # target_encode = 'utf-16'
    # fileobject.file_encode(filelocation,original_encode,target_encode)

    # 测试合并功能：
    file_dir = r"C:\\Users\\chja7006\\Google Drive\\全能渠道项目\\4.平台开发\\4.平台数据\\平台数据上传\\20190110_正式平台更新后的数据\\platform_admin_attr_201806\admin_attr\\"
    file_list = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if file.endswith('.csv'):
                # print(file)
                file_list.append(file)
    print(file_list)
    file_merge(file_list, file_dir)

    # # 测试拆分file
    # fileobject = FileHandle()
    # filelocation = r'C:\Users\jachen\PycharmProjects\jason_module\dianping_page1.csv'
    # encoding = 'utf-8'
    # fileobject.file_split(filelocation, 10)

    # 测试去重功能
    # filelocation = r'/Users/chenxing/PycharmProjects/Crawler_ChinaAdventure/chinaventure_invest/chinaadventure_page_details_v4.csv'
    # fileinstance = FileHandle()
    # encoding = 'utf-8'
    # fileinstance.file_dedup(filelocation)
