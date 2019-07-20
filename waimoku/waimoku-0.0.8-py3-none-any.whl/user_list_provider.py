import pandas as pd
from .user import WaimokuUser
from .setsuei_status import WaimokuSetsueiStatus


class WaimokuUserListProvider:
    raw_data: pd.DataFrame

    def fetch(self, file_path: str, encoding: str = "cp932") -> list:
        """指定されたファイルパスに存在するファイルからユーザ一覧を取得する

        Arguments:
            file_path {str} -- ファイルパス

        Keyword Arguments:
            encoding {str} -- ファイルのテキストエンコーディング (default: {"cp932"})

        Returns:
            list -- ユーザ情報一覧
        """
        user_list = []
        self.raw_data = pd.read_csv(file_path, encoding=encoding)
        for data in self.raw_data.itertuples():
            user = WaimokuUser(user_name=data[2],
                               display_name=data[3],
                               full_name=data[7],
                               assign=data[8],
                               is_staff=data[1],
                               join_status=data[5],
                               participation_status=data[6],
                               mokumoku=data[9],
                               is_handagote=data[10],
                               is_survey=data[11],
                               is_setsuei=data[12],
                               is_lt=data[15],
                               latest_update=data[16])
            user_list.append(user)
        return user_list
