
# coding: utf-8

# In[1]:


import sys
import common_speed
from smrt import sensor_list



if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(prog='process')
    parser.add_argument('--nop', action="store_true", help="use non-optimized code")
    parser.add_argument('-l', '--nlyr', help="number of layers", default=100)
    parser.add_argument('-d', '--ndensity', help="number of density steps", default=10)

    args = parser.parse_args(sys.argv[1:])


    model = common_speed.get_model(args, emmodel='iba')

    pa35 = sensor_list.passive(10e9, 35)
 
    res = model.run(pa35, common_speed.setup_exp_snowpack(nlyr=int(args.nlyr), ndensity=int(args.ndensity)))

    print(res.TbV())
