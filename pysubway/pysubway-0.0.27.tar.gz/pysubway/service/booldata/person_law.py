from typing import Dict, Optional, Tuple

import pandas as pd

try:
    from service.booldata.base import BoolDataBase
    from utils import udict
    from utils.uexcel import Excel
except (ImportError, ModuleNotFoundError) as e:
    from pysubway.service.booldata.base import BoolDataBase
    from pysubway.utils import udict


class LawList(BoolDataBase):
    service = 'personal_law_info'
    mode = 'mode_personal_law_info'
    default_part = [{
        "compatibility": '',
        "content": "",
        "data_id": "",
        "data_type": "",
        "sort_time": 0,
        "sort_time_string": "",
        "title": ""
    }]
    df_default_header = (
        "name",
        "phone",
        "ident_number",
        "compatibility",
        "content",
        "data_id",
        "data_type",
        "sort_time",
        "sort_time_string",
        "title"
    )

    @classmethod
    def generate_biz_data(cls, name: str, phone: str, ident_number: str) -> Dict[str, str]:
        biz_data = udict.Dict.filter(locals())
        biz_data.update({
            "service": cls.service,
            "mode": cls.mode
        })
        return biz_data

    def set_biz_data(self, name: str, phone: str, ident_number: str) -> 'LawList':
        self.biz_data = self.generate_biz_data(name, phone, ident_number)
        return self

    def result_as_df_partial(self, append_biz_data: bool = True) -> pd.DataFrame:
        return self.result_as_df(self.response.get('resp_data', {}).get('data_list'), self.default_part,
                                 append_biz_data=append_biz_data)


def batch_test(input: str,
               account: Dict[str, str],
               output_file: str,
               names: Optional[Tuple[str, ...]] = ('name', 'idcard', 'phone'),
               columns: Tuple[str, ...] = LawList.df_default_header) -> None:
    """
    batch test personal law, read from excel -> request personal law -> save result to excel

    :param input: excel file
    :param account: booldata account
    :param output_file: xlsx file that saving booldata personal law result
    :param names: input excel file header, you can adjust the sequence
    :param columns: output_file columns header
    :return: None
    """
    excel_ins = Excel(input).read(names=names)
    result_df = pd.DataFrame()
    law_list = LawList(account['rsa_prv_key'], account['aes_key'], account['company_uuid'])
    for _, series in excel_ins.dataframe.iterrows():
        name = series['name']
        phone = series['phone']
        idcard = series['idcard']
        law_list.set_biz_data(name, phone, idcard).request()
        result_law_list = law_list.result_as_df_partial()
        result_df = result_df.append(result_law_list)
        print(f'{name} {phone} {idcard} result_df', result_df)
    result_df.to_excel(output_file, columns=columns, index=False)


if __name__ == '__main__':
    from gitignore import BOOLDATA_ACCOUNT

    file = ''
    output = ''
    batch_test(file, BOOLDATA_ACCOUNT, output)
