from requests import Response

from pybacklogpy.modules import RequestSender


class Priority:
    base_path = 'priorities'
    rs = RequestSender()

    def get_priority_list(self) -> Response:
        """
        優先度一覧の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-priority-list/

        :return: レスポンス
        """

        path = self.base_path
        return self.rs.send_get_request(path=path, url_param={})
