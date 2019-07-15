# help.py - contains help messages for the command line version of XTGen.

import sys
from .utils import BUILD

#--------------------------------------------------------------------
def get_about_help():
    text = f'''
XTGen ({BUILD})
XTGen is a command line tool to generate ML training apps from research datasets and architectures.

Features:
    - Generation for frameworks: PyTorch, Keras
    - Multiple areas of ML/AI supported: Vision, NLP, RL 
    - Include optional features:
        - checkpoints
        - Tensorboard logging
        - TensorWatch logging
        - early stopping
        - cmdline arguments
        - XT hyperparameter and metrics logging
        - Hovorod distributed training
        - plots/visualizations (models, weights, gradients, model performance, etc.)

The goal of XTGen is to jumpstart your entry into a new dataset/architecture so you can start trainining immediately, 
and then have a clean codebase that you can modify as needed.

For more information, run: xtgen --help'''

    return text

def get_api_help():
    text = '''
XTGen API 
The XTGen API is not yet exposed.  Let us know if you would like it to be documented and supported. '''

    return text

#--------------------------------------------------------------------
def get_cmd_help():

    text = '''
usages: 
     xtgen <options> <output directory>     # generate code to specified output dir
     xtgen config                           # edit the xtgen config file                          
     xtgen version                          # show xtgen version/build info 

note: option names can be abbreviated down to 4 letters

general options:  
     --help                          # print detailed help
     --framework <name>              # override the default framework 
     --dataset <name>                # override the default train/eval/test dataset
     --model <name>                  # override the default model
     --zap                           # remove contents of output directory before generation
     --download-root <name>          # specify root download directory for all datasets

feature options:
    --checkpoints [ <value> ]        # include support for training checkpoint/restart 
    --tb-logging <name list>         # include Tensorboard logging for the specified variables
    --tw-watches <name list>         # include TensorWatch watches for the specified variables
    --early-stopping [ <value> ]     # include code for early stopping
    --args [ <name list> ]           # include code to support cmdline arguments for app
    --xt-hparams [ <name list> ]     # include logging of hyperparameter values to XT
    --xt-metrics [ <name list> ]     # include logging of metrics values to XT
    --horovod                        # include code for Horovod distributed training

internal options:
     --diagnostics <bool>           # turn XT diagnostics msgs on/off
     --raise                        # if an exception is caught, raise it so we can see stack trace info
     --timing <bool>                # turn XT timing msgs on/off

examples:
    xtgen --framework=pytorch --data=mnist  --zap c:/xxx     # gen mnist app with default model 
    
'''

    text += get_pytorch_assets()
    text += get_keras_assets()

    return text

#--------------------------------------------------------------------
def get_pytorch_assets():

    text = '''
PyTorch datasets:
    mnist
    sli

PyTorch models:
    default
'''
    return text

#--------------------------------------------------------------------
def get_keras_assets():

    text = '''
Keras datasets:
    mnist

Keras models:
    default
'''
    return text
