"""
file: textastic.py
description: a reusable library for text analysis and comparison
"""

import matplotlib.pyplot as plt
import random as rnd
from collections import Counter, defaultdict

class Textastic:

    def __init__(self):
        """ constructor """
        self.data = defaultdict(dict)

    @staticmethod
    def _default_parser(filename):
        """ this should probably be a default text parser for processing
        simple unformatted text files. """

        results = {
            'wordcount': Counter('to be or not to be'.split(' ')),
            'numwords': rnd.randrange(10, 50)
        }
        print('Parsed: ', filename, ': ', results)
        return results


    def load_text(self, filename, label=None, parser=None):
        if parser is None:
            results = Textastic._default_parser(filename)
        else:
            results = parser(filename)

        if label is None:
            label = filename

        for k, v in results.items():
            self.data[k][label] = v


    def compare_num_words(self):
        """ a very simplistic visualization that creates a bar chart comparing the
        number of words in each text file (FOR DEMO ONLY) """

        for label, nw in self.data['numwords'].items():
            plt.bar(label, nw)
        plt.show()

