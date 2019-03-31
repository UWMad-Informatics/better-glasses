from __future__ import unicode_literals, division, print_function

import unittest
import pandas as pd
import numpy as np
import warnings

from pymatgen.util.testing import PymatgenTest
from sklearn.dummy import DummyRegressor, DummyClassifier

from matminer.featurizers.base import BaseFeaturizer, MultipleFeaturizer, StackedFeaturizer
from matminer.featurizers.function import FunctionFeaturizer


class SingleFeaturizer(BaseFeaturizer):
    def feature_labels(self):
        return ['y']

    def featurize(self, x):
        return [x + 1]

    def citations(self):
        return ["A"]

    def implementors(self):
        return ["Us"]


class SingleFeaturizerMultiArgs(SingleFeaturizer):
    def featurize(self, *x):
        return [x[0] + x[1]]


class MultipleFeatureFeaturizer(BaseFeaturizer):
    def feature_labels(self):
        return ['w', 'z']

    def featurize(self, x):
        return [x - 1, x + 2]

    def citations(self):
        return ["A"]

    def implementors(self):
        return ["Them"]


class MatrixFeaturizer(BaseFeaturizer):
    def feature_labels(self):
        return ['representation']

    def featurize(self, *x):
        return [np.eye(2, 2)]

    def citations(self):
        return ["C"]

    def implementors(self):
        return ["Everyone"]


class MultiArgs2(SingleFeaturizerMultiArgs):
    def featurize(self, *x):
        # Making a 2D array to test whether MutliFeaturizer
        #  can handle featurizers that have both 1D vectors with
        #  singleton dimensions (e.g., shape==(4,1)) and those
        #  without (e.g., shape==(4,))
        return [super(MultiArgs2, self).featurize(*x)]

    def feature_labels(self):
        return ['y2']

class FittableFeaturizer(BaseFeaturizer):
    """
    This test featurizer tests fitting qualities of BaseFeaturizer, including
    refittability and different results based on different fits.
    """
    def fit(self, X, y=None, **fit_kwargs):
        self._features = ['a', 'b', 'c'][:len(X)]
        return self

    def featurize(self, x):
        return [x + 3, x + 4, 2 * x][:len(self._features)]

    def feature_labels(self):
        return self._features

    def citations(self):
        return ["Q"]

    def implementors(self):
        return ["A competing research group"]


class TestBaseClass(PymatgenTest):
    def setUp(self):
        self.single = SingleFeaturizer()
        self.multi = MultipleFeatureFeaturizer()
        self.matrix = MatrixFeaturizer()
        self.multiargs = SingleFeaturizerMultiArgs()
        self.fittable = FittableFeaturizer()

    @staticmethod
    def make_test_data():
        return pd.DataFrame({'x': [1, 2, 3]})

    def test_dataframe(self):
        data = self.make_test_data()
        data = self.single.featurize_dataframe(data, 'x')
        self.assertArrayAlmostEqual(data['y'], [2, 3, 4])

        data = self.multi.featurize_dataframe(data, 'x')
        self.assertArrayAlmostEqual(data['w'], [0, 1, 2])
        self.assertArrayAlmostEqual(data['z'], [3, 4, 5])

    def test_matrix(self):
        """Test the ability to add features that are matrices to a dataframe"""
        data = self.make_test_data()
        data = self.matrix.featurize_dataframe(data, 'x')
        self.assertArrayAlmostEqual(np.eye(2, 2), data['representation'][0])

    def test_inplace(self):
        data = self.make_test_data()
        self.single.featurize_dataframe(data, 'x', inplace=False)
        self.assertNotIn('y', data.columns)

        self.single.featurize_dataframe(data, 'x', inplace=True)
        self.assertIn('y', data)

    def test_indices(self):
        data = self.make_test_data()
        data.index = [4, 6, 6]

        data = self.single.featurize_dataframe(data, 'x')
        self.assertArrayAlmostEqual(data['y'], [2, 3, 4])

    def test_multiple(self):
        multi_f = MultipleFeaturizer([self.single, self.multi])
        data = self.make_test_data()

        self.assertArrayAlmostEqual([2, 0, 3], multi_f.featurize(1))

        self.assertArrayEqual(['A'], multi_f.citations())

        implementors = multi_f.implementors()
        self.assertIn('Us', implementors)
        self.assertIn('Them', implementors)
        self.assertEquals(2, len(implementors))

        # Ensure BaseFeaturizer operation without overriden featurize_dataframe
        with warnings.catch_warnings(record=True) as w:
            multi_f.featurize_dataframe(data, 'x')
            self.assertEqual(len(w), 0)
        self.assertArrayAlmostEqual(data['y'], [2, 3, 4])
        self.assertArrayAlmostEqual(data['w'], [0, 1, 2])
        self.assertArrayAlmostEqual(data['z'], [3, 4, 5])

        # Test handling of Featurizers with overloaded featurize_dataframe
        f = FunctionFeaturizer()
        multi_f = MultipleFeaturizer([self.single, self.multi, f])
        data = self.make_test_data()
        with warnings.catch_warnings(record=True) as w:
            multi_f.featurize_dataframe(data, 'x')
            self.assertEqual(len(w), 1)

    def test_multifeatures(self):
        # Make a test dataset with two input variables
        data = self.make_test_data()
        data['x2'] = [4, 5, 6]

        multiargs2 = MultiArgs2()

        # Create featurizer
        multi_f = MultipleFeaturizer([self.multiargs, multiargs2])

        # Test featurize with multiple arguments
        features = multi_f.featurize(0, 2)
        self.assertArrayAlmostEqual([2, 2], features)

        # Test dataframe
        data = multi_f.featurize_dataframe(data, ['x', 'x2'])
        self.assertEquals(['y', 'y2'], multi_f.feature_labels())
        self.assertArrayAlmostEqual([[5, 5], [7, 7], [9, 9]], data[['y', 'y2']])

    def test_featurize_many(self):

        # Single argument
        s = self.single
        s.set_n_jobs(2)
        mat = s.featurize_many([1, 2, 3])
        self.assertArrayAlmostEqual(mat, [[2], [3], [4]])

        # Multi-argument
        s = self.multiargs
        s.set_n_jobs(2)
        mat = s.featurize_many([[1, 4], [2, 5], [3, 6]])
        self.assertArrayAlmostEqual(mat, [[5], [7], [9]])

    def test_multiprocessing_df(self):

        # Single argument
        s = self.single
        data = self.make_test_data()
        s.set_n_jobs(2)
        data = s.featurize_dataframe(data, 'x')
        self.assertArrayAlmostEqual(data['y'], [2, 3, 4])

        # Multi-argument
        s = self.multiargs
        data = self.make_test_data()
        s.set_n_jobs(2)
        data['x2'] = [4, 5, 6]
        data = s.featurize_dataframe(data, ['x', 'x2'])
        self.assertArrayAlmostEqual(data['y'], [5, 7, 9])

    def test_fittable(self):
        data = self.make_test_data()
        ft = self.fittable

        # Test fit and featurize separately
        ft.fit(data['x'][:2])
        ft.featurize_dataframe(data, 'x')
        self.assertArrayAlmostEqual(data['a'], [4, 5, 6])
        self.assertRaises(Exception, data.__getattr__, 'c')

        # Test fit + featurize methods on new fits
        data = self.make_test_data()
        transformed = ft.fit_transform([data['x'][1]])
        self.assertArrayAlmostEqual(transformed[0], [5])
        data = self.make_test_data()
        ft.fit_featurize_dataframe(data, 'x')
        self.assertArrayAlmostEqual(data['a'], [4, 5, 6])
        self.assertArrayAlmostEqual(data['b'], [5, 6, 7])
        self.assertArrayAlmostEqual(data['c'], [2, 4, 6])

    def test_stacked_featurizer(self):
        data = self.make_test_data()
        data['y'] = [1, 2, 3]

        # Test for a regressor
        model = DummyRegressor()
        model.fit(self.multi.featurize_many(data['x']), data['y'])

        #  Test the predictions
        f = StackedFeaturizer(self.single, model)
        self.assertEquals([2], f.featurize(data['x'][0]))

        #  Test the feature names
        self.assertEquals(['prediction'], f.feature_labels())
        f.name = 'ML'
        self.assertEquals(['ML prediction'], f.feature_labels())

        # Test classifier
        model = DummyClassifier("prior")
        data['y'] = [0, 0, 1]
        model.fit(self.multi.featurize_many(data['x']), data['y'])

        #  Test the prediction
        f.model = model
        self.assertEquals([2./3], f.featurize(data['x'][0]))

        #  Test the feature labels
        self.assertRaises(ValueError, f.feature_labels)
        f.class_names = ['A', 'B']
        self.assertEquals(['ML P(A)'], f.feature_labels())

        # Test with three classes
        data['y'] = [0, 2, 1]
        model.fit(self.multi.featurize_many(data['x']), data['y'])

        self.assertArrayAlmostEqual([1./3]*2, f.featurize(data['x'][0]))
        f.class_names = ['A', 'B', 'C']
        self.assertEquals(['ML P(A)', 'ML P(B)'], f.feature_labels())


if __name__ == '__main__':
    unittest.main()
