import unittest
import shutil
import os,time,json,io
import logging
from HttpTesting.globalVar import gl
from HttpTesting.library import HTMLTESTRunnerCN
from HttpTesting.library import scripts
from HttpTesting.library.scripts import (get_yaml_field, start_web_service, write_file)
from HttpTesting.library.emailstmp import EmailClass
from HttpTesting.library.case_queue import case_exec_queue
from HttpTesting import case
from HttpTesting.library.falsework import create_falsework
from HttpTesting.library.har import ConvertHarToYAML
import argparse

########################################################################
#Command line mode.
def run_min():

    #Takes the current path of the command line
    cur_dir= os.getcwd()
    os.chdir(cur_dir)

    parse = argparse.ArgumentParser(description='HttpTesting parameters')

    parse.add_argument(
        "-file", 
        default='', 
        help='The file path; File absolute or relative path.'
        )
    parse.add_argument(
        "-dir", 
        default='',
        help='The folder path; folder absolute or relative path.'
        )
    parse.add_argument(
        "-startproject", 
        default='',
        help='Generate test case templates.'
        )
    parse.add_argument(
        "-config", 
        default='',
        help='Basic setting of framework.'
        )
    parse.add_argument(
        "-har", 
        default='',
        help='Convert the har files to YAML. har file is *.har'
        )
    parse.add_argument(
        "-service", 
        default='',
        help='Convert the har files to YAML. har file is *.har'
        )
    parse.add_argument(
        "-convert", 
        default='',
        help='Convert the har files to YAML. YAML file is *.yaml'
        )



    args = parse.parse_args()
    case_file = args.file
    case_dir = args.dir
    start_project = args.startproject
    config = args.config
    har = args.har
    service = args.service
    vert = args.convert

    # Conver YAML.
    if vert != '':
        yamlfile = os.path.join(cur_dir, str(vert).strip())
        scripts.generate_case_tmpl(yamlfile)

    #Start the a web service.
    if str(service).lower() != '' and str(service).lower() == 'start' :
        start_web_service()


    #Convert har files to YAML.
    #r'D:\httphar.har'
    if har != '':
        temp_dict = ConvertHarToYAML.convert_har_to_ht(har)
        ConvertHarToYAML.write_case_to_yaml('', temp_dict)

    #Setting global var.
    if config == 'set':
        os.system(gl.configFile)

    if start_project !='':
        create_falsework(os.path.join(os.getcwd(), start_project))

    tempList = []
    #Get the yaml file name and write to the queue.
    if case_file != '':
        # case_exec_queue.put(case_file)
        tempList.append(os.path.join(cur_dir, case_file))
        write_file(os.path.join(gl.loadcasePath, 'temp.txt'), 'w', ';'.join(tempList))
        #Began to call.
        Run_Test_Case.invoke()


    if case_dir != '':
        for root, dirs, files in os.walk(case_dir):
            for f in files:
                if 'yaml' in f:
                    # case_exec_queue.put(os.path.join(case_dir, f))
                    d = os.path.join(cur_dir, case_dir)
                    tempList.append(os.path.join(d, f))

        # Write file absolute path to file. 
        write_file(os.path.join(gl.loadcasePath, 'temp.txt'), 'w', ';'.join(tempList))
        #Began to call.
        Run_Test_Case.invoke()



#########################################################################
# Not in command mode --dir defaults to the testcase directory.
# Example:
# python3 main.py --dir=r"D:\test_project\project\cloud_fi_v2\testcase"
#########################################################################

class Run_Test_Case(object):

    @classmethod
    def create_report_file(cls):
        #测试报告文件名
        time_str = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        report_dir = time_str.split('_')[0]
        cls.file_name = 'Report_{}.html'.format(time_str)

        root_dir = os.path.join(os.getcwd(), 'report')
        portdir = os.path.join(root_dir, report_dir)

        #按日期创建测试报告文件夹
        if not os.path.exists(portdir):
            os.makedirs(portdir)

        cls.filePath = os.path.join(portdir, cls.file_name)  # 确定生成报告的路径

        return cls.filePath

    @staticmethod
    def copy_report(filePath, file_name):
        #复制report下子文件夹到 templates/report/下
        split_path = os.path.dirname(filePath).split("\\")
        low_path = split_path[split_path.__len__() - 1]
        web_path = os.path.join(gl.templatesReportPath, low_path)
        if not os.path.exists(web_path):
            shutil.copytree(os.path.dirname(filePath), web_path)
        else:
            shutil.copy(filePath, os.path.join(web_path, file_name))
        return low_path

    @staticmethod
    def tmpl_msg(low_path, file_name):
        # 发送钉钉模版测试结果
        result_str = """共{}个用例, 通过{}, 失败{}, 错误{}, 通过率{}""".format(
            gl.get_value('sum'),
            gl.get_value('passed'),
            gl.get_value('failed'),
            gl.get_value('error'),
            gl.get_value('passrate')
        )

        # 测试结论
        if '100' in str(gl.get_value('passrate')):
            msg_1 = '本次测试★通过★'
        else:
            msg_1 = '本次测试★不通过★'

        #report外网发布地址ip+port
        report_url = get_yaml_field(gl.configFile)['REPORT_URL']

        # 发送钉钉消息
        msg = """接口自动化测试已完成:{},{}\n测试报告地址:{}/report/{}/{}"""
        msg = msg.format(result_str, msg_1, report_url, low_path, file_name)

        return msg

    @staticmethod
    def run(filePath):
        """
        Execute the test and generate the test report file.
        :param filePath: Report file absolute path.
        :return: There is no.
        """
        config  = get_yaml_field(gl.configFile)
        exe_con = config['ENABLE_EXECUTION']
        exe_num = config['EXECUTION_NUM']
        rerun = config['ENABLE_RERUN']
        renum = config['RERUN_NUM']  

        #Enable CPU concurrency
        pyargs = ''  
        if exe_con:
            pyargs = ' -n {} '.format(exe_num)

        #Enable failed retry
        reargs = ''
        if rerun:
            reargs = ' --reruns {} '.format(renum)

        #Load the pytest framework, which must be written here or DDT will be loaded first.
        # from HttpTesting.case import test_load_case
        casePath = gl.loadcasePath
        cmd = 'cd {} && py.test {} {} {}  --html={} --tb=no --self-contained-html'.format(
            casePath, 
            pyargs,
            reargs,
            'test_load_case.py', 
            filePath
        )
        os.system(cmd)


    @staticmethod
    def invoke():
        """
        Start executing tests generate test reports.
        :return: There is no.
        """
        ##########################Read configuration information###############
        config  = get_yaml_field(gl.configFile)
        dd_enable = config['ENABLE_DDING']
        dd_token = config['DD_TOKEN']
        dd_url = config['DING_URL']
        report_service = config['REPORT_SERVICE_ENABLE']
        email_enable = config['EMAIL_ENABLE']
        ########################################################################
        #Enable a test reporting web service.
        _HOST = config['REPORT_HOST']
        _PORT = config['REPORT_PORT']

        #Whether to enable web services.
        if report_service:
            boolRet = scripts.check_http_status(_HOST, _PORT)
            if not boolRet:
                os.system('python {} --host {} --port {}'.format(
                        os.path.join(gl.webPath, 'service.py'),
                        _HOST,
                        _PORT
                    )
                )

        # Test report file name.
        time_str = time.strftime('%Y%m%d_%H%M%S', time.localtime())
        filePath = Run_Test_Case.create_report_file()


        # Start test the send pin message.
        if dd_enable:
            scripts.send_msg_dding(
                '{}:★开始API接口自动化测试★'.format(time_str),  
                dd_url, 
                dd_token
            )

        # Execute the test and send the test report.
        Run_Test_Case.run(filePath)
        
        # Copy the folder under the report directory under  /templates/report/
        low_path = Run_Test_Case.copy_report(filePath, Run_Test_Case.file_name)

        if dd_enable:
            # Template message.
            msg = Run_Test_Case.tmpl_msg(low_path, Run_Test_Case.file_name)
            print(msg)
            scripts.send_msg_dding(msg, dd_url, dd_token)

        if email_enable:
            # Send test report to EMAIL.
            email = EmailClass()
            email.send(filePath)


# if __name__=="__main__":
#     run_min()

