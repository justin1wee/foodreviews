"""
file: textastic.py
description: a reusable library for text analysis and comparison
"""

import matplotlib.pyplot as plt
import random as rnd
from collections import Counter, defaultdict
import re
from textblob import TextBlob
import plotly.graph_objects as go
import pprint
from wordcloud import WordCloud

class Textastic:

    def __init__(self):
        """ constructor """
        self.data = defaultdict(dict)

    @staticmethod
    def _default_parser(filename):
        """ this should probably be a default text parser for processing
        simple unformatted text files. """

        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()

        results = {
            'wordcount': Counter([token.lower() for token in re.split(r'[\s\W_]+', text) if token]),
            'numwords': len([token.lower() for token in re.split(r'[\s\W_]+', text) if token]),
            'sentiment': TextBlob(text).sentiment
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

    @staticmethod
    def load_stop_words(filename):
        """ a static method that loads stop words from a text file of stopwords"""

        # creates a list of stopwords to filter out
        stopwords = []
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                stopwords.append(line.strip().lower())

        return stopwords

    # function for wordcount_sankey diagram
    def wordcount_sankey(self, labels, word_list=None, k=5):

        stopwords = Textastic.load_stop_words('txt/stopwords.txt')

        for label in labels:
            self.data['wordcount'][label] = Counter(
                {word: count for word, count in self.data['wordcount'][label].items() if word not in stopwords})

        # Determine words to include
        if word_list is None:
            combined_counter = Counter()
            for label in labels:
                combined_counter += self.data['wordcount'][label]
            word_list = [word for word, _ in combined_counter.most_common(k)]

        # Prepare data for the Sankey diagram
        sources, targets, values = [], [], []
        node_labels = labels + word_list  # Label nodes for texts and words
        for label in labels:
            for word in word_list:
                if word in self.data['wordcount'][label]:
                    sources.append(labels.index(label))
                    targets.append(len(labels) + word_list.index(word))
                    values.append(self.data['wordcount'][label][word])

        # Create the Sankey diagram
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=node_labels,
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
            ))])

        fig.update_layout(title_text="Word Count Sankey Diagram", font_size=10)
        fig.write_image('wordcount_sankey.png')
        fig.show()

    # function for sentiment scatter plot
    def sentiment_scatter(self, labels):
        """ a function that performs sentiment analysis on each text file
        and creates a scatter plot with each restaurant's polarity and subjectivity"""

        polarities = []
        subjectivities = []
        sizes = []
        colors = []  # List to hold colors for each point

        # Define a list of colors to use (extend this list if you have many labels)
        color_options = ['red', 'green', 'blue', 'purple', 'orange', 'cyan', 'magenta', 'yellow', 'black']

        for i, label in enumerate(labels):
            polarity, subjectivity = self.data['sentiment'][label]
            numwords = self.data['numwords'][label]

            polarities.append(polarity)
            subjectivities.append(subjectivity)
            sizes.append(numwords / 2)  # Example scaling; adjust as necessary
            colors.append(color_options[i % len(color_options)])  # Cycle through color_options

        plt.figure(figsize=(10, 6))  # Set the figure size

        # Create a scatter plot with colors
        plt.scatter(polarities, subjectivities, s=sizes, c=colors, alpha=0.5)

        plt.title('Scatter Plot of Text Analysis')
        plt.xlabel('Polarity')
        plt.ylabel('Subjectivity')

        # Label each point with its corresponding label
        for i, label in enumerate(labels):
            plt.annotate(label, (polarities[i], subjectivities[i]))

        plt.grid(True)  # Optionally add a grid
        plt.savefig('sentiment_scatter.png')
        plt.show()

    # function for word cloud subplot visualization
    def generate_word_cloud(self, labels):
        stopwords = self.load_stop_words('txt/stopwords.txt')

        # Filter word counts for each label by removing stopwords
        for label in labels:
            if label in self.data['wordcount']:
                word_counts = self.data['wordcount'][label]
                filtered_word_counts = {word: count for word, count in word_counts.items() if word not in stopwords}
                self.data['wordcount'][label] = filtered_word_counts

        # Determine grid layout for subplots based on the number of labels
        num_labels = len(labels)
        num_cols = 2  # Number of columns in the subplot grid
        num_rows = (num_labels + num_cols - 1) // num_cols  # Calculate number of rows

        # Create subplots for each label
        fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 7))

        for i, label in enumerate(labels):
            if label in self.data['wordcount']:
                word_counts = self.data['wordcount'][label]
                wordcloud = WordCloud(width=400, height=200, background_color='white', random_state=42,
                                      max_font_size=60)
                wordcloud.generate_from_frequencies(word_counts)

                row = i // num_cols
                col = i % num_cols
                ax = axes[row, col] if num_rows > 1 else axes[col]  # Get appropriate axis

                ax.imshow(wordcloud, interpolation='bilinear')
                ax.set_title(f'Word Cloud for {label}')
                ax.set_xticks([])
                ax.set_yticks([])

        # Adjust layout and spacing of subplots
        plt.tight_layout()
        plt.show()