from requests import Response
from typing import List, Optional

from pybacklogpy.modules import RequestSender


class Space:
    def __init__(self):
        self.base_path = 'space'
        self.rs = RequestSender()

    def get_space(self) -> Response:
        """
        スペース情報の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-space/

        :return: レスポンス
        """
        path = self.base_path
        return self.rs.send_get_request(path=path, url_param={})

    def get_recent_updates(self,
                           activity_type_id: Optional[List[int]] = None,
                           min_id: Optional[int] = None,
                           max_id: Optional[int] = None,
                           count: Optional[int] = 20,
                           order: Optional[str] = 'desc',
                           update_type: Optional[int] = None) -> Response:
        """
        最近の更新の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-recent-updates/

        :param activity_type_id: type(1-26)
        :param min_id: 最小ID
        :param max_id: 最大ID
        :param count: 取得上限(1-100) 指定が無い場合は20
        :param order: “asc”または”desc” 指定が無い場合は”desc”
        :param update_type: 最近の更新の種別：(1)課題の追加 (2)課題の更新 (3)課題にコメント (4)課題の削除 (5)Wikiを追加 (6)Wikiを更新 (7)Wikiを削除 (8)共有ファイルを追加 (9)共有ファイルを更新(10)共有ファイルを削除 (11)Subversionコミット (12)GITプッシュ (13)GITリポジトリ作成 (14)課題をまとめて更新 (15)ユーザーがプロジェクトに参加 (16)ユーザーがプロジェクトから脱退 (17)コメントにお知らせを追加 (18)プルリクエストの追加 (19)プルリクエストの更新 (20)プルリクエストにコメント (21)プルリクエストの削除 (22)マイルストーンの追加 (23)マイルストーンの更新 (24)マイルストーンの削除 (25)グループがプロジェクトに参加 (26)グループがプロジェクトから脱退

        :return: レスポンス
        """

        path = self.base_path + '/activities'
        payloads = {}
        if activity_type_id is not None:
            payloads['activityTypeId[]'] = activity_type_id
        if min_id is not None:
            payloads['minId'] = min_id
        if max_id is not None:
            payloads['maxId'] = max_id
        if count is not None:
            if not 1 <= count <= 100:
                raise ValueError('count(取得上限)は1-100の範囲で指定してください')
        if order is not None:
            if order not in {'desc', 'asc'}:
                raise ValueError('order は desc または asc のみが使用できます')
            payloads['order'] = order
        if update_type is not None:
            payloads['type'] = update_type

        return self.rs.send_get_request(path=path, url_param=payloads)

    def get_space_logo(self) -> Response:
        """
        スペースアイコン画像の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-space-logo/

        :return: レスポンス
        """

        path = self.base_path + '/image'

        return self.rs.send_get_request(path=path, url_param={})

    def get_space_notification(self) -> Response:
        """
        スペースのお知らせの取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-space-notification/

        :return: レスポンス
        """

        path = self.base_path + '/notification'

        return self.rs.send_get_request(path=path, url_param={})

    def update_space_notification(self) -> Response:
        """
        スペースのお知らせの更新
        https://developer.nulab.com/ja/docs/backlog/api/2/update-space-notification/

        :return: レスポンス
        """

        path = self.base_path + '/notification '

        return self.rs.send_patch_request(path=path, request_param={})

    def get_space_disk_usage(self) -> Response:
        """
        スペースの容量使用状況の取得
        https://developer.nulab.com/ja/docs/backlog/api/2/get-space-disk-usage/

        :return: レスポンス
        """

        path = self.base_path + '/diskUsage'

        return self.rs.send_get_request(path=path, url_param={})
