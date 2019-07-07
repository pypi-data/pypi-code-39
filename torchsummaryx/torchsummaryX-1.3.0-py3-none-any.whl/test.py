import torch
import torch.nn as nn
import torch.nn.functional as F
from torchsummaryX import summary

import torchvision
model = torchvision.models.resnet18()
summary(model, torch.zeros(4, 3, 224, 224))
