# example
import json
import traceback
from typing import Any, Optional, Dict, Callable

import flask
from flask import abort
from flask import request
from flask.views import MethodView
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

try:
    from pysubway.apps.app_batch_test.main import (huzumodel_batch_test,
                                                   send_email_batch_test,
                                                   can_recharge_money_account,
                                                   can_open_company_account,
                                                   get_real_name,
                                                   send_email)
    from pysubway.cache import FlaskCache
    from pysubway.errors import IncomingDataError, RequestFailed, AuthenticationFailed
    from pysubway.model import call_procedure
    from pysubway.model.guard.company import Company
    from pysubway.model.guard.company_product import CompanyProduct
    from pysubway.service.booldata.base import BoolDataBase
    from pysubway.service.booldata.hz_risk_model import HzRiskModel
    from pysubway.utils.file import File
    from pysubway.view import View
    from pysubway.utils.utime import strftime
except (ModuleNotFoundError, ImportError) as e:
    from apps.app_batch_test.main import (huzumodel_batch_test,
                                          send_email_batch_test,
                                          can_recharge_money_account,
                                          can_open_company_account,
                                          get_real_name,
                                          send_email)
    from cache import FlaskCache
    from errors import IncomingDataError, RequestFailed, AuthenticationFailed
    from model import call_procedure
    from model.guard.company import Company
    from model.guard.company_product import CompanyProduct
    from service.booldata.base import BoolDataBase
    from service.booldata.hz_risk_model import HzRiskModel
    from utils.file import File
    from view import View
    from utils.utime import strftime

BOOLDATA_ACCOUNT = dict(
    rsa_prv_key="""-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA3PgggZllwepRByXqAeqrWU4Zx7m+0kvhcbEvpbGTez7PAj8u
IJRKGnH2QfOkZHsRknamuBtJr9c2Js9yrrWbazNPFQrjekprroBSC7DO+EUHQqxZ
mV8ldqukT+C/UOHXavNH3FHnrYSgU7yj4I1+AnAzQq33xbSASE9DkTyoEzJnlRjn
TBopidDVA+P/bxR9z6FBWv8M6P/VAcKamYGIwsx9AbsVhHDd8yOzMDJHOuJza4ku
KFyjf/N+2Fwc7d6ZbKhRYITio7nerw6/XYrcWhAAyB6XhEp3wfCA5SpgCBWGbdve
fiPsme5qqirCy2rlPn76Biev3wW2zhVWTw7HDwIDAQABAoIBABA3vdsFMSy8T9og
dD5TxOO3EblQ7qpsm01G3eJhWBuxjmvxyybk+1NZjeNlSGl/htijELVue0gGmZjb
nOUpuxBxIZq/w9ZT4/dYv6zP+0DJgDDqiWDyVMOS8WpTanc7PB5DYMDQ2hooI8RB
kh2HBPqU1Y5NSmQeTVQBTUo5k3RlGbeAE05U3kVfg6j6xf/67rceCOKa6G+Tkp6h
eebLmuuc19rqg7jBblCsoMgb76P+STlnpvyB8fIYkb1W64bHkX/m4Qj/f4SiDh5t
9W3/bmB+2ygsQCaTPGS9y6z8EfnWZT74Fd+o8XuStubEFw0q+b/BdrmEfL5CjEnO
q57Ep4ECgYEA4/rO82UlKQ6YS0pv4Z7yqPSrJSYwtoazGbGtgp1EHuRk//VEfLOT
4Yo665CbBIrTJxfgZlNkSkBoYaZA8KBg1fP56iuCBUvqBRhSvy94E8dNYjLEjX1q
gskOFrfJ2UaHdp6alctrNSIuWd5q/1LIA4qUBD+mLbnRVWC6dIV2W68CgYEA+CC9
Zw3M1w+5EYWXgq7D6PiDXMjGgvVn+J0/9nDSxVi41zhnxGQD40h/9eNAai67rJHG
xvjK313aUVvMJRSXZuR9Y3zwh1Qb6wUdFgDlGUMuJbazVEgNQDrexf9oCGkvlmPH
/5WDHTOdch07rNaE6/0xnSk45intCIbZy3bEQqECgYACHlWH+3uh6wnNQU7S2OhG
W6eve7BeMdg+N+F14kI8y0CJBF1zjzOjl+Y+RCS8oRGfPmCOct3utrSBm8rksYjU
1CSRYYAeznrJO1Whgy5peKOmcvRSoES6HGYuHd0ZUMd3ebfUBoTjhILLwP5biwhi
yAniFDlWGXDxiymQZaEY7wKBgQC1r6OAdkZro4OsJNoQQtAJIw9tPUa+VdvP27Ue
SvbKsnCGhzLURzfhkRDBh6l/FsEtV4Dp6PsEG8Dkmgcdj7pdCSoXU0D8lsXqjVAC
8JzQprR/wQwGxsuNII5HBQG0RvEleeLUbzIWi9jZ2jX8FQg3lKpjne+f+UsrVzLb
HRgQgQKBgDeMsUFxAeNFN9iHu0IqUboe09ULrZ0NZMHOJ3zoFnuus4sEQpNDC32y
TuzAQumL7z6U5EzzKfdOZX1aAaLoId6+WNjaYkaSD+r/Iz8EzA8V3maip4M2usDl
NLm+JyWqvj9Ze9y7VOgIqRarqjgNwjBoWysNzKIOMpxxItEWUE6b
-----END RSA PRIVATE KEY-----""",
    aes_key='vo8N6ZPawqLDhGj7',
    company_uuid='01b20490-4a1e-11e9-9eb7-247703d210dc',
)

DEV_DB = dict(
    host='47.102.132.18',
    user='root',
    password='qwe123456',
    database='lightning',
)

PROD_DB = dict(
    # open
    host='rm-uf6xfyemz1085v2a48o.mysql.rds.aliyuncs.com',
    # inner
    # host='rm-uf6xfyemz1085v2a4.mysql.rds.aliyuncs.com',
    user='root',
    password='Qwe123456',
    database='lighting',
)

EMAIL_LIST = [
    'booleandatamsg@shouxin168.com',
    'booleandatamsg002@shouxin168.com',
    'booleandatamsg003@shouxin168.com',
    'booleandatamsg004@shouxin168.com',
    'booleandatamsg005@shouxin168.com',
]

EMAIL_PASSWORD = 'Qwe123456_'

# remove mypy hints: error: Value of type "object" is not indexable
DB_CONF: Dict[str, Any] = {
    'SQLALCHEMY_DATABASE_URI':
        f'mysql+pymysql://root:{PROD_DB["password"]}@{PROD_DB["host"]}/{PROD_DB["database"]}?charset=utf8',
    'SQLALCHEMY_BINDS': {
        'guard': f'mysql+pymysql://root:{PROD_DB["password"]}@{PROD_DB["host"]}/{PROD_DB["database"]}?charset=utf8'
    },
}

app = flask.Flask(__name__)
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


def check_operation(can_func: Callable[[str, str], str]) -> Optional[str]:
    stored = get_cache(request.args.get('access_token'))
    if not can_func(stored.get(KEY_USERNAME), CODE_BOOK):
        return abort(403)


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


class RechargeCompany(MethodView):

    @staticmethod
    def send_email_recharge_money(mail_user: str,
                                  mail_pass: str,
                                  account: str = '',
                                  code_book: str = '',
                                  company_name: str = '',
                                  recharged_money: int = 0,
                                  balanced: int = 0,
                                  specified_receivers: str = ''
                                  ) -> None:
        real_name = get_real_name(code_book, account)
        content = f'{company_name} 于 {strftime()} 充值 {recharged_money} 元，' \
            f'该公司当前账户余额为 {balanced}, 充值操作者为 {real_name}.'
        send_email(mail_user, mail_pass, '公司充值邮件提醒', content, code_book, specified_receivers=specified_receivers)

    def post(self):
        company_uuid, money = View.request.get_data('company', 'money')
        print(f'account, money >>>>>> {company_uuid},{money}+++++++++++++++++++')
        check_operation(can_recharge_money_account)
        call_procedure(DB_CONF['SQLALCHEMY_BINDS']['guard'], 'company_recharge_money', company_uuid, money)
        username = CACHE.get(request.args.get('access_token')).get(KEY_USERNAME)
        ins = Company.get_one(uuid=company_uuid)
        self.send_email_recharge_money(EMAIL_LIST[0],
                                       EMAIL_PASSWORD,
                                       account=username,
                                       code_book=CODE_BOOK,
                                       company_name=ins.name,
                                       recharged_money=money,
                                       balanced=ins.balance / 100,
                                       )
        return View.response.success({"msg": "操作成功"})


class OpenCompanyAccount(MethodView):

    def env_test(self, company_name, money, email, comment):
        username = CACHE.get(request.args.get('access_token')).get(KEY_USERNAME)
        ins = Company.get_one(uuid=company_uuid)
        send_email(EMAIL_LIST[0],
                   EMAIL_PASSWORD,
                   account=username,
                   code_book=CODE_BOOK,
                   company_name=ins.name,
                   recharged_money=money,
                   balanced=ins.balance / 100,
                   )
        return View.response.success({"msg": "操作成功"})

    def env_prod(self, company_name: str, money: str, email: str, comment: str):
        pass

    def open_company_account_by_env(self, env: str) -> Optional[Callable]:
        all_envs = {
            'test': self.env_test,
            'prod': self.env_prod,
        }
        return all_envs.get(env, None)

    def post(self):
        env, company_name, money, email, comment = View.request.get_data('env', 'company', 'money', 'email', 'comment')
        check_operation(can_open_company_account)
        operation_func = self.open_company_account_by_env(env)
        if operation_func is None:
            # resp code is SW0300
            return View.response.incoming_data_error()
        else:
            return operation_func(company_name, money, email, comment)


app.add_url_rule('/open/company_account', view_func=OpenCompanyAccount.as_view('open_company_account'))
app.add_url_rule('/recharge/company', view_func=RechargeCompany.as_view('recharge_company'))

if __name__ == '__main__':
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    app.run(port=8888, host='0.0.0.0', debug=False, use_reloader=True, processes=True)
