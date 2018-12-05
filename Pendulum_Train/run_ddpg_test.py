""" 
Implementation of DDPG - Deep Deterministic Policy Gradient

Algorithm and hyperparameter details can be found here: 
    http://arxiv.org/pdf/1509.02971v2.pdf

The algorithm is tested on the Pendulum-v0 OpenAI gym task 
and developed with tflearn + Tensorflow

Author: Patrick Emami
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
import numpy as np
import gym
from gym import wrappers
import tflearn
import argparse
import pprint as pp

from replay_buffer import ReplayBuffer

from actor_network import ActorNetwork
from critic_network import CriticNetwork
from Ornstein_Uhlenbeck_Action_Noise import OrnsteinUhlenbeckActionNoise
from ddpg_train import train
from ddpg_test import test


def main(args):

    with tf.Session() as sess:

        env = gym.make(args['env'])
        np.random.seed(int(args['random_seed']))
        tf.set_random_seed(int(args['random_seed']))
        env.seed(int(args['random_seed']))

        state_dim = env.observation_space.shape[0]
        # print("state_dim = ",state_dim)
        action_dim = env.action_space.shape[0]
        # print("action_dim = ",action_dim)
        action_bound = env.action_space.high
        # print("action_bound =", action_bound)
        # Ensure action bound is symmetric
        assert (env.action_space.high == -env.action_space.low)

        actor = ActorNetwork(sess, state_dim, action_dim, action_bound,
                             float(args['actor_lr']), float(args['tau']),
                             int(args['minibatch_size']))

        critic = CriticNetwork(sess, state_dim, action_dim,
                               float(args['critic_lr']), float(args['tau']),
                               float(args['gamma']),
                               actor.get_num_trainable_vars())

        # Load network weights
        actor.load_network()
        critic.load_network()
        
        actor_noise = OrnsteinUhlenbeckActionNoise(mu=np.zeros(action_dim))

        if args['use_gym_monitor']:
            if not args['render_env']:
                env = wrappers.Monitor(
                    # env, args['monitor_dir'], video_callable=False, force=True)
                    env, args['monitor_dir'], force=True)
                    # env, args['monitor_dir'], video_callable=False, force=True, resume=True, mode='training')
            else:
                env = wrappers.Monitor(env, args['monitor_dir'], force=True)
                # env = wrappers.Monitor(env, args['monitor_dir'], force=True, resume=True,mode='training')

        test(sess, env, args, actor, critic, actor_noise)

        if args['use_gym_monitor']:
            # env.monitor.close()
            env.env.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='provide arguments for DDPG agent')

    # agent parameters
    parser.add_argument('--actor-lr', help='actor network learning rate', default=0.0001)
    parser.add_argument('--critic-lr', help='critic network learning rate', default=0.001)
    parser.add_argument('--gamma', help='discount factor for critic updates', default=0.99)
    parser.add_argument('--tau', help='soft target update parameter', default=0.001)
    parser.add_argument('--buffer-size', help='max size of the replay buffer', default=1000000)
    parser.add_argument('--minibatch-size', help='size of minibatch for minibatch-SGD', default=64)

    # run parameters
    parser.add_argument('--env', help='choose the gym env- tested on {Pendulum-v0}', default='Pendulum-v0')
    parser.add_argument('--random-seed', help='random seed for repeatability', default=1234)
    parser.add_argument('--test-max-episodes', help='max num of episodes to do while training', default=1)
    # parser.add_argument('--max-episodes', help='max num of episodes to do while training', default=1)
    # parser.add_argument('--max-episode-len', help='max length of 1 episode', default=10)
    parser.add_argument('--test-max-episode-len', help='max length of 1 episode', default=1000)
    parser.add_argument('--render-env', help='render the gym env', action='store_true')
    parser.add_argument('--use-gym-monitor', help='record gym results', action='store_true')
    parser.add_argument('--monitor-dir', help='directory for storing gym results', default='./results/gym_ddpg')
    parser.add_argument('--train-summary-dir', help='directory for storing tensorboard info', default='./train_results/tf_ddpg')
    parser.add_argument('--test-summary-dir', help='directory for storing tensorboard info', default='./test_results/tf_ddpg')
    parser.add_argument('--use-trained-model', help='use trained mode or not', default=False)



    parser.set_defaults(render_env=False)
    parser.set_defaults(use_gym_monitor=True)
    parser.set_defaults(use_trained_model = True)
    
    args = vars(parser.parse_args())
    
    pp.pprint(args)

    main(args)
