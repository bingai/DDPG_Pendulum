import gym
import time
env = gym.make('Pendulum-v0')
# env = gym.make('CartPole-v0')
env.reset()
for i in range(1000):
    env.render()
    print("i = ", i)
    # time.sleepenv(0.1)
    s2, r, terminal, info = env.step(env.action_space.sample()) # take a random action
    if terminal:
        print('______DONE!!!, i = {:d}'.format(i))
        # time.sleep(20)
        break

