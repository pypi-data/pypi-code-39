from datetime import datetime
from .setsuei_status import WaimokuSetsueiStatus


class WaimokuUser:
    """ワイもくのユーザ情報
    """

    user_name: str
    display_name: str
    full_name: str
    assign: str
    is_yahoo: bool
    is_staff: bool
    join_status: bool
    participation_status: bool
    mokumoku: str
    is_handagote: bool
    is_enquete: bool
    is_setsuei: WaimokuSetsueiStatus
    is_lt: bool
    latest_update: datetime

    def __init__(self,
                 user_name: str,
                 display_name: str,
                 full_name: str,
                 assign: str,
                 is_staff: str,
                 join_status: str,
                 participation_status: str,
                 mokumoku: str,
                 is_handagote: str,
                 is_survey: str,
                 is_setsuei: WaimokuSetsueiStatus,
                 is_lt: str,
                 latest_update: str):
        """イニシャライザ

        Arguments:
            user_name {str} -- ユーザ名
            display_name {str} -- 表示名
            full_name {str} -- 名前
            assign {str} -- 所属
            is_staff {str} -- 運営枠かどうか
            join_status {bool} -- 参加ステータス
            participation_status {bool} -- 出席ステータス
            mokumoku {str} -- 本日のもくもく内容
            is_handagote {bool} -- はんだごてを利用するかどうか
            is_survey {bool} -- アンケートに同意したかどうか
            is_setsuei {WaimokuSetsueiStatus} -- 設営に協力するかどうか
            is_lt {bool} -- LTをするかどうか
            latest_update {str} -- 最終更新日時
        """
        self.user_name = user_name
        self.display_name = display_name
        self.full_name = full_name
        self.assign = assign
        self.is_yahoo = WaimokuUser.__is_yahoo(assign=assign)
        self.is_staff = WaimokuUser.__is_staff(is_staff=is_staff)
        self.join_status = WaimokuUser.__join_status(join_status=join_status)
        self.participation_status = WaimokuUser.__participation_status(participation_status=participation_status)
        self.mokumoku = mokumoku
        self.is_handagote = WaimokuUser.__is_handagote(is_handagote=is_handagote)
        self.is_survey = WaimokuUser.__is_survey(is_survey=is_survey)
        self.is_setsuei = WaimokuUser.__is_setsuei(is_setsuei=is_setsuei)
        self.is_lt = WaimokuUser.__is_lt(is_lt=is_lt)
        self.latest_update = WaimokuUser.__latest_update(latest_update=latest_update)

    @classmethod
    def __is_staff(cls, is_staff: str) -> bool:
        return is_staff == "運営枠（各団体の代表）"

    @classmethod
    def __is_yahoo(cls, assign: str) -> bool:
        return assign == "ヤフー株式会社" or assign == "ヤフー" or assign == "Yahoo! JAPAN" or assign == "Yahoo Japan Corporation" or assign == "Yahoo Japan Corporation." or assign == "yahoo" or assign == "yahoo japan"

    @classmethod
    def __join_status(cls, join_status: str) -> bool:
        return join_status == "参加"

    @classmethod
    def __participation_status(cls, participation_status: str) -> bool:
        return participation_status == "出席"

    @classmethod
    def __is_handagote(cls, is_handagote: str) -> bool:
        return is_handagote == "はい"

    @classmethod
    def __is_survey(cls, is_survey: str) -> bool:
        return is_survey == "理解しました"

    @classmethod
    def __is_setsuei(cls, is_setsuei: str) -> WaimokuSetsueiStatus:
        if is_setsuei == "両方手伝えそう":
            return WaimokuSetsueiStatus.all
        elif is_setsuei == "設営を手伝えそう":
            return WaimokuSetsueiStatus.setsuei
        elif is_setsuei == "撤収を手伝えそう":
            return WaimokuSetsueiStatus.tessyu
        else:
            return WaimokuSetsueiStatus.mokumoku

    @classmethod
    def __is_lt(cls, is_lt: str) -> bool:
        return is_lt == "します"

    @classmethod
    def __latest_update(cls, latest_update: str) -> datetime:
        return datetime.strptime(latest_update+"00秒", "%Y年%m月%d日 %H時%M分%S秒")
