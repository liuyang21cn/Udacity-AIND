import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on BIC scores
        best_score, best_n_components = None, None
        min_bic = float('inf')
        best_model = None

        for num_states in range(self.min_n_components, self.max_n_components+1):
            try :
                # for each number of states, caclulate the logL and BIC score
                model = self.base_model(num_states)
                logL = model.score(self.X, self.lengths)
                logN = np.log(len(self.X))
                N = sum(self.lengths)
                n_features = self.X.shape[1]
                p = num_states*(num_states-1) + 2 * n_features * n_components
                BIC_Score = -2.0 * logL + p * logN
                if BIC_Score < min_bic:
                    min_bic = BIC_Score
                    best_model = model

            except Exception as e:
                continue

        return best_model if best_model else self.base_model(self.n_constant)

        # best_score = float('-inf')
        # best_model = None
        #
        # for num_states in range(self.min_n_components, self.max_n_components+1):
        #     try :
        #         # for each number of states, caclulate the logL and BIC score
        #         model = self.base_model(num_states)
        #         logL = model.score(self.X, self.lengths)
        #         logN = np.log(sum(self.lengths))
        #         p = num_states + num_states*(num_states-1) + num_states*sum(self.lengths)*2
        #         BIC_Score = -2.0 * logL + p * logN
        #     except Exception as e:
        #         continue
        #     # update best model
        #     if BIC_Score > best_score:
        #         best_score = BIC_Score
        #         best_model = model
        #
        # return best_model

class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    https://pdfs.semanticscholar.org/ed3d/7c4a5f607201f3848d4c02dd9ba17c791fc2.pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on DIC scores
        best_score = float('-inf')
        best_model = None
        M = len(self.words.keys())
        models = {}

        for num_states in range(self.min_n_components, self.max_n_components+1):
            log_sum = 0.0
            DIC_Score = float('-inf')
            # for each number of states, caclulate the logL and add to log_sum
            # if the current word is not this word
            try :
                model = self.base_model(num_states)
                logL = model.score(self.X, self.lengths)
                for word in self.hwords:
                    if word != self.this_word:
                        try:
                            log_sum += model.score(self.hwords[word])
                        except:
                            log_sum += 0.0
            except:
                logL = float('-inf')
            # calculate DIC score and update best model
            DIC_Score = logL - 1.0/(M-1)*log_sum
            if DIC_Score > best_score:
                best_score = DIC_Score
                best_model = model

        return best_model

class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection using CV

        # Initialize KFold
        n_split = 3
        split_method = KFold(n_splits = n_split)
        logLs = []
        best_score = float('-inf')
        best_model = None

        # run for different number of states
        for num_states in range(self.min_n_components, self.max_n_components+1):
            # if the length of sequences less than number of split,
            # don't use CV
            if len(self.sequences) < n_split:
                # use base model if can't use KFold
                try:
                    model = self.base_model(num_states)
                    logL = model.score(self.X, self.lengths)
                except:
                    logL = 0
                logLs.append(logL)
            else:
                for cv_train_idx, cv_test_idx in split_method.split(self.sequences):
                    self.X, self.lengths = combine_sequences(cv_train_idx, self.sequences)
                    X_test, lengths_test = combine_sequences(cv_test_idx,  self.sequences)
                    try:
                        model = self.base_model(num_states)
                        logL  = model.score(X_test, lengths_test)
                    except:
                        logL = 0
                    logLs.append(logL)
            # calculate average of log likelihood
            avg_logL = np.mean(logLs)
            # find the best model
            if avg_logL > best_score:
                best_score = avg_logL
                best_model = model

        return best_model
