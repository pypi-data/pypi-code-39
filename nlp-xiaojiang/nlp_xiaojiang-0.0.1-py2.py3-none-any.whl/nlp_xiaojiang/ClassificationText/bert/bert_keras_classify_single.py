# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/5/30 19:29
# @author   :Mo
# @function :

# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/5/10 18:05
# @author   :Mo
# @function :classify text of bert and bi-lstm

from __future__ import division, absolute_import

import codecs
import logging as logger

import numpy as np
from nlp_xiaojiang.ClassificationText.bert import args
from nlp_xiaojiang.conf.feature_config import config_name, ckpt_name, vocab_file, max_seq_len
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from keras.layers import Dense
from keras.layers import Lambda
from keras.models import Model
from keras.objectives import categorical_crossentropy
from keras_bert import Tokenizer
from sklearn.metrics import classification_report

from nlp_xiaojiang.ClassificationText.bert.keras_bert_embedding import KerasBertEmbedding
from nlp_xiaojiang.conf.path_config import path_webank_train, path_webank_dev, path_webank_test

class BertBiLstmModel():
    def __init__(self):
        # logger.info("BertBiLstmModel init start!")
        print("BertBiLstmModel init start!")
        self.config_path, self.checkpoint_path, self.dict_path, self.max_seq_len = config_name, ckpt_name, vocab_file, max_seq_len
        # reader tokenizer
        self.token_dict = {}
        with codecs.open(self.dict_path, 'r', 'utf8') as reader:
            for line in reader:
                token = line.strip()
                self.token_dict[token] = len(self.token_dict)

        self.tokenizer = Tokenizer(self.token_dict)
        # 你可以选择一个model build，有bi-lstm single、bi-lstm 3-layers、bi-lstm_attention
        self.build_model_bert_single_layer()
        # logger.info("BertBiLstmModel init end!")
        print("BertBiLstmModel init end!")

    def process_single(self, texts):
        # 文本预处理，传入一个list，返回的是ids\mask\type-ids
        input_ids = []
        input_masks = []
        input_type_ids = []
        for text in texts:
            logger.info(text)
            tokens_text = self.tokenizer.tokenize(text)
            logger.info('Tokens:', tokens_text)
            input_id, input_type_id = self.tokenizer.encode(first=text, max_len=self.max_seq_len)
            input_mask = [0 if ids == 0 else 1 for ids in input_id]
            input_ids.append(input_id)
            input_type_ids.append(input_type_id)
            input_masks.append(input_mask)
        # numpy处理list
        input_ids = np.array(input_ids)
        input_masks = np.array(input_masks)
        input_type_ids = np.array(input_type_ids)
        logger.info("process ok!")
        return input_ids, input_masks, input_type_ids

    def process_pair(self, textss):
        # 文本预处理，传入一个list，返回的是ids\mask\type-ids
        input_ids = []
        input_masks = []
        input_type_ids = []
        for texts in textss:
            tokens_text = self.tokenizer.tokenize(texts[0])
            logger.info('Tokens1:', tokens_text)
            tokens_text2 = self.tokenizer.tokenize(texts[1])
            logger.info('Tokens2:', tokens_text2)
            input_id, input_type_id = self.tokenizer.encode(first=texts[0], second=texts[1], max_len=self.max_seq_len)
            input_mask = [0 if ids == 0 else 1 for ids in input_id]
            input_ids.append(input_id)
            input_type_ids.append(input_type_id)
            input_masks.append(input_mask)
        # numpy处理list
        input_ids = np.array(input_ids)
        input_masks = np.array(input_masks)
        input_type_ids = np.array(input_type_ids)
        logger.info("process ok!")
        return input_ids, input_masks, input_type_ids

    def build_model_bert_single_layer(self):
        # bert embedding
        bert_inputs, bert_output = KerasBertEmbedding().bert_encode(layer_indexes=-1)
        layer_get_cls = Lambda(lambda x: x[:, 0:1, :])
        x = layer_get_cls(bert_output)
        # print("layer_get_cls:")
        # print(bert_output.shape)
        print(x.shape)
        # 最后就是softmax
        dense_layer = Dense(args.label, activation=args.activation)(x)
        output_layers = [dense_layer]
        self.model = Model(bert_inputs, output_layers)

    def compile_model(self):
        self.model.compile(optimizer=args.optimizers,
                           loss=categorical_crossentropy,
                           metrics=args.metrics)

    def callback(self):
        cb = [ModelCheckpoint(args.path_save_model, monitor='val_loss',
                              verbose=1, save_best_only=True, save_weights_only=False, mode='min'),
              EarlyStopping(min_delta=1e-8, patience=4, mode='min'),
              ReduceLROnPlateau(factor=0.2, patience=4, verbose=0, mode='min', epsilon=1e-6, cooldown=4, min_lr=1e-8)
              ]
        return cb

    def fit(self, x_train, y_train, x_dev, y_dev):
        self.model.fit(x_train, y_train, batch_size=args.batch_size,
                       epochs=args.epochs, validation_data=(x_dev, y_dev),
                       shuffle=True,
                       callbacks=self.callback())
        self.model.save(args.path_save_model)

    def load_model(self):
        print("BertBiLstmModel load_model start!")
        # logger.info("BertBiLstmModel load_model start!")
        self.model.load_weights(args.path_save_model)
        # logger.info("BertBiLstmModel load_model end+!")
        print("BertBiLstmModel load_model end+!")

    def predict(self, sen_1, sen_2):
        input_ids, input_masks, input_type_ids = self.process_pair([[sen_1, sen_2]])
        return self.model.predict([input_ids, input_masks], batch_size=1)

    def predict_list(self, questions):
        label_preds = []
        for questions_pair in questions:
            input_ids, input_masks, input_type_ids = self.process_pair([questions_pair])
            label_pred = self.model.predict([input_ids, input_masks], batch_size=1)
            label_preds.append(label_pred[0])
        return label_preds


def classify_single_corpus(bert_model):
    # 数据预处理
    from nlp_xiaojiang.utils import text_preprocess, txtRead
    from nlp_xiaojiang.conf.path_config import path_webank_sim
    import random

    webank_q_2_l = txtRead(path_webank_sim, encodeType='gbk')
    questions = []
    labels = []
    for ques_label in webank_q_2_l[1:]:
        q_2_l = ques_label.split(',')
        q_2 = "".join(q_2_l[:-1])
        label = q_2_l[-1]
        questions.append(text_preprocess(q_2))
        label_int = int(label)
        labels.append([0, 1] if label_int == 1 else [1, 0])

    questions = np.array(questions)
    labels = np.array(labels)
    index = [i for i in range(len(labels))]
    random.shuffle(index)
    questions = questions[index]
    labels = labels[index]
    len_train = int(len(labels) * 0.9)

    train_x, train_y = questions[0:len_train], labels[0:len_train]
    test_x, test_y = questions[len_train:], labels[len_train:]

    input_ids, input_masks, input_type_ids = bert_model.process_single(train_x)
    input_ids2, input_masks2, input_type_ids2 = bert_model.process_single(test_x)

    return train_x, train_y, test_x, test_y, input_ids, input_masks, input_type_ids, input_ids2, input_masks2, input_type_ids2


def classify_pair_corpus(bert_model):
    # 数据预处理
    from nlp_xiaojiang.utils import text_preprocess, txtRead
    from nlp_xiaojiang.conf.path_config import path_webank_sim
    import random

    webank_q_2_l = txtRead(path_webank_sim, encodeType='gbk')
    questions = []
    labels = []
    for ques_label in webank_q_2_l[1:]:
        q_2_l = ques_label.split(',')
        q_1 = q_2_l[0]
        q_2 = "".join(q_2_l[1:-1])
        label = q_2_l[-1]
        questions.append([text_preprocess(q_1), text_preprocess(q_2)])
        label_int = int(label)
        labels.append([0, 1] if label_int == 1 else [1, 0])

    questions = np.array(questions)
    labels = np.array(labels)
    index = [i for i in range(len(labels))]
    random.shuffle(index)
    questions = questions[index]
    labels = labels[index]
    len_train = int(len(labels) * 0.9)

    train_x, train_y = questions[0:len_train], labels[0:len_train]
    test_x, test_y = questions[len_train:], labels[len_train:]

    input_ids, input_masks, input_type_ids = bert_model.process_pair(train_x)
    input_ids2, input_masks2, input_type_ids2 = bert_model.process_pair(test_x)

    return train_x, train_y, test_x, test_y, input_ids, input_masks, input_type_ids, input_ids2, input_masks2, input_type_ids2


def classify_pair_corpus_webank(bert_model, path_webank):
    # 数据预处理
    from nlp_xiaojiang.utils import text_preprocess, txtRead

    webank_q_2_l = txtRead(path_webank, encodeType='utf-8')
    questions = []
    labels = []
    for ques_label in webank_q_2_l[1:]:
        q_2_l = ques_label.split(',')
        q_1 = q_2_l[0]
        q_2 = "".join(q_2_l[1:-1])
        label = q_2_l[-1]
        questions.append([text_preprocess(q_1), text_preprocess(q_2)])
        label_int = int(label)
        labels.append([0, 1] if label_int == 1 else [1, 0])

    questions = np.array(questions)
    labels = np.array(labels)

    input_ids, input_masks, input_type_ids = bert_model.process_pair(questions)

    return questions, labels, input_ids, input_masks, input_type_ids


def train():
    # 1. trian
    bert_model = BertBiLstmModel()
    bert_model.compile_model()
    _, labels_train, input_ids_train, input_masks_train, _ = classify_pair_corpus_webank(bert_model, path_webank_train)
    _, labels_dev, input_ids_dev, input_masks_dev, _ = classify_pair_corpus_webank(bert_model, path_webank_dev)
    # questions_test, labels_test, input_ids_test, input_masks_test, _ = classify_pair_corpus_webank(bert_model, path_webank_test)
    print("process corpus ok!")
    bert_model.fit([input_ids_train, input_masks_train], labels_train, [input_ids_dev, input_masks_dev], labels_dev)
    print("bert_model fit ok!")


def tet():
    #  2.test
    bert_model = BertBiLstmModel()
    bert_model.load_model()
    questions_test, labels_test, input_ids_test, input_masks_test, _ = classify_pair_corpus_webank(bert_model,
                                                                                                   path_webank_test)
    print('predict_list start! you will wait for a few minutes')
    labels_pred = bert_model.predict_list(questions_test)
    print('predict_list end!')

    labels_pred_np = np.array(labels_pred)
    labels_pred_np_arg = np.argmax(labels_pred_np, axis=1)
    labels_test_np = np.array(labels_test)
    labels_test_np_arg = np.argmax(labels_test_np, axis=1)
    target_names = ['不相似', '相似']
    report_predict = classification_report(labels_test_np_arg, labels_pred_np_arg,
                                           target_names=target_names, digits=9)
    print(report_predict)


def predict():
    # 3. predict
    bert_model = BertBiLstmModel()
    bert_model.load_model()
    pred = bert_model.predict(sen_1='jy', sen_2='myz')
    print(pred[0][1])
    while True:
        print("sen_1: ")
        sen_1 = input()
        print("sen_2: ")
        sen_2 = input()
        pred = bert_model.predict(sen_1=sen_1, sen_2=sen_2)
        print(pred[0][1])


if __name__ == "__main__":
    train()
    # tet()
    # predict()
