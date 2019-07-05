# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/5/30
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from .person.face.face_detect import open_face_detector, close_face_detector, get_faces_detected
from .person.face.face_recog import open_face_recognizer, close_face_recognizer, get_faces_recognized
from .person.face.face_register import face_register
from .person.age_gender.age_gender_recog import open_age_gender_recognizer
from .person.age_gender.age_gender_recog import close_age_gender_recognizer, get_age_genders_recognized
from .person.beauty.beauty_recog import open_beauty_age_gender_recognizer
from .person.beauty.beauty_recog import close_beauty_age_gender_recognizer, get_beauty_age_genders_recognized
from .person.emotion.emotion_recog import open_emotion_recognizer
from .person.emotion.emotion_recog import close_emotion_recognizer, get_emotions_recognized
from .person.handpose.handpose_recog import open_handpose_recognizer
from .person.handpose.handpose_recog import close_handpose_recognizer, get_handposes_recognized
from .person.headpose.headpose_recog import open_headpose_recognizer
from .person.headpose.headpose_recog import close_headpose_recognizer, get_headpose_recognized
from .person.skeleton.skeleton_recog import open_skeleton_recognizer
from .person.skeleton.skeleton_recog import close_skeleton_recognizer, get_skeletons_recognized
from .object.color.color_recog import open_single_color_recognizer, open_multi_color_recognizer
from .object.color.color_recog import close_color_recognizer, get_colors_recognized
from .object.distance.distance_detect import open_distance_detector, close_distance_detector, get_distance_detected
from .object.object.object_detect import open_object_detector, close_object_detector, get_objects_detected
