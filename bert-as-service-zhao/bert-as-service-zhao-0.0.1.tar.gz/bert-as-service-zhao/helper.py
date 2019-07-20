# -*- coding: utf-8 -*-
# Design by zhaoguanzhi
# Email: zhaoguanzhi1992@163.com

import argparse
import os

__all__ = ['get_args_parser']

def get_args_parser():
    parser = argparse.ArgumentParser()
    group1 = parser.add_argument_group('File Paths', 'config the path, checkpoint and '
                                                     'filename of a pretrained/fine-tuned BERT model')
    group1.add_argument('-root_path', type=str, default=os.path.join(os.path.dirname(__file__)),
                        help='path of root dir')
    group1.add_argument('-bert_path', type=str, default='model_bert',
                        help='path of bert model')
    group1.add_argument('-raw_data_dir', type=str, default='data_raw',
                        help='nlu.md and jieba_lookup_files')
    group1.add_argument('-data_seq2seq_dir', type=list, default=['data_washed', 'seq2seq'],
                        help='train, dev and test data dir')
    group1.add_argument('-data_ir_dir', type=list, default=['data_washed', 'ir'],
                        help='train, dev and test data dir')
    group1.add_argument('-data_ner_dir', type=list, default=['data_washed', 'ner'],
                        help='train, dev and test data dir')
    group1.add_argument('-seq2seq_config_file', type=list, default=['base_seq2seq',
                        'seq2seq_config.json'])
    group1.add_argument('-bert_config_file', type=str, default='bert_config.json')
    group1.add_argument('-output_ner_dir', type=str, default='model_ner',
                        help='directory of a pretrained BERT NER model')
    group1.add_argument('-output_ner_bisltm_dir', type=str, default='model_ner_bilstm',
                        help='directory of a pretrained BERT NER model')
    group1.add_argument('-output_ir_dir', type=str, default='model_ir',
                        help='directory of a pretrained BERT classification model')
    group1.add_argument('-output_seq2seq_dir', type=str, default='model_seq2seq',
                        help='directory of a seq2seq model')
    group1.add_argument('-init_checkpoint', type=str, default='bert_model.ckpt',
                        help='Initial checkpoint (usually from a pre-trained BERT model).')
    group1.add_argument('-vocab_file', type=str, default='vocab.txt',
                        help='')

    group2 = parser.add_argument_group('Model Config', 'config the model params')
    group2.add_argument('-max_seq_length', type=int, default=128,
                        help='The maximum total input sequence length after WordPiece tokenization.')
    group2.add_argument('-do_train', action='store_false', default=True,
                        help='Whether to run training.')
    group2.add_argument('-do_eval', action='store_false', default=True,
                        help='Whether to run eval on the dev set.')
    group2.add_argument('-do_predict', action='store_false', default=True,
                        help='Whether to run the predict in inference mode on the test set.')
    group2.add_argument('-batch_size', type=int, default=32,
                        help='Total batch size for training, eval and predict.')
    group2.add_argument('-learning_rate', type=float, default=1e-5,
                        help='The initial learning rate for Adam.')
    group2.add_argument('-num_train_epochs', type=float, default=10,
                        help='Total number of training epochs to perform.')
    group2.add_argument('-dropout_rate', type=float, default=0.5,
                        help='Dropout rate')
    group2.add_argument('-clip', type=float, default=0.5,
                        help='Gradient clip')
    group2.add_argument('-warmup_proportion', type=float, default=0.1,
                        help='Proportion of training to perform linear learning rate warmup for '
                             'E.g., 0.1 = 10% of training.')
    group2.add_argument('-lstm_size', type=int, default=128,
                        help='size of lstm units.')
    group2.add_argument('-num_layers', type=int, default=1,
                        help='number of rnn layers, default is 1.')
    group2.add_argument('-cell', type=str, default='lstm',
                        help='which rnn cell used.')
    group2.add_argument('-save_checkpoints_steps', type=int, default=500,
                        help='save_checkpoints_steps')
    group2.add_argument('-save_summary_steps', type=int, default=500,
                        help='save_summary_steps.')
    group2.add_argument('-filter_adam_var', type=bool, default=False,
                        help='after training do filter Adam params from model and save no Adam params model in file.')
    group2.add_argument('-do_lower_case', type=bool, default=True,
                        help='Whether to lower case the input text.')
    group2.add_argument('-clean', type=bool, default=True)
    group2.add_argument('-device_map', type=str, default='0',
                        help='switch device using to train')
    group2.add_argument('-threshold_of_break', type=int, default=5000,
                        help='do nothing improved in the latest threshold_of_break epoches')
    group2.add_argument('-validation_scale', type=int, default=100,
                        help='randomly choose validation_scale of validations to do eval')

    # add labels
    group2.add_argument('-label_list', type=str, default=None,
                        help='User define labels， can be a file with one label one line or a string using \',\' split')

    parser.add_argument('-verbose', action='store_true', default=False,
                        help='turn on tensorflow logging for debug')
    parser.add_argument('-ner', type=str, default='ner', help='which modle to train')
    parser.add_argument('-version', action='version', version='%(prog)s ')
    return parser.parse_args()

def get_args():
    args = get_args_parser()
    args.bert_path = os.path.join(args.root_path, args.bert_path)
    args.raw_data_dir = os.path.join(args.root_path, args.raw_data_dir)
    args.data_seq2seq_dir = os.path.join(args.root_path,
                                         args.data_seq2seq_dir[0],
                                         args.data_seq2seq_dir[1])
    args.data_ir_dir = os.path.join(args.root_path,
                                         args.data_ir_dir[0],
                                         args.data_ir_dir[1])
    args.data_ner_dir = os.path.join(args.root_path,
                                         args.data_ner_dir[0],
                                         args.data_ner_dir[1])
    args.seq2seq_config_file = os.path.join(args.root_path,
                                            args.seq2seq_config_file[0],
                                            args.seq2seq_config_file[1])
    args.bert_config_file = os.path.join(args.bert_path, args.bert_config_file)
    args.output_ner_dir = os.path.join(args.root_path, args.output_ner_dir)
    args.output_ner_bisltm_dir = os.path.join(args.root_path, args.output_ner_bisltm_dir)
    args.output_ir_dir = os.path.join(args.root_path, args.output_ir_dir)
    args.output_seq2seq_dir = os.path.join(args.root_path, args.output_seq2seq_dir)
    args.init_checkpoint = os.path.join(args.bert_path, args.init_checkpoint)
    args.vocab_file = os.path.join(args.bert_path, args.vocab_file)
    return args