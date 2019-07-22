# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/5/30
@author:qianyang<qianyang@aibayes.com>
@description:none
"""


class BayesLibsConfig:
    def __init__(self, ip, port, user_id=None, password=None):
        self.ip = ip
        self.port = port
        self.user_id = user_id
        self.password = password

    def connect(self):
        from bayeslibs.voice.chat.small_talk import ApolloChatter
        from bayeslibs.config.setting import ApolloConfig
        apollo = ApolloConfig()
        apollo.set_apollo_url(self.ip, self.port)
        chatter = ApolloChatter()
        res = chatter.start('连接成功')
        if res and res['status'] == 0:
            flag = True
            print('connect success, apollo ip:{}'.format(apollo.get_apollo_url()))
        else:
            flag = False
            print('connect failed, please reset apollo\'s ip')
        return flag


def add_slam_pos(dest, x, y):
    """
        设置室内导航目标地点的坐标位置
        :param dest: 目标地点描述，英文
        :param x: RVIZ点x坐标
        :param y: RVIZ点y坐标
        :return:
    """
    from bayeslibs.config.setting import ApolloConfig
    apollo = ApolloConfig()
    apollo.set_nav_pos(dest, x, y)


def get_slam_pos():
    from bayeslibs.config.setting import ApolloConfig
    apollo = ApolloConfig()
    return apollo.get_nav_pos_map()


__all__ = ['BayesLibsConfig', 'add_slam_pos', 'get_slam_pos']
