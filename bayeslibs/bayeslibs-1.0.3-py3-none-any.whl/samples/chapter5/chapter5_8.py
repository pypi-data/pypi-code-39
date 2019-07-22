# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/7/18
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from bayeslibs.voice import start_small_talk, start_speak, get_speak_status


def voice_play(text):
    """
       输入任意内容，让APOLLO机器人将其播放出来，实现语音合成功能
    """
    start_res = start_speak(text)
    if start_res and start_res['status'] == 0:
        res = get_speak_status()
        print('小贝语音合成中.......')
        print('------------------------------------')
        while res['status'] == 0:
            res = get_speak_status()
        return True
    else:
        return False


class ApolloIdiom:
    """
        手动输入成语，语音播报APOLLO成语接龙的结果
    """

    def __init__(self):
        self.exit()
        self.status = False

    def idiom_input(self, idiom):
        idiom = idiom.strip()
        if self.status:
            return self.idiom_output(idiom)
        else:
            idiom = '成语接龙{}'.format(idiom)
            return self.idiom_output(idiom)

    def idiom_output(self, idiom):
        result = start_small_talk(idiom)
        if result['status'] == 0:
            answer = result['answer']
            if "退出成语接龙模式" in answer:
                self.status = False
                answer = '你接错了，请重新输入成语'
            if "进入成语接龙模式" in answer:
                self.status = True
                answer = answer.split('：')[-1]
                if self.status and answer[0] != idiom[-1]:
                    answer = '你成语写错了，我给你出个成语：{}'.format(answer)
        else:
            answer = '你接错了，请重新输入成语'
        print('小贝的回答:{}'.format(answer))
        print('------------------------------------')
        return answer

    def exit(self):
        start_small_talk('退出成语接龙')
        self.status = False


if __name__ == '__main__':
    count_ = 0
    # 初始化成语接龙实例
    apollo_idiom = ApolloIdiom()
    # 循环成语接龙10次，次数可修改
    while count_ < 10:
        question_ = input('请输入您的成语:')
        print('------------------------------------')
        answer_ = apollo_idiom.idiom_input(question_)
        voice_play(answer_)
        count_ += 1
