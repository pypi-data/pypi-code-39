
# coding: utf-8

# In[1]:


import sys
import common_speed
from smrt import sensor_list



if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(prog='process')
    parser.add_argument('--nop', action="store_true", help="use non-optimized code")
    parser.add_argument('-l', '--nlyr', help="number of layers", default=40)

    args = parser.parse_args(sys.argv[1:])


    model = common_speed.get_model(args, emmodel='iba')

    act35 = sensor_list.active(10e9, 35)
 
    res = model.run(act35, common_speed.setup_exp_snowpack(nlyr=int(args.nlyr)))

    print(res.sigmaVV())
