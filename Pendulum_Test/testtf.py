import tensorflow as tf

p = tf.placeholder(tf.float32, shape=[], name="p")
v2 = tf.Variable(2. , name="v2")
a = tf.add(p, v2)

with tf.Session() as sess:
  sess.run(tf.global_variables_initializer())
  # From the moment we initiliaze variables, until the end of the Session's scope
  # We can access variables
  print(sess.run(v2)) # -> 2.

  # On the other hand, intermediate tensors has to be recalculated 
  # each time you want to access its value
  print(sess.run(a, feed_dict={p: 3})) # -> 5.

  # Even if calculated once, the value of a is no more accessible
  # the value of a has been freed off the memory
  try:
    # print(sess.run(a, feed_dict={p: 3})) # -> 5.
    sess.run(a) # Error: "You must feed a value for placeholder tensor 'p' with dtype float"
    # sess.run(a, feed_dict={p: 3})
  except Exception as e:
    print(e)