import sys
#sys.path.append("crnn.pytorch")
import time

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from PIL import Image

import torch
from torch.autograd import Variable
import tidkvideochange.crnnpytorch.crnn as crnn
import tidkvideochange.crnnpytorch.utils as utils
import tidkvideochange.crnnpytorch.dataset as dataset
from . import weights

import numpy as np

def timefunc(f):
    def f_timer(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(f.__name__, 'took', end - start, 'time')
        return result
    return f_timer

#model_path = pkg_resources.resource_filename(weights, "crnn.pth")
with pkg_resources.path(weights, "crnn.pth") as path:
    model_path = str(path.resolve())
#model_path = './weights/crnn.pth'
alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
model = None
converter = None
transformer = None

def prepare_model():
    global model
    global converter
    global transformer
    #Intial model
    model = crnn.CRNN(32, 1, 37, 256)
    if torch.cuda.is_available():
        model = model.cuda()
    #print('loading pretrained model from %s' % model_path)
    model.load_state_dict(torch.load(model_path))

    #For decoding model output
    converter = utils.strLabelConverter(alphabet)
    #For preprocessing the input
    transformer = dataset.resizeNormalize((100, 32))

def recognize_cropped(images, cuts):
    
    stacked_images = None
    for img in images:
        image = transformer(img.convert('L'))
        img_np = np.array(image)
        img_np_expanded = np.expand_dims(img_np, axis=0)
        if stacked_images is None:
            stacked_images = img_np_expanded
        else:
            stacked_images = np.concatenate([stacked_images, img_np_expanded], axis=0)
    #print(stacked_images.shape)
    #print(cuts)
    #return 0, 0
    #image = transformer(images.convert('L'))
    #if torch.cuda.is_available():
    #    image = image.cuda()
    #Reshaping by adding another axis with length 1 at the beginning
    # [1, 32, 100] -> [1, 1, 32, 100]
    #image = image.view(1, *image.size())
    
    #Create pytorch variable and evaluate(infer) the model
    image = torch.from_numpy(stacked_images)
    if torch.cuda.is_available():
        image = image.cuda()
    image = Variable(image)
    model.eval()
    preds = model(image)
    # preds.size() = [26, 1, 37]
    #print(preds.size())
    #Process preds for decoding
    _, preds = preds.max(2)
    #print(preds.size())
    preds_size = Variable(torch.IntTensor(preds.size(1)*[preds.size(0)]))
    #print(preds_size)
    preds = preds.transpose(1, 0).contiguous().view(-1)
    #print(preds.size())

    #Decode
    #preds_size = Variable(torch.IntTensor([preds.size(0)]))
    raw_pred = converter.decode(preds.data, preds_size.data, raw=True)
    sim_pred = converter.decode(preds.data, preds_size.data, raw=False)
    #print(sim_pred)
    i = 0
    j = 1
    sim_pred_split = []
    while j < len(cuts):
        a = sim_pred[cuts[i]:cuts[j]]
        #print(a)
        sim_pred_split.append(a)
        i += 1
        j += 1
    return raw_pred, sim_pred_split
    #print('%-20s => %-20s' % (raw_pred, sim_pred))
 
@timefunc
def recognize(filename,wordBB):
    text = []
    images = []
    cuts = []
    i = 0
    cuts.append(i)
    for b, f in zip(wordBB, filename):
        #texts = []
        for bb in b:
            image = Image.open(f)
            images.append(image.crop(bb))
            i += 1
            #raw_pred, sim_pred = recognize_cropped(image.crop(bb))
            #texts.append(sim_pred)
        #text.append(texts)
        cuts.append(i)
    raw_pred, sim_pred = recognize_cropped(images, cuts)
    #text.append(sim_pred)
    return sim_pred