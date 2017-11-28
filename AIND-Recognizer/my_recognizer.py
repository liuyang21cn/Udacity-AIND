import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # TODO implement the recognizer
    # return probabilities, guesses
    # loop over each X in the test set
    for i in range(len(test_set.get_all_Xlengths())):
        X, lengths = test_set.get_item_Xlengths(i)
        # for each X create a dictionary to store the log likelihood
        log_map = {}
        # for each word and model in models, calculate score for each word
        for word, model in models.items():
            try:
                log_map[word] = model.score(X, lengths)
            except:
                log_map[word] = float('-inf')
        # for each X, append score dict
        probabilities.append(log_map)
        # first sort the score dcit, then take the last element which has the
        # largetst possibility, append the word to guesses
        guess_word = sorted(log_map.items(), key = lambda x: x[1])[-1][0]
        guesses.append(guess_word)

    return  probabilities, guesses
