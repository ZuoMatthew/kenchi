from unittest import TestCase

import numpy as np
from sklearn.exceptions import NotFittedError
from sklearn.model_selection import ParameterGrid

from kenchi import VMFDetector


class VMFDetectorTest(TestCase):
    def setUp(self):
        train_size   = 1000
        test_size    = 100
        n_outliers   = 10
        n_features   = 10

        rnd          = np.random.RandomState(0)

        mean         = np.zeros(n_features)
        cov          = np.eye(n_features)

        self.X_train = rnd.multivariate_normal(mean, cov, train_size)

        self.X_test  = np.concatenate((
            rnd.multivariate_normal(mean, cov, test_size - n_outliers),
            rnd.uniform(-10.0, 10.0, size=(n_outliers, n_features))
        ))

        self.y_test  = np.concatenate((
            np.zeros(test_size - n_outliers, dtype=np.int32),
            np.ones(n_outliers, dtype=np.int32)
        ))

        self.sut     = VMFDetector()

    def test_fit(self):
        self.assertIsInstance(self.sut.fit(self.X_train), VMFDetector)

    def test_predict_with_notfitted(self):
        with self.assertRaises(NotFittedError):
            self.sut.predict(self.X_train)

    def test_score(self):
        param_grid = {'assume_normalized': [False, True], 'fpr': [0.1]}

        for params in ParameterGrid(param_grid):
            with self.subTest(**params):
                self.sut.set_params(**params).fit(self.X_train)

                self.assertGreater(
                    self.sut.score(self.X_test, self.y_test), 0.0
                )
