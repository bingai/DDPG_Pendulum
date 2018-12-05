import numpy as np
from build_summaries import *
from replay_buffer import ReplayBuffer
import time
# ===========================
#   Agent Training
# ===========================

def train(sess, env, args, actor, critic, actor_noise):

    # Set up summary Ops
    summary_ops, summary_vars = build_summaries()

    sess.run(tf.global_variables_initializer())
    writer = tf.summary.FileWriter(args['train_summary_dir'], sess.graph)

    ############################################
    # load actor checkpoints
    actor_ckpt = tf.train.get_checkpoint_state("saved_actor_networks")
    critic_ckpt = tf.train.get_checkpoint_state("saved_critic_networks")

    # resume training if a checkpoint exists
    if actor_ckpt and actor_ckpt.model_checkpoint_path and critic_ckpt and critic_ckpt.model_checkpoint_path :
        actor.load_network()
        print("Loaded Actor Network from {}".format(actor_ckpt.model_checkpoint_path))
        critic.load_network()
        print("Loaded Critic Network from {}".format(critic_ckpt.model_checkpoint_path))

    # Initialize target network weights
    actor.update_target_network()
    critic.update_target_network()

    # Initialize replay memory
    replay_buffer = ReplayBuffer(int(args['buffer_size']), int(args['random_seed']))

    # Needed to enable BatchNorm. 
    # This hurts the performance on Pendulum but could be useful
    # in other environments.
    # tflearn.is_training(True)

    for i in range(int(args['max_episodes'])):

        s = env.reset()

        ep_reward = 0
        ep_ave_max_q = 0
        # print("________New Episode:")
        # time.sleep(1)
        

        for j in range(int(args['max_episode_len'])):

            if args['render_env']:
                env.render()

            # Added exploration noise
            #a = actor.predict(np.reshape(s, (1, 3))) + (1. / (1. + i))
            a = actor.predict(np.reshape(s, (1, actor.s_dim))) + actor_noise()

            s2, r, terminal, info = env.step(a[0])
            print('TRAINING...  | episode_len: {:d}     | Episode: {:d} '.format(j, i))
            # time.sleep(1)

            replay_buffer.add(np.reshape(s, (actor.s_dim,)), np.reshape(a, (actor.a_dim,)), r,
                              terminal, np.reshape(s2, (actor.s_dim,)))

            # Keep adding experience to the memory until
            # there are at least minibatch size samples
            if replay_buffer.size() > int(args['minibatch_size']):
                s_batch, a_batch, r_batch, t_batch, s2_batch = \
                    replay_buffer.sample_batch(int(args['minibatch_size']))

                # Calculate targets
                target_q = critic.predict_target(
                    s2_batch, actor.predict_target(s2_batch))

                y_i = []
                for k in range(int(args['minibatch_size'])):
                    if t_batch[k]:
                        y_i.append(r_batch[k])
                    else:
                        y_i.append(r_batch[k] + critic.gamma * target_q[k])

                # Update the critic given the targets
                predicted_q_value, _ = critic.train(
                    s_batch, a_batch, np.reshape(y_i, (int(args['minibatch_size']), 1)))

                ep_ave_max_q += np.amax(predicted_q_value)

                # Update the actor policy using the sampled gradient
                a_outs = actor.predict(s_batch)
                grads = critic.action_gradients(s_batch, a_outs)
                actor.train(s_batch, grads[0])

                # Update target networks
                actor.update_target_network()
                critic.update_target_network()

            s = s2
            ep_reward += r
            # if i % 5 == 0:
            #     # print("++++++++++++++++++save!!!!")
            #     actor.save_network()
            #     critic.save_network()

            if terminal:

                summary_str = sess.run(summary_ops, feed_dict={
                    summary_vars[0]: ep_reward,
                    summary_vars[1]: ep_ave_max_q / float(j)
                })

                writer.add_summary(summary_str, i)
                writer.flush()
                print('| Reward: {:d} | episode_len: {:d} | Episode: {:d} | Qmax: {:.4f}'.format(int(ep_reward), \
                        j, i, (ep_ave_max_q / float(j))))
                # if i % 5 == 0:
                #     # print("++++++++++++++++++save!!!!")
                #     actor.save_network()
                #     critic.save_network()

                break
        if i % 5 == 0:
            # print("++++++++++++++++++save!!!!")
            actor.save_network(i)
            critic.save_network(i)