import os
import numpy as np
# import ujson as json
import json
import pickle
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer


class SVMModel:
    """Base class for SVM-like classifiers."""

    def __init__(self, X_filename, y_filename, meta_filename, num_features=None, save_folder='./SVM_models'):
        self.X_filename = X_filename
        self.y_filename = y_filename
        self.meta_filename = meta_filename
        self._num_features = num_features
        self.save_folder = save_folder
        self.clf, self.vec = None, None
        self.column_idxs = [] # feature indexes after feature selection
        self.X_train, self.y_train, self.m_train = [], [], []
        self.X_test, self.y_test, self.m_test = [], [], []

    def generate(self, save=True):
        X_train, X_test, y_train, y_test, m_train, m_test, self.vec, train_test_random_state = load_features(self.X_filename, self.y_filename, self.meta_filename)

        self.column_idxs = self.perform_feature_selection(X_train, y_train)
        self.X_train = X_train[:, self.column_idxs]
        self.X_test = X_test[:, self.column_idxs]
        self.y_train, self.y_test = y_train, y_test
        self.m_train, self.m_test = m_train, m_test
        self.clf = self.fit(self.X_train, self.y_train)

        if save:
            self.save_to_file()

    #
    # CHECKPOINT 2 (5 points) MANDATORY COMMENT
    # Feature Selection Analysis:
    # Training and testing the SVM with all features (226,548 features) versus using the top 5,000 features
    # demonstrates that a smaller, more relevant feature set can improve performance.

    # Training Performance with All Features (226,548 features):
    #   - Accuracy: 99.96%, F1: 99.80%, Precision: 99.68%, Recall: 99.92%
    #   - Confusion Matrix: [[11483, 4], [1, 1275]]
    # Training Performance with 5,000 Features:
    #   - Accuracy: 99.97%, F1: 99.84%, Precision: 99.84%, Recall: 99.84%
    #   - Confusion Matrix: [[11485, 2], [2, 1274]]
    # 
    # Observations: The training performance difference is minimal, but 5,000 features slightly improves accuracy, F1, and precision.

    # Testing Performance with All Features:
    #   - Accuracy: 97.87%, F1: 89.17%, Precision: 90.49%, Recall: 87.89%
    #   - Confusion Matrix: [[5601, 58], [76, 552]]
    # Testing Performance with 5,000 Features:
    #   - Accuracy: 98.06%, F1: 90.16%, Precision: 91.34%, Recall: 89.01%
    #   - Confusion Matrix: [[5606, 53], [69, 559]]
    #
    # Observations: The testing performance shows a more noticeable improvement with 5,000 features in all metrics.

    # Explanation:
    # By focusing on the 5,000 most important features, the model avoids overfitting on less informative or noisy features.
    # These selected features have stronger predictive power for distinguishing between malware and benign samples,
    # leading to better accuracy, precision, and recall. 
    # In summary, feature selection improves model performance by emphasizing the most relevant features
    # and reducing noise from irrelevant features.
    #
    def perform_feature_selection(self, X_train, y_train):
        ############## TODO:  implement me #########
        # """Perform L2-penalty feature selection."""
        # cols = None
        # if self._num_features is not None:
        #     # TODO
        #     pass
        # else:
        #     pass
        #     # TODO
        # ############
        # return cols

        if self._num_features is None:
            # If no specific number of features is set, use all features
            cols = np.arange(X_train.shape[1])
        else:
            # Perform feature selection if the number of features is specified
            clf = LinearSVC(C=self.svm_c, max_iter=self.max_iter, dual=False)
            clf.fit(X_train, y_train)
            
            # Get feature importances from the trained model coefficients
            feature_importances = np.abs(clf.coef_).sum(axis=0)
            
            # Select the indices of the top `self._num_features` most important features
            cols = np.argsort(feature_importances)[-self._num_features:]
        
        # Return the indices of the selected features
        return cols

    def save_to_file(self):
        create_parent_folder(self.model_name)
        with open(self.model_name, 'wb') as f:
            pickle.dump(self, f, protocol=4)


class SVM(SVMModel):
    """Standard linear SVM using scikit-learn implementation."""

    def __init__(self, X_filename, y_filename, meta_filename, save_folder='./',
                 num_features=None, svm_c=1, max_iter=1000):
        super().__init__(X_filename, y_filename, meta_filename, num_features, save_folder)
        self.model_name = self.generate_model_name()
        self.svm_c = svm_c
        self.max_iter = max_iter

    def fit(self, X_train, y_train):
        ##############TODO: implement me ########
        # clf = None
        # return clf

        # Initialize the LinearSVC model with specified C and max_iter parameters
        self.clf = LinearSVC(C=self.svm_c, max_iter=self.max_iter, dual=False)
        # Train the classifier with the training data
        self.clf.fit(X_train, y_train)
        return self.clf

    def generate_model_name(self):
        model_name = f'svm'
        model_name += '.p' if self._num_features is None else '-f{}.p'.format(self._num_features)
        return os.path.join(self.save_folder, model_name)


def create_parent_folder(file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))


def load_features(X_filename, y_filename, meta_filename):
    train_test_random_state = 137 #hard coded to split the training set and testing set.
    with open(X_filename, 'rt') as f:
        X = json.load(f)
        try:
            [o.pop('sha256') for o in X]
        except:
            pass
    with open(y_filename, 'rt') as f:
        y = json.load(f)
    with open(meta_filename, 'rt') as f:
        meta = json.load(f)

    X, y, vec = vectorize(X, y)
    train_idxs, test_idxs = train_test_split(
        range(X.shape[0]),
        stratify=y,
        test_size=0.33,
        random_state=train_test_random_state)

    X_train = X[train_idxs]
    X_test = X[test_idxs]
    y_train = y[train_idxs]
    y_test = y[test_idxs]
    m_train = [meta[i] for i in train_idxs]
    m_test = [meta[i] for i in test_idxs]

    return X_train, X_test, y_train, y_test, m_train, m_test, vec, train_test_random_state

def vectorize(X, y):
    vec = DictVectorizer(sparse=True)
    X = vec.fit_transform(X)
    y = np.asarray(y)
    return X, y, vec

