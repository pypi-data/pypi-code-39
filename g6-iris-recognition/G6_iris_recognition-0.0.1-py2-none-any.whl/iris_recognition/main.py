from G6_iris_recognition.iris_matching import *
from G6_iris_recognition.encode_iris_model import *
import os
import sys
import argparse

import click
# "Test_Image/25/nkll5.bmp"
# "Input_database"
# this means that if this script is executed, then 
# main() will be executed
# if __name__ == '__main__':
#     inputdata=""
#     inputdata = str(input('"train" or "test" = '))
#     if inputdata=="train":
#         # print('++++++++++++++++++')
#         train_db_path = str(input('enter train database path = '))
#         if os.path.exists(train_db_path):
#             train_db_model_path = str(input('create model file name as irisEncodings.pickle and give his path = '))
#             if os.path.exists(train_db_path):
#                 iris_test_model(train_db_path,train_db_model_path) 
#             else:
#                 print("model path not exist")        
#         else:
#             print("database path not exist")    
#     elif inputdata=="test":
#         # print('___________________')
#         test_db_model_path = str(input('give path of created model name as irisEncodings.pickle = '))
#         if os.path.exists(test_db_model_path):
#             iris_recg(test_db_model_path)
#         else:
#             print("model path not exist")    
#     else:
#         print('please inter input  "train" or "test"')
        


def iris_model_train(train_db_path, train_encoding_model_path):
    if os.path.exists(train_db_path):
        if os.path.exists(train_encoding_model_path):
                iris_names=iris_test_model(train_db_path,train_encoding_model_path)
                return iris_names
        else:
                print("encoding model path not exist")  
                return "encoding model path not exist"      
    else:
        print("image database path not exist") 
        return "image database path not exist" 
        

def iris_model_test(test_encoding_model_path,image_path):   
    if os.path.exists(test_encoding_model_path):
        if os.path.exists(image_path):
                iris_name=iris_recg(test_encoding_model_path,image_path) 
                return iris_name
        else:
                print("image path not exist")
                return "image path not exist"        
    else:
        print("image model path not exist") 
        return "image model path not exist"




# @click.command()
# @click.argument('train_encoding_model_path')
# @click.argument('train_db_path')
# @click.argument('image_path')
# @click.argument('test_encoding_model_path')
# @click.option('--cpus', default=1, help='number of CPU cores to use in parallel (can speed up processing lots of images). -1 means "use all in system"')
# @click.option('--tolerance', default=0.6, help='Tolerance for face comparisons. Default is 0.6. Lower this if you get multiple matches for the same person.')
# @click.option('--show-distance', default=False, type=bool, help='Output face distance. Useful for tweaking tolerance setting.')
def main():


    # parser = argparse.ArgumentParser(
    #     description='CLI - iris recognition.')
    # parser.add_argument('-t', '--train_encoding_model_path', type=str)
    # parser.add_argument('-t', '--train_db_path', type=str)
    # parser.add_argument('-t', '--test_encoding_model_path', type=str)
    # parser.add_argument('-i', '--image_path', type=str)
    #
    # if len(sys.argv) < 2:
    #     print('Specify a key to use')
    #     sys.exit(1)
    #
    # # Optional bash tab completion support
    # try:
    #     import argcomplete
    #     argcomplete.autocomplete(parser)
    # except ImportError:
    #     pass
    #
    # args = parser.parse_args()
    # if args.train_db_path != None and args.train_encoding_model_path != None:
    #     iris_model_train(args.train_db_path, args.train_encoding_model_path)
    # if args.test_encoding_model_path != None and args.image_path != None:
    #     iris_model_test(args.test_encoding_model_path,args.image_path)
    #
    #


    # iris_names=iris_model_train(train_db_path, train_encoding_model_path)
    # iris_name=iris_model_test(test_encoding_model_path,image_path)

    print("iris_coding")


if __name__ == "__main__":
    main()

# iris_main(aa):
#         print("iris maun file",aa)


# if __name__ == "__main__":
#     iris_main("hiii")
