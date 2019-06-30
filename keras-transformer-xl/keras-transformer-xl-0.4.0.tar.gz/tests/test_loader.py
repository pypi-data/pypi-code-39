import os
import json
from unittest import TestCase
import numpy as np
from keras_transformer_xl import load_trained_model_from_checkpoint


class TestLoader(TestCase):

    def test_load_div_1(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        checkpoint_path = os.path.join(current_path, 'test_checkpoint_div_1')
        model = load_trained_model_from_checkpoint(
            config_path=os.path.join(checkpoint_path, 'config.json'),
            checkpoint_path=os.path.join(checkpoint_path, 'model.ckpt')
        )
        model.summary()
        tokens = np.load(os.path.join(checkpoint_path, 'tokens.npy'))
        memory_0 = np.load(os.path.join(checkpoint_path, 'memory_0.npy'))
        memory_1 = np.load(os.path.join(checkpoint_path, 'memory_1.npy'))
        softmax = np.load(os.path.join(checkpoint_path, 'softmax.npy'))
        new_memory_0 = np.load(os.path.join(checkpoint_path, 'new_memory_0.npy'))
        new_memory_1 = np.load(os.path.join(checkpoint_path, 'new_memory_1.npy'))
        outputs = model.predict([tokens, memory_0, memory_1])
        self.assertTrue(np.allclose(new_memory_0[0, 10:], outputs[1]))
        self.assertTrue(np.allclose(new_memory_1[0, 10:], outputs[2], atol=1e-6))
        self.assertTrue(np.allclose(softmax, outputs[0]))

    def test_load_div_2(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        checkpoint_path = os.path.join(current_path, 'test_checkpoint_div_2')
        model = load_trained_model_from_checkpoint(
            config_path=os.path.join(checkpoint_path, 'config.json'),
            checkpoint_path=os.path.join(checkpoint_path, 'model.ckpt')
        )
        model.summary()
        tokens = np.load(os.path.join(checkpoint_path, 'tokens.npy'))
        memory_0 = np.load(os.path.join(checkpoint_path, 'memory_0.npy'))
        memory_1 = np.load(os.path.join(checkpoint_path, 'memory_1.npy'))
        softmax = np.load(os.path.join(checkpoint_path, 'softmax.npy'))
        new_memory_0 = np.load(os.path.join(checkpoint_path, 'new_memory_0.npy'))
        new_memory_1 = np.load(os.path.join(checkpoint_path, 'new_memory_1.npy'))
        outputs = model.predict([tokens, memory_0, memory_1])
        self.assertTrue(np.allclose(new_memory_0[0, 10:], outputs[1]))
        self.assertTrue(np.allclose(new_memory_1[0, 10:], outputs[2], atol=1e-6))
        self.assertTrue(np.allclose(softmax, outputs[0]))

    def test_load_div_2_cutoffs_3(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        checkpoint_path = os.path.join(current_path, 'test_checkpoint_div_2_cutoffs_3')
        config_path = os.path.join(checkpoint_path, 'config.json')
        with open(config_path, 'r') as reader:
            config = json.loads(reader.read())
        model = load_trained_model_from_checkpoint(
            config_path=config,
            checkpoint_path=os.path.join(checkpoint_path, 'model.ckpt')
        )
        model.summary()
        tokens = np.load(os.path.join(checkpoint_path, 'tokens.npy'))
        memory_0 = np.load(os.path.join(checkpoint_path, 'memory_0.npy'))
        memory_1 = np.load(os.path.join(checkpoint_path, 'memory_1.npy'))
        memory_2 = np.load(os.path.join(checkpoint_path, 'memory_2.npy'))
        softmax = np.load(os.path.join(checkpoint_path, 'softmax.npy'))
        new_memory_0 = np.load(os.path.join(checkpoint_path, 'new_memory_0.npy'))
        new_memory_1 = np.load(os.path.join(checkpoint_path, 'new_memory_1.npy'))
        new_memory_2 = np.load(os.path.join(checkpoint_path, 'new_memory_2.npy'))
        outputs = model.predict([tokens, memory_0, memory_1, memory_2])
        self.assertTrue(np.allclose(new_memory_0[0, 10:], outputs[1]))
        self.assertTrue(np.allclose(new_memory_1[0, 10:], outputs[2], atol=1e-6))
        self.assertTrue(np.allclose(new_memory_2[0, 10:], outputs[3], atol=1e-6))
        self.assertTrue(np.allclose(softmax, outputs[0]))
