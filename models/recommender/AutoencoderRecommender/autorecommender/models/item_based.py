import pandas as pd
import numpy as np
from ..data import Dataset

from sklearn.metrics.pairwise import cosine_similarity, linear_kernel, polynomial_kernel


def encode_tags(df, column, sep='|'):
    return df[column].str.split(sep, expand=True).stack().str.get_dummies().groupby(level=0).sum()


class ItemSimilarity(object):

    def __init__(self, distance='cosine'):
        """
        Create an item similarity model.

        :param distance: Specify the distance kernel to use. One of 'cosine', 'linear', or 'polynomial'.
        """
        self._distance = distance
        self._sim = None
        self._mean_0 = None
        self._mean_i = None
        self._max_val = None
        self._min_val = None
        self._items = None

    def _similarity(self, X):
        s = None
        if self._distance == 'cosine':
            s = cosine_similarity(X)
        if self._distance == 'linear':
            s = linear_kernel(X)
            s = s/s.max(axis=1).reshape(-1, 1)
        if self._distance == 'polynomial':
            s = polynomial_kernel(X)
            s = s/s.max(axis=1).reshape(-1, 1)

        return pd.DataFrame(s, index=X.index, columns=X.index)

    def fit(self, dataset, column='genre', sep='|'):
        """
        "Fit" this model. (Computes the item similarity matrix and normalization vectors.)

        :param dataset: The dataset to fit.
        :param column: The name of the tag column to use for computing similarity.
        :param sep:
        :return:
        """
        self._items = dataset.items
        self._mean_0 = dataset.mean_0
        self._mean_i = dataset.mean_i
        self._max_val = dataset.max_val
        self._min_val = dataset.min_val

        tags = encode_tags(dataset.items, column, sep)

        self._sim = self._similarity(tags).fillna(0)

    def raw_predict(self, X):
        w = (X != 0).astype(int)
        preds = X.dot(self._sim)
        den = w.dot(self._sim)
        den[den == 0] = 1.0
        preds = preds/den
        return preds

    def predict(self, ratings, null=False):
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
                          mean_i=self._mean_i)

        pm = dataset._make_prefmatrix()
        X = np.array(pm)
        preds = self.raw_predict(X)

        if null:
            preds = np.zeros_like(preds)

        preds = pd.DataFrame(preds, index=pm.index, columns=pm.columns)

        preds[preds > 1.0] = 1.0
        preds[preds < -1.0] = -1.0

        preds = (preds + 1.0)/2.0

        preds = preds*(self._max_val - self._min_val) + self._min_val
        preds = preds + self._mean_0 + self._mean_i
        preds = preds.add(dataset.mean_u, axis=0)

        return preds


