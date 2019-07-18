from keras.applications import (
    densenet, inception_v3, mobilenetv2, nasnet,
    resnet50, xception,
)
from keras.utils import multi_gpu_model
from ....lib.config_lib import ImageClassificationConfig


def image_classification_model(num_classes, gpu_num, model_type):
    if model_type == 'resnet50':
        model = resnet50.ResNet50(weights=None, classes=num_classes,
                                  input_shape=ImageClassificationConfig.INPUT_SHAPE)
    elif model_type == 'inception_v3':
        model = inception_v3.InceptionV3(weights=None, classes=num_classes,
                                         input_shape=ImageClassificationConfig.INPUT_SHAPE)
    elif model_type == 'inception_resnet_v2':
        model = inception_v3.InceptionV3(weights=None, classes=num_classes,
                                         input_shape=ImageClassificationConfig.INPUT_SHAPE)
    elif model_type == 'mobilenet_v2':
        model = mobilenetv2.MobileNetV2(weights=None, classes=num_classes,
                                        input_shape=ImageClassificationConfig.INPUT_SHAPE)
    elif model_type == 'nasnet_large':
        model = nasnet.NASNetLarge(weights=None, classes=num_classes,
                                   input_shape=ImageClassificationConfig.INPUT_SHAPE)
    elif model_type == 'nasnet_mobile':
        model = nasnet.NASNetMobile(weights=None, classes=num_classes,
                                    input_shape=ImageClassificationConfig.INPUT_SHAPE)
    elif model_type == 'xception':
        model = xception.Xception(weights=None, classes=num_classes,
                                  input_shape=ImageClassificationConfig.INPUT_SHAPE)
    else:
        model = densenet.DenseNet121(weights=None, classes=num_classes,
                                     input_shape=ImageClassificationConfig.INPUT_SHAPE)

    if gpu_num > 1:
        model = multi_gpu_model(model, gpus=gpu_num)

    return model
