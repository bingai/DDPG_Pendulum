import tensorflow as tf
# import numpy as np
# import gym
# from gym import wrappers
import tflearn
from time import time
# import argparse
# import pprint as pp

# ===========================
#   Actor DNN
# ===========================

class ActorNetwork(object):
    """
    Input to the network is the state, output is the action
    under a deterministic policy.

    The output layer activation is a tanh to keep the action
    between -action_bound and action_bound
    """

    def __init__(self, sess, state_dim, action_dim, action_bound, learning_rate, tau, batch_size):
        self.sess = sess
        self.s_dim = state_dim
        self.a_dim = action_dim
        self.action_bound = action_bound
        self.learning_rate = learning_rate
        self.tau = tau
        self.batch_size = batch_size

        # Actor Network
        self.inputs, self.out, self.scaled_out = self.create_actor_network()

        self.network_params = tf.trainable_variables()

        # Target Network
        self.target_inputs, self.target_out, self.target_scaled_out = self.create_actor_network()

        self.target_network_params = tf.trainable_variables()[
            len(self.network_params):]

        # Op for periodically updating target network with online network
        # weights
        self.update_target_network_params = \
            [self.target_network_params[i].assign(tf.multiply(self.network_params[i], self.tau) +
                                                  tf.multiply(self.target_network_params[i], 1. - self.tau))
                for i in range(len(self.target_network_params))]

        # This gradient will be provided by the critic network
        self.action_gradient = tf.placeholder(tf.float32, [None, self.a_dim])

        # Combine the gradients here
        self.unnormalized_actor_gradients = tf.gradients(
            self.scaled_out, self.network_params, -self.action_gradient)
        self.actor_gradients = list(map(lambda x: tf.div(x, self.batch_size), self.unnormalized_actor_gradients))

        # Optimization Op
        self.optimize = tf.train.AdamOptimizer(self.learning_rate).\
            apply_gradients(zip(self.actor_gradients, self.network_params))

        self.num_trainable_vars = len(
            self.network_params) + len(self.target_network_params)

    def create_actor_network(self):
        inputs = tflearn.input_data(shape=[None, self.s_dim])
        net = tflearn.fully_connected(inputs, 400)
        net = tflearn.layers.normalization.batch_normalization(net)
        net = tflearn.activations.relu(net)
        net = tflearn.fully_connected(net, 300)
        net = tflearn.layers.normalization.batch_normalization(net)
        net = tflearn.activations.relu(net)
        # Final layer weights are init to Uniform[-3e-3, 3e-3]
        w_init = tflearn.initializations.uniform(minval=-0.003, maxval=0.003)
        out = tflearn.fully_connected(
            net, self.a_dim, activation='tanh', weights_init=w_init)
        # Scale output to -action_bound to action_bound
        scaled_out = tf.multiply(out, self.action_bound)
        return inputs, out, scaled_out

    def train(self, inputs, a_gradient):
        self.sess.run(self.optimize, feed_dict={
            self.inputs: inputs,
            self.action_gradient: a_gradient
        })

    def predict(self, inputs):
        return self.sess.run(self.scaled_out, feed_dict={
            self.inputs: inputs
        })

    def predict_target(self, inputs):
        return self.sess.run(self.target_scaled_out, feed_dict={
            self.target_inputs: inputs
        })

    def update_target_network(self):
        self.sess.run(self.update_target_network_params)

    def get_num_trainable_vars(self):
        return self.num_trainable_vars
    
    # def load_network(self):
    #     self.saver = tf.train.Saver()
    #     checkpoint = tf.train.get_checkpoint_state("saved_actor_networks")
    #     if checkpoint and checkpoint.model_checkpoint_path:
    #         self.saver.restore(self.sess, checkpoint.model_checkpoint_path)
    #         print ("Successfully loaded:", checkpoint.model_checkpoint_path)
    #     else:
    #         print ("Could not find old actor network weights")

    def load_network(self):
        load_path = 'saved_actor_networks/'
        load_start = time()        
        self.saver = tf.train.Saver(max_to_keep=None)
        checkpoint = tf.train.get_checkpoint_state(load_path)
        # print('checkpoint = ++++++++++++++++++++++   ', checkpoint)
        # print('checkpoint = ++++++++++++++++++++++   ', tf.train.latest_checkpoint('saved_critic_networks'))
        if checkpoint and checkpoint.model_checkpoint_path:
            self.saver.restore(self.sess, checkpoint.model_checkpoint_path)
            print ("Load actor-network in %.1f" %(time() - load_start), "seconds. Path: %s" %load_path)
        else:
            print ("________Could not find old critic network weights")


    # def load_network(self):
    #     checkpoint_path = 'saved_actor_networks'
    #     self.saver = tf.train.Saver(max_to_keep=None)
    #     # self.saver = tf.train.import_meta_graph('saved_actor_networks/'+'actor-network.meta')
    #     # self.saver.restore(self.sess, tf.train.latest_checkpoint('saved_actor_networks'))
    #     ckpt = tf.train.get_checkpoint_state('saved_actor_networks')
    #     self.saver.restore(self.sess, ckp.model_checkpoint_path)
    #     print("_____________!!!!!!!!!!!!!Successfully loaded Saved Actor Networks!!!!!")
    #     # if checkpoint and checkpoint.model_checkpoint_path:
    #     #     self.saver.restore(self.sess, checkpoint.model_checkpoint_path)
    #     #     print ("Successfully loaded:", checkpoint.model_checkpoint_path)
    #     # else:
    #     #     print ("Could not find old actor network weights")
	
    # def save_network(self,time_step):
    #     self.saver = tf.train.Saver()
    #     print ('_________save actor-network...',time_step)
    #     self.saver.save(self.sess, 'saved_actor_networks/' + 'actor-network', global_step = time_step)

    def save_network(self, step):
        save_path = 'saved_actor_networks/' + 'actor-network'
        save_start = time()
        self.saver = tf.train.Saver(max_to_keep=None)
        self.saver.save(self.sess, save_path ,global_step=step)
        print ("Save actor-network in %.1f" %(time() - save_start), "seconds. Path: %s" %save_path)
