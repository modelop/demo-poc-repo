import numpy as np
import pandas as pd
import zipfile
import pickle
import os

import tensorflow as tf

from keras.layers import Input, Dense, Lambda
from keras.models import Model
from keras.models import load_model as keras_load_model
from keras import losses
from keras.callbacks import EarlyStopping

from ..data import Dataset


def lambda_mse(frac=1.0):
    """
    Specialized loss function for recommender model.

    :param frac: Proportion of weight to give to novel ratings.
    :return: A loss function for use in a Lambda layer.
    """
    def lossfunc(xarray):
        x_in, y_true, y_pred = xarray
        zeros = tf.zeros_like(y_true)

        novel_mask = tf.not_equal(x_in, y_true)
        known_mask = tf.not_equal(x_in, zeros)

        y_true_1 = tf.boolean_mask(y_true, novel_mask)
        y_pred_1 = tf.boolean_mask(y_pred, novel_mask)

        y_true_2 = tf.boolean_mask(y_true, known_mask)
        y_pred_2 = tf.boolean_mask(y_pred, known_mask)

        unknown_loss = losses.mean_squared_error(y_true_1, y_pred_1)
        known_loss = losses.mean_squared_error(y_true_2, y_pred_2)

        # remove nans
        unknown_loss = tf.where(tf.is_nan(unknown_loss), 0.0, unknown_loss)

        return frac*unknown_loss + (1.0 - frac)*known_loss
    return lossfunc


def final_loss(y_true, y_pred):
    """
    Dummy loss function for wrapper model.
    :param y_true: true value (not used, but required by Keras)
    :param y_pred: predicted value
    :return: y_pred
    """
    return y_pred


class Autoencoder(object):

    def __init__(self,
                 item_count,
                 encoding_dim=25,
                 scale_factor=2,
                 activation='selu',
                 deep=True,
                 optimizer='adadelta',
                 loss_frac=1.0):
        """

        :param item_count: Number of items in the universe.
        :param encoding_dim: Number of latent factors for the recommender.
        :param scale_factor: If deep=True, intermediate layers will have dim scale_factor*encoding_dim
        :param activation: Activation function (default: selu)
        :param deep: If true, have 3 hidden layers. If false, just one.
        :param optimizer: Optimizer.
        :param loss_frac: Number between 0 and 1 to scale loss on masked items vs known ratings.
        """

        self._item_count = item_count
        self._encoding_dim = encoding_dim
        self._scale_factor = scale_factor
        self._activation = activation
        self._deep = deep
        self._optimizer = optimizer
        self._loss_frac = loss_frac

        # ~~~~~ build recommender, ~~~~~ #
        input_layer = Input(shape=(self._item_count, ))

        if self._deep:
            encoded = Dense(self._scale_factor*self._encoding_dim, activation=self._activation)(input_layer)
            encoded = Dense(self._encoding_dim, activation=self._activation)(encoded)

            decoded = Dense(self._scale_factor*self._encoding_dim, activation=self._activation)(encoded)
            decoded = Dense(self._item_count, activation='tanh')(decoded)

            self.recommender = Model(input_layer, decoded)
            self.encoder = Model(input_layer, encoded)

            encoded_input = Input(shape=(self._encoding_dim, ))

            self.decoder = Model(encoded_input, self.recommender.layers[-1](
                self.recommender.layers[-2](encoded_input)
                ))

        else:

            encoded = Dense(self._encoding_dim, activation=self._activation)(input_layer)
            decoded = Dense(self._item_count, activation='tanh')(encoded)

            self.recommender = Model(input_layer, decoded)

            self.encoder = Model(input_layer, encoded)
            encoded_input = Input(shape=(self._encoding_dim, ))
            self.decoder = Model(encoded_input, self.recommender.layers[-1](encoded_input))

        # ~~~~~ build wrapper model ~~~~~ #

        original_inputs = self.recommender.input
        y_true_inputs = Input(shape=(self._item_count, ))
        original_outputs = self.recommender.output
        loss = Lambda(lambda_mse(loss_frac))([original_inputs, y_true_inputs, original_outputs])

        self.wrapper_model = Model(inputs=[original_inputs, y_true_inputs], outputs=[loss])
        self.wrapper_model.compile(optimizer=optimizer, loss=final_loss)

        # ~~~~~ statistics & training data ~~~~~ #
        self.history = None
        self._mean_0 = None
        self._mean_i = None
        self._max_val = None
        self._min_val = None
        self._items = None

    def fit(self, dataset, epochs=1, batch_size=64, mask_fraction=0.2,
            verbose=1, validation_data=None, patience=0):
        """
        Fit this model on the specified dataset.

        :param dataset: The training dataset.
        :param epochs: Number of epochs to train for.
        :param batch_size: Size of each training batch.
        :param mask_fraction: Fraction of item ratings to mask to create model inputs.
        :param verbose: 0 = silent, 1 = live update, 2 = update at end of epoch
        :param validation_data: If not None, pass a Dataset object to use for validation
        :param patience: if > 0, stop training after this many epochs with no improvement in loss.
        :return: The history associated to this training session.
        """

        self._mean_0 = dataset.mean_0
        self._mean_i = dataset.mean_i.fillna(dataset.mean_i.mean()) # fill any missings
        self._max_val = dataset.max_val
        self._min_val = dataset.min_val
        self._items = dataset.items

        monitor = 'loss' if validation_data is None else 'val_loss'
        stopper = EarlyStopping(monitor=monitor, min_delta=0.00001, patience=patience, verbose=1)

        callbacks = [stopper] if patience > 0 else []

        batches_per_epoch = int(np.floor(len(dataset.users)/batch_size))

        generator = dataset.generate(batch_size, mask_fraction)

        validation_generator = None
        validation_steps = None
        if validation_data is not None:
            validation_generator = validation_data.generate(batch_size, mask_fraction)
            validation_steps = int(np.floor(len(validation_data.users)/batch_size))

        self.history = self.wrapper_model.fit_generator(
            generator,
            steps_per_epoch=batches_per_epoch,
            validation_data=validation_generator,
            validation_steps=validation_steps,
            epochs=epochs,
            verbose=verbose,
            callbacks=callbacks
        )

        return self.history

    def raw_predict(self, X):
        return self.recommender.predict(X)

    def predict(self, ratings, null=False):
        """
        Predict new ratings with this model.

        :param ratings: Input ratings. Assumed to be indexed with multiindex (user, item) : rating.
        :param null: If True, returns only the baseline mean values, not recommender adjustments.
                     (Useful for debugging.)
        :return: A matrix whose ijth entry is user i's predicted rating of item j.
        """

        userid = ratings.index.names[0]
        itemid = ratings.index.names[1]

        dataset = Dataset(items=self._items,
                          users=None,
                          ratings=ratings,
                          userid=userid,
                          itemid=itemid,
                          ratingid=ratings.columns[0],
                          max_val=self._max_val,
                          min_val=self._min_val,
                          mean_0=self._mean_0,
                          mean_i=self._mean_i
                          )

        X = dataset._make_prefmatrix()

        preds = self.raw_predict(X)
        if null is True:
            preds = np.zeros_like(preds)

        # clamp to within [-1.0, 1.0]

        preds[preds > 1.0] = 1.0
        preds[preds < -1.0] = -1.0

        preds = pd.DataFrame(preds, index=X.index, columns=X.columns)

        preds = (preds + 1.0)/2.0 # [-1, 1] -> [0, 1]
        preds = preds*(self._max_val - self._min_val) + self._min_val

        preds = preds + self._mean_0 + self._mean_i
        preds = preds.add(dataset.mean_u, axis=0)

        return preds

    def save(self, filepath):
        """
        Save the model to a zip archive. Note: probably useless if the model is not
        trained.

        :param filepath: Path to the zip file.
        """
        attrs = {'mean_0': self._mean_0,
                 'mean_i': self._mean_i,
                 'max_val': self._max_val,
                 'min_val': self._min_val,
                 'item_count': self._item_count,
                 'items': self._items,
                 'encoding_dim': self._encoding_dim,
                 'scale_factor': self._scale_factor,
                 'deep': self._deep,
                 'optimizer': self._optimizer,
                 'activation': self._activation,
                 'loss_frac': self._loss_frac}

        with open('_attrs.pkl', 'wb') as f:
            pickle.dump(attrs, f)
        self.recommender.save_weights('_recommender.hdf5')

        zf = zipfile.ZipFile(filepath, 'w')
        zf.write('_attrs.pkl', compress_type=zipfile.ZIP_DEFLATED)
        zf.write('_recommender.hdf5')
        zf.close()

        os.remove('_attrs.pkl')
        os.remove('_recommender.hdf5')

def load_model(filepath):
    """
    Load a model from a zip archive.

    :param filepath: Path to a zip archive created with Autorecommender.save
    :return: A trained Autorecommender object
    """
    zf = zipfile.ZipFile(filepath, 'r')
    zf.extractall('.')
    zf.close()

    with open('_attrs.pkl', 'rb') as f:
        attrs = pickle.load(f)

    model = Autoencoder(
        item_count=attrs['item_count'],
        encoding_dim=attrs['encoding_dim'],
        scale_factor=attrs['scale_factor'],
        activation=attrs['activation'],
        deep=attrs['deep'],
        optimizer=attrs['optimizer'],
        loss_frac=attrs['loss_frac']
    )

    model.recommender.load_weights('_recommender.hdf5')

    os.remove('_recommender.hdf5')
    os.remove('_attrs.pkl')

    model._mean_0 = attrs['mean_0']
    model._mean_i = attrs['mean_i']
    model._max_val = attrs['max_val']
    model._min_val = attrs['min_val']
    model._items = attrs['items']

    return model
