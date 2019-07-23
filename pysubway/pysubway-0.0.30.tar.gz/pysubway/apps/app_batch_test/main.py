import json
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
                         ) -> Tuple[str, str]:
    if is_invalid_str(biz_data):
        raise IncomingDataError('提交数据有误')
    excel_ins = Excel.prepare_file(biz_data).read()
    account = account_info.copy()
    account['company_uuid'] = company_uuid
    error_log = File.join_path(THIS_DIR, 'log', File(output).pure_name)
    output_file = batch_test(excel_ins.dataframe, account,
                             output, names=tuple(excel_ins.header), error_log=error_log,
                             raise_failed_exception=True,
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


if __name__ == '__main__':
    # example
    from typing import Any, Optional
    import flask
    from gitignore import BOOLDATA_ACCOUNT, EMAIL_LIST, EMAIL_PASSWORD
    from gitignore import PROD_DB
    from flask_cors import CORS
    from cache import FlaskCache
    from flask import request
    from flask import abort
    from service.booldata.base import BoolDataBase
    from model.guard.company_product import CompanyProduct
    from model.guard.company import Company
    from service.booldata.hz_risk_model import HzRiskModel
    from flask_sqlalchemy import SQLAlchemy
    from model import call_procedure

    # remove mypy hints: error: Value of type "object" is not indexable
    DB_CONF: Dict[str, Any] = {
        'SQLALCHEMY_DATABASE_URI':
            f'mysql+pymysql://root:{PROD_DB["password"]}@{PROD_DB["host"]}/{PROD_DB["database"]}?charset=utf8',
        'SQLALCHEMY_BINDS': {
            'guard': f'mysql+pymysql://root:{PROD_DB["password"]}@{PROD_DB["host"]}/{PROD_DB["database"]}?charset=utf8'
        },
    }

    app = generate_app()
    CACHE = FlaskCache(app)
    app.config.from_mapping(DB_CONF)
    SQLAlchemy().init_app(app)
    HASH_SALT = 'sdaer3rf'
    KEY_USERNAME = 'userName'
    KEY_PASSWORD = 'password'
    CODE_BOOK = f'{File.this_dir(__file__)}/static/code_book.ini'


    def set_cache(key: str, val: Any) -> None:
        CACHE.set(key, val)


    def get_cache(key: Any) -> Any:
        return CACHE.get(key)


    @app.before_request
    def verify_token() -> Optional[flask.Response]:
        """
        :key cache key is access_token
        :return:
        """
        if request.path not in ('/login/'):
            stored = get_cache(request.args.get('access_token'))
            # debug: options is like a ping of chrome browser.
            if not stored and request.method != 'OPTIONS':
                return abort(401)
        return None


    # this part will catch all exception including abort exception
    # @app.errorhandler(Exception)
    # def handle_exception(e):
    #     print(e)
    #     return abort(500)

    @app.route("/batch-test-huizu/", methods=['POST'])
    def batch_test_huizu() -> str:
        try:
            company_uuid = CACHE.get(request.args.get('access_token')).get(KEY_PASSWORD)
            if not CompanyProduct.has_permission_for_product(company_uuid, HzRiskModel.service, HzRiskModel.mode):
                raise IncomingDataError(f'company_uuid {company_uuid} do not has_permission_for_product')
            biz_data, product, remarks, specified_receivers = View.request.get_data('biz_data',
                                                                                    'product',
                                                                                    'remarks',
                                                                                    'email')
            print('biz_data, product, remarks', biz_data, product, remarks)
            result, output_file = huzumodel_batch_test(BOOLDATA_ACCOUNT,
                                                       env='prod',
                                                       company_uuid=company_uuid,
                                                       biz_data=biz_data)
            # send email
            account = CACHE.get(request.args.get('access_token')).get(KEY_USERNAME)
            send_email_batch_test(account=account,
                                  remarks=remarks,
                                  mail_user=EMAIL_LIST[0],
                                  mail_pass=EMAIL_PASSWORD,
                                  filename=output_file,
                                  code_book=CODE_BOOK)
            send_email_batch_test(account=account,
                                  remarks='',
                                  mail_user=EMAIL_LIST[0],
                                  mail_pass=EMAIL_PASSWORD,
                                  filename=output_file,
                                  specified_receivers=specified_receivers,
                                  code_book=CODE_BOOK)
            return result
        except IncomingDataError as e:
            traceback.print_exc()
            return abort(403)
        except RequestFailed as e:
            traceback.print_exc()

            def parse_error(e: Exception) -> object:
                return json.loads(str(e))

            error = parse_error(e)
            if isinstance(error, dict) and error.get('resp_code') in BoolDataBase.resp_code_biz_data_error:
                return abort(403)
            else:
                return abort(500)
        except Exception as e:
            traceback.print_exc()
            return abort(500)


    @app.route('/login', methods=['POST'])
    def login() -> flask.Response:
        account, password = View.request.get_data(KEY_USERNAME, KEY_PASSWORD)
        token = FlaskCache.generate_token(account + password, HASH_SALT)
        set_cache(token, {KEY_USERNAME: account, KEY_PASSWORD: password})
        try:
            return View.login(KEY_USERNAME,
                              KEY_PASSWORD,
                              View.response.login_succeed(token),
                              is_aborted=True,
                              code_book=CODE_BOOK,
                              section='accounts_authentication')
        except AuthenticationFailed:
            CACHE.delete(token)
            return View.response.login_fail()
        except Exception as e:
            traceback.print_exc()
            CACHE.delete(token)
            return abort(500)


    @app.route('/companies', methods=['get'])
    def display_companies() -> flask.Response:
        return View.response.success({ins.uuid: ins.name for ins in Company.get_all()})


    @app.route('/recharge/company', methods=['post'])
    def recharge_company() -> flask.Response:
        company_uuid, money = View.request.get_data('company', 'money')
        print(f'account, money >>>>>> {company_uuid},{money}+++++++++++++++++++')
        stored = get_cache(request.args.get('access_token'))
        if not can_recharge_money_account(stored.get(KEY_USERNAME), CODE_BOOK):
            return abort(403)
        call_procedure(DB_CONF['SQLALCHEMY_BINDS']['guard'], 'company_recharge_money', company_uuid, money)
        username = CACHE.get(request.args.get('access_token')).get(KEY_USERNAME)
        ins = Company.get_one(uuid=company_uuid)
        send_email_recharge_money(EMAIL_LIST[0],
                                  EMAIL_PASSWORD,
                                  account=username,
                                  code_book=CODE_BOOK,
                                  company_name=ins.name,
                                  recharged_money=money,
                                  balanced=ins.balance / 100,
                                  )
        return View.response.success({"msg": "操作成功"})


    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    app.run(port=8888, debug=True, use_reloader=True, processes=True)
