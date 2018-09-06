import numpy as np
import pandas as pd


class Dataset(object):

    def __init__(self, items, users, ratings,
                 userid='userid',
                 itemid='movieid',
                 ratingid='rating',
                 max_val=None,
                 min_val=None,
                 mean_0=None,
                 mean_i=None,
                 mean_u=None):
        self._items = items
        self._users = users
        self._ratings = ratings
        self._userid = userid
        self._itemid = itemid
        self._ratingid = ratingid
        self._mean_0 = mean_0
        self._mean_i = mean_i
        self._mean_u = mean_u
        self._max_val = max_val
        self._min_val = min_val
        self._prefs = None

    @property
    def ratings(self):
        """
        :return: Dataframe with raw user-item ratings.
        """
        return self._ratings

    @property
    def users(self):
        """
        :return: Dataframe with user data.
        """
        return self._users

    @property
    def items(self):
        """
        :return: Dataframe with item data.
        """
        return self._items

    @property
    def preferences(self):
        """
        :return: Normalized user preferences dataframe.
        """
        if self._prefs is None:
            self._compute_prefs()
        return self._prefs

    @property
    def mean_0(self):
        """
        :return: mean_0 normalization factor (average of all ratings)
        """
        if self._mean_0 is None:
            self._compute_prefs()
        return self._mean_0

    @property
    def mean_i(self):
        """
        :return: mean_i normalization vector (average normalized rating per movie)
        """
        if self._mean_i is None:
            self._compute_prefs()
        return self._mean_i

    @property
    def mean_u(self):
        """
        :return: mean_u normalization vector (average normalized rating per user)
        """
        if self._mean_u is None:
            self._compute_prefs()
        return self._mean_u

    @property
    def max_val(self):
        if self._max_val is None:
            self._compute_prefs()
        return self._max_val

    @property
    def min_val(self):
        if self._min_val is None:
            self._compute_prefs()
        return self._min_val

    def _compute_prefs(self):
        prefs = self._ratings[self._ratingid]
        mean_0 = prefs.mean() if self._mean_0 is None else self._mean_0
        prefs = prefs - mean_0 # subtract off the mean
        item_mean = prefs.groupby(self._itemid).mean() if self._mean_i is None else self._mean_i
        mean_i = pd.Series(index=self.items.index).fillna(0) + item_mean
        prefs = prefs - mean_i
        mean_u = prefs.groupby(self._userid).mean() if self._mean_u is None else self._mean_u
        prefs = prefs - mean_u

        max_val = prefs.max() if self._max_val is None else self._max_val
        min_val = prefs.min() if self._min_val is None else self._min_val

        prefs = 2*(prefs - min_val)/(max_val - min_val) - 1 # normalize to between -1 and 1

        self._max_val = max_val
        self._min_val = min_val
        self._mean_0 = mean_0
        self._mean_i = mean_i
        self._mean_u = mean_u
        self._prefs = prefs

    def train_test_split(self, frac=0.8):
        """
        Split this dataset into training and testing datasets.
        :param frac: The fraction of the data to use for training.
        :return: A tuple of Dataset objects (train, test) with no users in common.
        """
        userids = np.array(self._users.index.unique())
        np.random.shuffle(userids)

        train_userids = userids[0:int(frac*len(userids))]
        test_userids = userids[int(frac*len(userids)):]

        # _ratings.loc[userids] is slow, user an alternative

        df = self._ratings.reset_index()

        train_ratings = df[df[self._userid].isin(train_userids)].set_index([self._userid, self._itemid]).sort_index()
        test_ratings = df[df[self._userid].isin(test_userids)].set_index([self._userid, self._itemid]).sort_index()

        udf = self._users.reset_index()
        train_users = udf[udf[self._userid].isin(train_userids)].set_index(self._userid).sort_index()
        test_users = udf[udf[self._userid].isin(test_userids)].set_index(self._userid).sort_index()

        if self._max_val is None or self._min_val is None:
            self._compute_prefs()

        train_dataset = Dataset(self._items, train_users, train_ratings, self._userid, self._itemid, self._ratingid,
                                max_val=self._max_val, min_val=self._min_val)

        test_dataset = Dataset(self._items, test_users, test_ratings, self._userid, self._itemid, self._ratingid,
                                max_val=self._max_val, min_val=self._min_val,
                                mean_0=train_dataset.mean_0, mean_i=train_dataset.mean_i)

        return train_dataset, test_dataset

    def _make_dummy_user(self):
        df = self.items.reset_index()[[self._itemid]].copy()
        df[self._userid] = -99999
        df[self._ratingid] = 0
        return df

    def _make_prefmatrix(self, userslice=None):
        df = None
        if userslice is None:
            df = pd.DataFrame({self._ratingid: self.preferences}).reset_index()
        else:
            df = pd.DataFrame({self._ratingid: self.preferences}).reset_index()
            df = df[df[self._userid].isin(userslice)]
        df = df.append(self._make_dummy_user(), sort=True)
        df = df.sort_values(by=self._userid)
        df = df.pivot(index=self._userid, columns=self._itemid, values=self._ratingid).iloc[1:] # drop dummy user
        df = df.fillna(0)
        return df

    def generate(self, batch_size=64, mask_fraction=0.2, repeat=1):
        """
        Generate training triplets from this dataset.

        :param batch_size: Size of each training data batch.
        :param mask_fraction: Fraction of ratings in training data input to mask. 0.2 = hide 20% of input ratings.
        :param repeat: Steps between shuffles.
        :return: A generator that returns tuples of the form ([X, y], zeros) where X, y, and zeros all have
                 shape[0] = batch_size. X, y are training inputs for the recommender.
        """

        def select_and_mask(frac):
            def applier(row):
                row = row.copy()
                idx = np.where(row != 0)[0]
                masked = np.random.choice(idx, size=(int)(frac*len(idx)), replace=False)
                row[masked] = 0
                return row
            return applier

        indices = np.array(self._users.index.unique())
        batches_per_epoch = int(np.floor(len(indices)/batch_size))
        while True:
            np.random.shuffle(indices)

            for _ in range(0, repeat):
                for batch in range(0, batches_per_epoch):
                    idx = indices[batch*batch_size:(batch+1)*batch_size]

                    y = np.array(self._make_prefmatrix(idx))
                    X = np.apply_along_axis(select_and_mask(frac=mask_fraction), axis=1, arr=y)

                    yield [X, y], np.zeros(batch_size)


def ratings_matrix_to_list(matrix, ratingid='rating'):
    """
    Convert a ratings matrix into a ratings list.

    :param matrix: A matrix whose (i,j)th element is user i's rating of item j.
    :param ratingid: The name to use for the rating column.
    :return: A dataframe whose index is (user, item) and column is the ratings.
    """
    return pd.DataFrame(matrix.transpose().unstack().fillna(0), columns=[ratingid])
