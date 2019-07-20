from enum import Enum


class WaimokuSetsueiStatus(Enum):
    """ワイもくのイベント設営をしてくれるかどうか

    Arguments:
        Enum {int} -- 0: 両方手伝えそう, 1: 設営を手伝えそう, 2: 撤収を手伝えそう, 3: もくもくパートだけ全力で楽しみます
    """
    all = "両方手伝えそう"
    setsuei = "設営を手伝えそう"
    tessyu = "撤収を手伝えそう"
    mokumoku = "もくもくパートだけ全力で楽しみます"
