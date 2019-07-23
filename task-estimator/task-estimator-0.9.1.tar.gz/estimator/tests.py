import os
import unittest
import tempfile
import subprocess

from estimator import Estimator


def get_status_output(*args, **kwargs):
    p = subprocess.Popen(*args, **kwargs)
    stdout, stderr = p.communicate()
    return p.returncode, stdout, stderr

# import warnings
# warnings.filterwarnings("ignore", category=ResourceWarning)


class Tests(unittest.TestCase):

    def test_write(self):
        os.system('ls -lah')
        os.system('whoami')

        fn1 = 'myfile.txt'
        text1 = b'test'
        with open(fn1, 'wb') as fout:
            fout.write(text1)
        with open(fn1, 'rb') as fin:
            self.assertEqual(fin.read(), text1)

        fn2 = '/tmp/temp1/myfile.txt'
        text2 = b'abc123'
        if not os.path.exists('/tmp/temp1'):
            os.makedirs('/tmp/temp1')
        with open(fn2, 'wb') as fout:
            fout.write(text2)
        with open(fn2, 'rb') as fin:
            self.assertEqual(fin.read(), text2)

    def test_learning(self):
        yaml_text = '''
source: fixture
projects: K
fixture: MYPROJECT
regressor:
    cls: KernelRidge
    stop_words: ''
    ngram_range: [1, 6]
    analyzer: char
    min_df: 0.0
minimum_estimate_minutes: 15
data_dir: /tmp
'''
        _, fn = tempfile.mkstemp()
        print('fn:', fn)
        try:
            with open(fn, 'w') as fout:
                fout.write(yaml_text.strip())
            estimator = Estimator.from_configuration_file(fn, verbose=True)
            print('-'*80)
            print('Retrieve:')
            estimator.retrieve(training=True, key=None, human=False)
            estimator.retrieve(training=False, key=None, human=False)
            print('-'*80)
            print('Train:')
            estimator.train()
            print('-'*80)
            print('Test(human):')
            mse, mae = estimator.test(human=True, retrain=False)
            print('MSE(human):', mse)
            print('MAE(human):', mae)
            self.assertAlmostEqual(mae, 2.6875)
            print('Test(algorithm):')
            mse, mae = estimator.test(human=False, retrain=False)
            print('MSE(algorithm):', mse)
            print('MAE(algorithm):', mae)
            self.assertAlmostEqual(mae, 2.4144952)
            print('-'*80)
            print('Apply:')
            ret = estimator.apply()
            print('ret:', ret)
        finally:
            #os.remove(fn)
            pass

    def test_commandline(self):
        yaml_text = '''
source: fixture
projects: MYPROJECT
regressor:
    cls: KernelRidge
    stop_words: ''
    ngram_range: [1, 6]
    analyzer: char
    min_df: 0.0
minimum_estimate_minutes: 15
'''
        _, fn = tempfile.mkstemp()
        try:
            with open(fn, 'w') as fout:
                fout.write(yaml_text.strip())

            ret, stdout, stderr = get_status_output(['which', 'estimator'])
            print('stdout:', stdout)
            print('stderr:', stderr)
            self.assertEqual(ret, 0)

            #TODO
            # ret, stdout, stderr = get_status_output(['estimator', '--verbose', fn, 'retrieve'])
            # print('stdout:', stdout)
            # print('stderr:', stderr)
            # self.assertEqual(ret, 0)

        finally:
            # os.remove(fn)
            pass


if __name__ == '__main__':
    unittest.main()
