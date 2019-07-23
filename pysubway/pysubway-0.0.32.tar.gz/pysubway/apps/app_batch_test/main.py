import traceback
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
                         raise_failed_exception: bool = False,
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
        receivers = specified_receivers if specified_receivers else FileIni(code_book). \
            get('email_notification', 'batch_test', 'unknown')
        Email(mail_user, mail_pass).send_email_attach('布尔数据个人信用查询测试申请', content, filename, receivers)
    except Exception as e:
        traceback.print_exc()


def send_email_recharge_money(mail_user: str,
                              mail_pass: str,
                              account: str = '',
                              code_book: str = '',
                              company_name: str = '',
                              recharged_money: int = 0,
                              balanced: int = 0,
                              specified_receivers: str = ''
                              ) -> None:
    try:
        real_name = get_real_name(code_book, account)
        content = f'{company_name} 于 {strftime()} 充值 {recharged_money} 元，' \
            f'该公司当前账户余额为 {balanced}, 充值操作者为 {real_name}.'
        receivers = specified_receivers if specified_receivers else FileIni(code_book). \
            get('email_notification', 'recharge_money', 'unknown')
        Email(mail_user, mail_pass).send_email('公司充值邮件提醒', content, receivers)
    except Exception as e:
        traceback.print_exc()


def can_recharge_money_account(account: str,
                               code_book: str,
                               section: str = 'recharge_money_account') -> bool:
    password = FileIni(code_book).get(section, account, '')
    return password != ''
