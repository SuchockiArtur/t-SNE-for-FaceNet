from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from sklearn.manifold import TSNE

import math
import os
import pickle
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import time
from sklearn.svm import SVC
from packages import facenet
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment
from tensorflow.python.keras.preprocessing import image
from lapjv import lapjv


class training:
    def __init__(self, datadir, modeldir,classifier_filename):
        self.datadir = datadir
        self.modeldir = modeldir
        self.classifier_filename = classifier_filename

    def main_train(self):
        with tf.Graph().as_default():
            with tf.Session() as sess:
                img_data = facenet.get_dataset(self.datadir)
                path, label = facenet.get_image_paths_and_labels(img_data)
                print("label")
                print(label)
                print('Classes: %d' % len(img_data))
                print('Images: %d' % len(path))

                facenet.load_model(self.modeldir)
                images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
                embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
                phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
                embedding_size = embeddings.get_shape()[1]

                print('Extracting features of images for model')
                batch_size = 1000
                image_size = 160
                nrof_images = len(path)
                nrof_batches_per_epoch = int(math.ceil(1.0 * nrof_images / batch_size))
                emb_array = np.zeros((nrof_images, embedding_size))
                #print(nrof_batches_per_epoch)
                #for i in range(nrof_batches_per_epoch):
                start_index = 0 * batch_size
                end_index = min((0 + 1) * batch_size, nrof_images)
                paths_batch = path[start_index:end_index]
                images = facenet.load_data(paths_batch, False, False, image_size)
                feed_dict = {images_placeholder: images, phase_train_placeholder: False}
                emb_array[start_index:end_index, :] = sess.run(embeddings, feed_dict=feed_dict)

                class_names = [cls.name.replace('_', ' ') for cls in img_data]
                classifier_file_name = os.path.expanduser(self.classifier_filename)
                print('emb_array')
                print(emb_array)
                X_embedded = TSNE(n_components=2).fit_transform(emb_array)
                X_embedded -= X_embedded.min(axis=0)
                X_embedded /= X_embedded.max(axis=0)
                print("X_embedded")
                print (X_embedded)
                
                #for i in range(0, nrof_images-1):
                #    plt.plot(X_embedded[i, 0], X_embedded[i, 1],'bo')
                plt.legend(bbox_to_anchor=(1, 1))
                plt.show()
                out_dim=8
                out_res = 160
                to_plot = np.square(out_dim)
                grid = np.dstack(np.meshgrid(np.linspace(0, 1, out_dim), np.linspace(0, 1, out_dim))).reshape(-1, 2)
                cost_matrix = cdist(grid, X_embedded, "sqeuclidean").astype(np.float32)
                cost_matrix = cost_matrix * (100000 / cost_matrix.max())
                print (cost_matrix)
                #rids, cids = solve_dense(costs)
                #print(rids)
                row_ind, col_ind = linear_sum_assignment(cost_matrix)
                row_asses, col_asses, _ = lapjv(cost_matrix)
                print("To cos")
                print (col_asses)
                print ("teraz to!")
                print (row_ind)
                print (col_ind)
                for r,c in zip(row_ind, col_asses):
                    print(r,c) # Row/column pairings
                grid_jv = grid[col_asses]
                out = np.ones((out_dim*out_res, out_dim*out_res, 3))
                print (grid_jv)

                for pos, img in zip(grid_jv, images[0:to_plot]):
                    h_range = int(np.floor(pos[0]* (out_dim - 1) * out_res))
                    w_range = int(np.floor(pos[1]* (out_dim - 1) * out_res))
                    out[h_range:h_range + out_res, w_range:w_range + out_res]  = image.img_to_array(img)
                print (out)
                im = image.array_to_img(out)
                im.save("obrazek.jpg", quality=95)