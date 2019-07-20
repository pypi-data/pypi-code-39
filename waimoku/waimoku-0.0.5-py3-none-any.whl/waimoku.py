from .user import WaimokuUser
from .user_list_provider import WaimokuUserListProvider
from .client import WaimokuClient


class Waimoku:
    """ワイもくの参加者情報を操作するためのクラス

    """

    __user_list_provider: WaimokuUserListProvider
    __client: WaimokuClient

    def __init__(self, *args, **kwargs):
        self.__user_list_provider = WaimokuUserListProvider()
        self.__client = WaimokuClient()
        return super().__init__(*args, **kwargs)

    def fetch_users(self, file_path: str) -> [WaimokuUser]:
        """Connpassの参加者一覧CSVファイルからユーザ一覧を取得する処理

        Arguments:
            file_path {str} -- ConnpassのCSVファイルが存在するパス

        Returns:
            [WaimokuUser] -- ワイもくのユーザ情報一覧
        """
        return self.__user_list_provider.fetch(file_path=file_path)

    def save_to_file_from_csv_file(self, file_path: str, save_filename: str):
        """Connpassの参加者一覧CSVファイルからLODGE提出用のXLSファイルに変換して保存する

        Arguments:
            file_path {str} -- ConnpassのCSVファイルが存在するパス
            save_filename {str} -- LODGE提出用のXLSファイル
        """
        user_list = self.fetch_users(file_path=file_path)
        self.save_to_file_from_user_list(user_list=user_list, save_filename=save_filename)

    def save_to_file_from_user_list(self, user_list: [WaimokuUser], save_filename: str):
        """ワイもくのユーザ情報一覧をLODGE提出用のXLSファイルに変換して保存する

        Arguments:
            user_list {[WaimokuUser]} -- ワイもくのユーザ情報一覧
            save_filename {str} -- LODGE提出用のXLSファイル
        """
        is_yahoo_count = 0
        is_staff_count = 0
        participation_list: [WaimokuUser] = []
        for user in user_list:
            if user.participation_status:
                participation_list.append(user)
                if user.is_yahoo:
                    is_yahoo_count = is_yahoo_count + 1
                if user.is_staff:
                    is_staff_count = is_staff_count + 1
        self.__client.save_to_file(user_list=participation_list, save_filename=save_filename)
        print("")
        print("=== ヤフー社員合計 ===")
        print("ヤフ-社員: " + str(is_yahoo_count) + "名")
        print("")
        print("=== " + "参加者" + str(len(participation_list)) + "名の内訳（この中にはヤフー社員も含めます）" + " ===")
        print("運営: " + str(is_staff_count) + "名")
        print("一般: " + str(len(participation_list) - is_staff_count) + "名")
