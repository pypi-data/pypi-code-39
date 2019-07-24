from service.huadao import HuaDaoBase

s = HuaDaoBase.get_token(HUADAO_ACCOUNT['AppID'], HUADAO_ACCOUNT['AppSecret'], HUADAO_ACCOUNT['Key'])
print(s)