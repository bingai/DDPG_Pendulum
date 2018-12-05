# import gym
# env = gym.make('CartPole-v0')
# env = gym.wrappers.Monitor(env, "recording")
# env.monitor.start('./tmp/cartpole-experiment-1')
# for i_episode in xrange(20):
#     observation = env.reset()
#     for t in xrange(100):
#         env.render()
#         print (observation)
#         action = env.action_space.sample()
#         observation, reward, done, info = env.step(action)
#         if done:
#             print ("Episode finished after {:d} timesteps".format(t+1))
#             break

# env.monitor.close()
# # print('| Reward: {:d} | Episode: {:d} | Qmax: {:.4f}'.format(int(ep_reward), \
# #                         i, (ep_ave_max_q / float(j))))
# import numpy as np
# import time
# import gym
# from gym import wrappers
# env = gym.make('Pendulum-v0')
# env = wrappers.Monitor(env, './tmp/Pendulum-v0',force=True)
# accreward = 0
# for i_episode in range(1):
#     observation = env.reset()
#     for t in range(50000):
#         env.render()
#         print("_____observation before action:", observation)
#         action = env.action_space.sample()
#         print("action = ", action)
#         observation, reward, done, info = env.step(action)
#         print("+++++observation after action:", observation)
#         accreward += reward
#         print("accreward = ", accreward)
#         print("done", done)
#         if done:
#             print("Episode finished after {} timesteps".format(t+1))
#             print("****************DONE!!!","accreward = ", accreward)
#             time.sleep(10)
#             break
# env.close()
# # gym.upload('./tmp/Pendulum-v0', api_key='')


# import gym
# env = gym.make('Pendulum-v0')
# env.reset()
# total_reward = 0
# for t in range(200):
#     env.render()
#     action = env.action_space.sample()
#     print("action :", action)
#     observation, reward, done, info = env.step(action) # take a random action
#     print("observation :", observation)
#     total_reward += reward
#     print("total_reward :", total_reward)
#     print("DONE_________", done)
#     # print("+++++++++++++info:", info)
#     if done:
#         print("Episode finished after {} timesteps".format(t+1))
#         print("****************DONE!!!","total_reward = ", total_reward)
#         time.sleep(10)
#         break


import gym
env = gym.make('Pendulum-v0')
env.reset()
total_reward = 0
t =0
while True:
    t += 1
    env.render()
    action = env.action_space.sample()
    print("action :", action)
    observation, reward, done, info = env.step(action) # take a random action
    print("observation :", observation)
    total_reward += reward
    print("total_reward :", total_reward)
    print("DONE_________", done)
    # print("+++++++++++++info:", info)
    if done:
        print("Episode finished after {} timesteps".format(t+1))
        print("****************DONE!!!","total_reward = ", total_reward)
        time.sleep(10)
        break
