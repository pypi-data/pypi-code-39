import os, sys
import tensorflow as tf
from ..tf_net.bert.tokenization import BasicTokenizer, load_vocab
from ..tf_net.bert import modeling
from .tf_models import TF, InputFeature


class BERT(TF):
    cfg = TF.cfg.copy()
    cfg.batch_size = 16

    tokenizer = BasicTokenizer()

    def __init__(self, name=None, cfg={}, batch_reader=None):
        super(BERT, self).__init__(name, cfg, batch_reader)
        self.vocab = load_vocab(self.cfg.bert_vocab_file)
        self.cfg.bert_config_file = os.path.join(cfg.data_dir, "bert/chinese_L-12_H-768_A-12/bert_config.json")
        self.cfg.bert_vocab_file = os.path.join(cfg.data_dir, "bert/chinese_L-12_H-768_A-12/vocab.txt")
        self.cfg.init_checkpoint = os.path.join(cfg.data_dir, "bert/chinese_L-12_H-768_A-12/bert_model.ckpt")

    def _init_input_features(self):
        input_features = list()
        input_features.append(InputFeature('seqs', [None, None], tf.int32))
        input_features.append(InputFeature('seqs_len', [None], tf.int32))
        return input_features

    def _add_main_graph(self):
        self.add_bert(self.seqs, self.seqs_len, self._training_plh)

    def add_bert(self, seqs, seqs_len, training):
        mask = tf.cast(tf.sequence_mask(seqs_len, tf.shape(self.seqs)[1]), seqs.dtype)
        bert_config = modeling.BertConfig.from_json_file(self.cfg.bert_config_file)
        self._bert_model = modeling.BertModel(config=bert_config, is_training=training, input_ids=seqs,
                                              input_mask=mask,
                                              use_one_hot_embeddings=False)
        self._feas = self._bert_model.get_sequence_output()
        self._var_init = tf.global_variables_initializer()
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        self.init_var()

    def init_var(self):
        tvars = tf.trainable_variables()
        #initialized_variable_names = {}
        (assignment_map, initialized_variable_names) = modeling.get_assignment_map_from_checkpoint(tvars, self.cfg.init_checkpoint)
        tf.train.init_from_checkpoint(self.cfg.init_checkpoint, assignment_map)
        #with self._sess.graph.as_default():
        #    saver = tf.train.Saver()
        #    saver.restore(self._sess, self.cfg.init_checkpoint)

    def extract_feas(self, ori_batch, batch_size=16):
        num = len(ori_batch['sents'])
        inds = np.arange(num)
        num_batch = (num + batch_size - 1) // batch_size
        feas = [];
        ori_sent_id = 0
        for i in range(num_batch):
            batch = {}
            batch_inds = inds[batch_size * i:min(batch_size * (i + 1), num)]
            batch['batch_inds'] = batch_inds
            batch['sent_ids'] = batch_inds
            batch['sents'] = ori_batch['sents'][batch_inds]
            batch = self.bert_batch(batch)
            fea = self.run(self._sess, batch, self._feas)
            pre_sent_id = -1;
            comb_fea = []
            for f, ind, sent_id in zip(fea, batch['ori_to_tok_inds'], batch['sent_ids']):
                if sent_id != pre_sent_id and len(comb_fea) > 0:
                    feas.append(np.concatenate(comb_fea))
                    comb_fea = []
                comb_fea.append(f[ind])
                pre_sent_id = sent_id
            if len(comb_fea) > 0:
                feas.append(np.concatenate(comb_fea))

        return feas

    def seq(self, chars):
        seq = []
        for char in chars:
            if char in self.vocab:
                seq.append(self.vocab[char])
            else:
                seq.append(self.vocab['[UNK]'])
        return seq

    def bert_sents(self, sents, sents_id, max_len=512):
        ori_to_tok_inds = []
        seqs = []; seqs_len = []; new_sents_ids = []; ori_seqs_len = []
        for sent_id, sent in  enumerate(sents_id, sents):
            ori_to_tok_ind = []
            new_tokens = ['[CLS]']
            ind = 1
            for i, token in enumerate(sent):
                ori_to_tok_ind.append(ind)
                for new_token in self.tokenizer.tokenize(token):
                    new_tokens.append(new_token)
                    ind += 1
                    if ind >= (max_len - 2):
                        new_tokens.append('[SEP]')
                        ori_seqs_len.append(len(ori_to_tok_ind))
                        ori_to_tok_inds.append(ori_to_tok_ind)
                        seqs.append(self.seq(new_tokens))
                        seqs_len.append(len(new_tokens))
                        new_sents_ids.append(sent_id)
                        new_tokens = ['[CLS]']
                        ind = 1
                        ori_to_tok_ind = []
            if len(new_tokens) > 1:
                new_tokens.append('[SEP]')
                ori_seqs_len.append(len(ori_to_tok_ind))
                ori_to_tok_inds.append(ori_to_tok_ind)
                seqs.append(self.seq(new_tokens) + [0] * (max_len-len(new_tokens)))
                seqs_len.append(len(new_tokens))
                new_sents_ids.append(sent_id)
        max_ori_seqs_len = max(ori_seqs_len)
        for ori_to_tok_ind, ori_seq_len in zip(ori_to_tok_inds, ori_seqs_len):
            ori_to_tok_ind + [-1]*(max_ori_seqs_len-ori_seq_len)
        return seqs, seqs_len, ori_seqs_len, new_sents_ids, ori_to_tok_inds
