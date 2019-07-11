import torch


def weighted_smooth(values, weight):
    '''
    Create a smoothed values by using the linear interpolation with torch.lerp()
    '''
    if len(values) == 0:
        return []
    outputs = [0] * len(values)
    outputs[0] = values[0]
    for i in range(1, len(values)):
        outputs[i] = outputs[i - 1].lerp(values[i], weight)
    return outputs

def get_module_names(model):
    return [name for name, m in model.named_modules()]

def get_named_modules_by_name(model, module_names):
    modules = []
    for name, m in model.named_modules():
        if name in module_names:
            modules.append((name, m))
    return modules

def get_device():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")
