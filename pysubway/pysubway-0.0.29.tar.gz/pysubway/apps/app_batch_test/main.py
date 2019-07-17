import traceback
from typing import List, Dict

import pandas as pd

try:
    from errors import IncomingDataError
    from errors import RequestFailed
    from service.booldata.hz_risk_model import batch_test
    from utils.file import File
    from utils.uexcel import Excel
    from utils.ustring import is_invalid_str
    from utils.ustring import unique_id
    from view import View
except (NotImplementedError, ImportError) as e:
    from pysubway.errors import IncomingDataError
    from pysubway.errors import RequestFailed
    from pysubway.service.booldata.hz_risk_model import batch_test
    from pysubway.utils.file import File
    from pysubway.utils.uexcel import Excel
    from pysubway.utils.ustring import is_invalid_str
    from pysubway.utils.ustring import unique_id
    from pysubway.view import View

THIS_DIR = File.this_dir(__file__)


def batch_huzumodel(input: pd.DataFrame, header: List[str], company_uuid: str, account_info: Dict[str, str],
                    env: str) -> str:
    output = File.join_path(THIS_DIR, f'{unique_id()}.xlsx')
    account = account_info.copy()
    account['company_uuid'] = company_uuid
    print(f'input: pd.DataFrame {input}, output: str {output}, header: List[str] {header}, passwd: str {company_uuid}')
    error_log = File.join_path(THIS_DIR, 'log', File(output).pure_name)
    batch_test(input, account, output, names=tuple(header), error_log=error_log, raise_failed_exception=True, env=env)
    return output


def view_batch_huzumodel(code_book_path: str, default_section: str, account_info: Dict[str, str], env: str) -> str:
    try:
        account, passwd, biz_data = View.request_form('account', 'passwd', 'biz_data')
        if is_invalid_str(account, passwd, biz_data):
            raise IncomingDataError('提交数据有误')
        is_authenticated = View.authenticate('file',
                                             code_book_path=code_book_path,
                                             default_section=default_section)(account, passwd)
        if not is_authenticated:
            raise IncomingDataError('账号或密码错误')
        excel_ins = Excel.prepare_file(biz_data).read()
        headers = excel_ins.header
        output_file = batch_huzumodel(excel_ins.dataframe, headers, passwd, account_info, env)
        return View.resp_file(output_file)
    except IncomingDataError as e:
        return View.resp_template('down_file.html', msg=str(e))
    except RequestFailed as e:
        return View.resp_template('down_file.html', msg=str(e))
    except Exception as e:
        traceback.print_exc()
        return View.resp_template('down_file.html', msg='未知错误, 请联系管理员.')


def generate_app():
    return View.new_app_this_dir(File.join_path(File.this_dir(__file__), 'templates'))


if __name__ == '__main__':
    # example
    from gitignore import BOOLDATA_ACCOUNT

    app = View.new_app_this_dir(THIS_DIR)


    @app.route('/')
    def index() -> str:
        return View.resp_template('index.html')


    @app.route("/batch-test-huizu/", methods=['POST'])
    def batch_test_huizu() -> str:
        code_book = f'{File.this_dir(__file__)}/static/code_book.ini'
        section = 'huizumodel'
        env = 'prod'
        print('it running batch_test_huizu')
        return view_batch_huzumodel(code_book, section, BOOLDATA_ACCOUNT, env)


    app.run(port=8000, debug=False, processes=True)
