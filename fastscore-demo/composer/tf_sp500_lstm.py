# fastscore.schema.0: double
# fastscore.schema.1: double
# fastscore.module-attached: tensorflow

import tensorflow as tf
import numpy as np

def begin():
    tf.logging.set_verbosity(tf.logging.WARN)
    global past_days
    past_days = []

    global n_steps, X, outputs, sess
    n_steps = 30
    n_inputs = 1
    n_outputs = 1
    n_layers = 3
    n_units = 100
    save_name = 'tf_sp500_lstm'

    X = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
    y = tf.placeholder(tf.float32, [None, n_steps, n_outputs])
    layers = [tf.contrib.rnn.BasicLSTMCell(num_units = n_units) for k in range(n_layers)]
    cell = tf.contrib.rnn.OutputProjectionWrapper(
      tf.contrib.rnn.MultiRNNCell(layers), output_size = n_outputs)
    outputs, states = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)
    saver = tf.train.Saver()
    sess = tf.Session()
    saver.restore(sess, './{}'.format(save_name))

def predict(inputs):
    if len(inputs[0,:,0]) < n_steps:
        raise Exception("Insufficient inputs! X should be an array of shape (1, k, 1) where k >= n_steps")

    preds = []
    steps_forward = len(inputs[0,:,0]) - n_steps + 1
    for j in range(0, steps_forward):
        X_in = inputs[:,j:j+n_steps,:]
        y_pred = sess.run(outputs, feed_dict = {X: X_in})
        preds.append(y_pred[0,-1,0]) # add the last one
    return np.array(preds).reshape(-1, len(preds), 1)

def action(x):
    global past_days
    past_days.append(x)
    past_days = past_days[-n_steps:]
    if len(past_days) == n_steps:
        result = predict(np.array(past_days).reshape(-1, n_steps, 1))[0, 0, 0]
        yield np.asscalar(result)
    else:
        yield x

def end():
    sess.close()
