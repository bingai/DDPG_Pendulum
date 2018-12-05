# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# import tensorflow as tf
# import numpy as np
# import gym
# from gym import wrappers
# variables_names = [v.name for v in tf.trainable_variables()]
# with tf.Session() as sess:
#     values = sess.run(variables_names)
#     for k, v in zip(variables_names, values):
#         print ("Variable: ", k)
#         print ("Shape: ", v.shape)
#         print (v)

import tensorflow as tf;  
import numpy as np;  
import matplotlib.pyplot as plt;  

v = tf.Variable(tf.constant(0.0, shape=[1], dtype=tf.float32), name='v')
v1 = tf.Variable(tf.constant(5, shape=[1], dtype=tf.float32), name='v1')

global_step = tf.Variable(tf.constant(5, shape=[1], dtype=tf.float32), name='global_step', trainable=False)
ema = tf.train.ExponentialMovingAverage(0.99, global_step)

for ele1 in tf.trainable_variables():
	print (ele1.name)
for ele2 in tf.all_variables():
	print (ele2.name)
