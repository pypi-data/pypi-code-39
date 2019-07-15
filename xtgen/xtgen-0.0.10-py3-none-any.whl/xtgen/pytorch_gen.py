# pytorch_gen.py: code for generating pytorch apps
import os
import shutil
from . import utils

class PytorchGenerator():
    def __init__(self):
        pass

    def generate(self, output_dir, dataset, model):
        mydir = os.path.dirname(__file__) 
        if dataset == "default" and model == "default":
            utils.user_error("you must specify the dataset or the model (or both)")
            
        if dataset == "mnist":
            from_dir = mydir + "/assets/pytorch_assets/mnist"
        elif dataset == "snli":
            from_dir = mydir + "/assets/pytorch_assets/snli"
        else:
            utils.user_error("dataset not yet available for pytorch: {}".format(dataset))

        shutil.copytree(from_dir, output_dir)

        # zap the __pycache__ directory created by pip install for our assets
        utils.zap_tree(output_dir + "/__pycache__")

        # count files generated (recursively)
        count = sum([len(files) for r, d, files in os.walk(output_dir)])
        return count
        
