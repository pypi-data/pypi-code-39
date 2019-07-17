# TODO: フィルターの際に時間で指定できるようにする．hostしか時間はわからなそう
# TODO: デフォルトで1つしかターゲットにしないようにする．manyオプションで複数操作できるようにする
# TODO: デバッグモードを追加する．デバッグモードではapiを叩かない
'''
別ファイルに分けるとclickがおかしくなったのでコマンド系は1つのファイルにまとめた
'''
from . import zabbix_controller
from . import utils
from . import hosts
