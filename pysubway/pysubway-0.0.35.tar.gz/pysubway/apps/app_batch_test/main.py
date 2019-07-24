import traceback
from functools import partial
from typing import Dict, Tuple

from flask import Flask

try:
    from errors import IncomingDataError, AuthenticationFailed
    from errors import RequestFailed
    from service.booldata.hz_risk_model import batch_test
    from utils.file import File
    from utils.uexcel import Excel
    from utils.ustring import is_invalid_str
    from utils.ustring import unique_id
    from view import View
    from cache import FlaskCache
    from service.aliyun.uemail import Email
    from utils.file import FileIni
    from utils.utime import strftime
except (NotImplementedError, ImportError) as e:
    from pysubway.errors import IncomingDataError, AuthenticationFailed
    from pysubway.errors import RequestFailed
    from pysubway.service.booldata.hz_risk_model import batch_test
    from pysubway.utils.file import File
    from pysubway.utils.uexcel import Excel
    from pysubway.utils.ustring import is_invalid_str
    from pysubway.utils.ustring import unique_id
    from pysubway.view import View
    from pysubway.service.aliyun.uemail import Email
    from pysubway.utils.file import FileIni
    from pysubway.utils.utime import strftime

THIS_DIR = File.this_dir(__file__)
CODE_BOOK = f'{File.this_dir(__file__)}/static/code_book.ini'


def huzumodel_batch_test(account_info: Dict[str, str],
                         env: str,
                         company_uuid: str,
                         biz_data: str,
                         output: str = File.join_path(THIS_DIR, f'{unique_id()}.xlsx'),
                         raise_failed_exception: bool = True,
                         ) -> Tuple[str, str]:
    if is_invalid_str(biz_data):
        raise IncomingDataError('提交数据有误')
    excel_ins = Excel.prepare_file(biz_data).read()
    account = account_info.copy()
    account['company_uuid'] = company_uuid
    error_log = File.join_path(THIS_DIR, 'log', File(output).pure_name)
    output_file = batch_test(excel_ins.dataframe, account,
                             output, names=tuple(excel_ins.header), error_log=error_log,
                             raise_failed_exception=raise_failed_exception,
                             env=env)
    return View.response.send_file(output_file, as_attachment=True, attachment_filename='batch_test.xlsx'), output_file


def generate_app() -> Flask:
    return Flask(__name__)


def get_real_name(code_book: str, account: str, section: str = 'account_username') -> str:
    real_name = FileIni(code_book).get(section, account, 'unknown')
    return real_name


def send_email(mail_user: str,
               mail_pass: str,
               title='',
               content: str = '',
               code_book: str = '',
               default_receivers_option: str = 'default',
               specified_receivers: str = '') -> None:
    try:
        receivers = Email.update_receiver(FileIni(code_book).get('email_notification',
                                                                 default_receivers_option,
                                                                 'unknown'), specified_receivers)
        Email(mail_user, mail_pass).send_email(title, content, receivers)
    except Exception as e:
        traceback.print_exc()


def send_email_batch_test(account: str = '',
                          remarks: str = '',
                          mail_user: str = '',
                          mail_pass: str = '',
                          filename: str = '',
                          specified_receivers: str = '',
                          code_book: str = '') -> None:
    try:
        real_name = get_real_name(code_book, account)
        content = f'申请者: {real_name}\n测试理由：{remarks}' if remarks else ''
        receivers = Email.update_receiver(FileIni(code_book).get('email_notification', 'batch_test', 'unknown'),
                                          specified_receivers)
        Email(mail_user, mail_pass).send_email_attach('布尔数据个人信用查询测试申请', content, filename, receivers)
    except Exception as e:
        traceback.print_exc()


def _can_do(option: str, code_book: str, section: str) -> bool:
    return FileIni(code_book).get(section, option, '') == ''


can_recharge_money_account = partial(_can_do, section='recharge_money_account')
can_open_company_account = partial(_can_do, section='open_company_account')
