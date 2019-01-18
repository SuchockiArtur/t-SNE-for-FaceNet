from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os

from packages.classifierTSNEv3 import training

normal_data_dir = "train_img"
align_datadata_dir = "align_img"

print ("Aligning photos Start")
os.system("python align\\align_dataset_mtcnn.py train_img align_img")
print ("Aligning photos Finished")


sys.exit("All Done")
