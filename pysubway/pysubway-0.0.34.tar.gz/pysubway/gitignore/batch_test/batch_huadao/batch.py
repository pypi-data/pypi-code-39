try:
    from service.huadao import batch_test
    from utils.file import File
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.service.huadao import batch_test
    from utils.file import File

if __name__ == '__main__':
    HUADAO_TOKEN = '9443C11E5C284240BEFC595B4E43DDD39C5BBE825A52D271844BEEC960922AB78B7C63B5F8D94830B48A3A826F136379'

    # 姓名电话身份证银行卡
    file = f'{File.this_dir(__file__)}/bankcard5eles.xlsx'
    output = f'{File.this_dir(__file__)}/bankcard5eles_result.xlsx'
    # 姓名	身份证号	银行卡号	手机号	账户类型
    batch_test(file,
               output,
               names=('name', 'idcard', 'bankcard', 'phone', 'account_type'),
               raise_failed_exception=True,
               token=HUADAO_TOKEN)
