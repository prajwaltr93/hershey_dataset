#filename : create_metadata.py
#author : PRAJWAL T R
#date last modified : Sat Sep 12 22:25:16 2020
#comments :

'''
    script to get metadata such as input/output dimension, number of samples
    in train, test and validation sets for both global and local datasets.

    USAGE:
    $python create_metadata.py <dataset> <train> <validation> <test>

    dataset - L -> Local Dataset
              G -> Global Dataset
    <test>,
    <test>,
    <train> - integer number of files to consider to count samples
'''

import sys
from drawing_utils import *
import pickle as pic

global_dataset_path = "./global_dataset/"
local_dataset_path = "./local_dataset/"

def help():
    print("$python create_metadata.py <dataset> <train> <validation> <test> \n \
    dataset - L -> Local Dataset \n \
              G -> Global Dataset \n \
    <test>, \n \
    <test>, \n \
    <train> - integer number of files to consider to count samples")
    exit(0)

if len(sys.argv) != 5:
    print("not enough arguements")
    help() # print help and return

# argument processing
try:
    if sys.argv[1].lower() == 'g':
        path = global_dataset_path
        metadata = {
                    'train_samples' : 0,
                    'validation_samples' : 0,
                    'test_samples' : 0,
                    'img_dim' : [HEIGHT, WIDTH],
                    'label_dim' : HEIGHT * WIDTH
        }
    elif sys.argv[1].lower() == 'l':
        path = local_dataset_path
        #meta-data structure
        metadata = {
            "img_dim" : [HEIGHT, WIDTH],
            "target_img_dim" : crop_img_size*crop_img_size,
            "slice_tensor_dim" : 3,
            "train_samples" : 0,
            "validation_samples" : 0,
            "test_samples" : 0
        }
    else:
        help()
except:
    help()

try:
    train = int(sys.argv[2])
    validation = int(sys.argv[3])
    test = int(sys.argv[4])
except:
    # train, test, validation should be integers
    help()

from os import walk

_, _, filelist = next(walk(path))
if (train + validation + test) > len(filelist):
    print("Found {} data files, requested for {} files".format(len(filelist) - 1, train + test + validation))
    exit(0)

# create metadata structure
train_files = ["data_batch_"+i.__str__() for i in range(train)] #two files
validation_files = ["data_batch_"+(train+i).__str__() for i in range(validation)]
test_files = ["data_batch_"+(train+validation+i).__str__() for i in range(test)]

traverse_list = [train_files, validation_files, test_files]
traverse_values = ['train_samples', 'validation_samples', 'test_samples']

for fold, fold_value in zip(traverse_list, traverse_values):
    temp_len = 0
    for file in fold:
        data = pic.load(open(path + file, 'rb'), encoding = 'bytes')
        temp_len += len(data[list(data.keys())[0]])
    metadata[fold_value] = temp_len

# print generated metadata to output
for key, item in metadata.items():
    print(key, item)

# pickle dataset
fd = open(path + "metadata", 'wb')
pic.dump(metadata, fd)
print('metadata created at : ' + path + 'metadata')
