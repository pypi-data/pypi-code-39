from requests import Response

from pybacklogpy.modules import RequestSender


class Status:
    def __init__(self):
        self.base_path = 'statuses'
        self.rs = RequestSender()

    def get_status_list(self) -> Response:
        """
        状態一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-status-list/

        :return: レスポンス
        """

        path = self.base_path
        return self.rs.send_get_request(path=path, url_param={})
