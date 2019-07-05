# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
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


def apollo_chat_sample(question):
    """
    语音输入自己想说的话，观察APOLLO的自然语言处理结果
    """
    result = start_small_talk(question)
    if result['status'] == 0:
        answer = result['answer']
        print('小贝的回答:{}'.format(answer))
    else:
        print('小贝还小，还有很多需要学习')
        answer = '小贝还小，还有很多需要学习'
    print('------------------------------------')
    return answer


if __name__ == '__main__':
    count_ = 0
    # 循环聊天10次，次数可修改
    while count_ < 10:
        question_ = input('请输入您的问题:')
        print('------------------------------------')
        answer_ = apollo_chat_sample(question=question_)
        voice_play(answer_)
        count_ += 1
