from requests import Response

from pybacklogpy.modules import RequestSender


class Licence:
    def __init__(self):
        self.rs = RequestSender()

    def get_licence(self,
                    ) -> Response:
        """
        ライセンス情報の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-licence/


        :return: レスポンス
        """

        path = 'space/licence'

        return self.rs.send_get_request(path=path, url_param={})
