from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import string
import os
import operator
from prettytable import PrettyTable

# Reads the large dictionary
def readNRC(filename):
    wordToEmotions = dict()
    with open(filename, 'r') as fp:
        # Loop through lines
        for line in fp:
            line = line.strip('\n')
            # If no emotional value, skip
            if line[-1:] == '0':
                continue
            # Else analyze
            else:
                words = line.split('\t')
                if len(words) != 3:
                    continue
                word = words[0]
                emotion = words[1]
                # Store the emotions associated with the word
                if word not in wordToEmotions.keys():
                    wordToEmotions[word] = [emotion]
                else:
                    wordToEmotions[word].append(emotion)
    return wordToEmotions


def getWords(filename):
    """ Gets all of the words from a file.
    """
    # Get text from the file
    with open(filename, 'r') as fp:
        text = fp.read()

    punctuation = [ c for c in string.punctuation ] + [u'\u201c',u'\u201d',u'\u2018',u'\u2019']

    # Get words from the file
    words = []
    for word in word_tokenize(text):
        # Omit punctuation or digits
        if word in punctuation or word in string.digits:
            continue
        words.append(word)

    return words


def getEmotions(words, wordToEmotions):
    """ Gets all of the emotions from a list of words.
    """
    # Define the emotions
    emotions = {
        'anger': 0.0,
        'anticipation': 0.0,
        'disgust': 0.0,
        'fear': 0.0,
        'joy': 0.0,
        'negative': 0.0,
        'positive': 0.0,
        'sadness': 0.0,
        'surprise': 0.0,
        'trust': 0.0
    }

    # loop through the words and count the emotions
    for word in words:
        # if the word is in the dictionary
        if word in wordToEmotions.keys():
            # for each emotion associated with that word
            for emotion in wordToEmotions[word]:
                emotions[emotion] += 1

    # percentify
    total = sum(emotions.values())
    for key in emotions.keys():
        emotions[key] = emotions[key] / total * 100

    return emotions


def analyze(filename, wordToEmotions):
    """ Performs general analysis on the file
    """
    # Get all words from the file
    words = getWords(filename)
    # Get the emotions
    emotions = getEmotions(words, wordToEmotions)    

    return emotions


def readDates(category):
    with open('dates.txt', 'r') as fp:
        lines = fp.readlines()
    for line in lines:
        if(line.split(':')[0] == category):
            # This is the stupidest line ever but it splits the dates from the date
            # file into a list of list of all of the date ranges
            return [list(range(int(x.split('-')[0]), int(x.split('-')[1])+1)) for x in line.strip('\n').split(':')[1].split(',')]


def mkdir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
            

# Generates all of the graphs
def graphs(df, dates):
    colors = {
        'wars': 'red',
        'pandemics': 'orange',
        'recessions': 'blue'
    }

    # Loop through each emotion and each event for each emotion
    for emotion in list(df):  
        for event in dates.keys():
            df[emotion].plot()

            # Create the span in the graph
            for date in dates[event]:
                start = int(date[0])
                end = int(date[len(date)-1])
                plt.axvspan(start, end, alpha=0.15, color=colors[event])

            # Label and title the graphs
            plt.xlabel('Year')
            plt.ylabel('Percentage of Emotion Words')
            if event == 'wars':
                plt.title(f'{emotion.upper()} during Wartime')
            elif event == 'recessions':
                plt.title(f'{emotion.upper()} during Recessions')
            elif event == 'pandemics':
                plt.title(f'{emotion.upper()} during Pandemics')

            # Save and clear
            mkdir(event)
            plt.savefig(f'{event}/{emotion}_{event}.png')
            plt.clf()


def main():
    # Create the word to emotion dictionary
    wordToEmotions = readNRC('NRC-Emotion-Lexicon-Wordlevel-v0.92.txt')
    dir = './sotu_speeches/'

    # Create data dictionary to hold all of the years emotions
    data = dict()

    # Loop through all files and analyze
    files = os.listdir(dir)
    for f in files[:]:
        year = int(f[:4])
        print(f'Analyzing {year}')
        data[year] = analyze(f'{dir}{f}', wordToEmotions)

    # Turn the data into a dataframe
    df = pd.DataFrame.from_dict(data, orient='index')

    # Read the dates for important events
    dates = dict()
    for event in ['wars', 'pandemics', 'recessions']:
        dates[event] = readDates(event)

    # Graph each emotion
    graphs(df, dates)
        
    # Generate a table to compare values
    means = dict()
    
    # Go through all of the emotions and get means
    for emotion in list(df):
        means[emotion] = dict()
        arr = df[emotion].values

        # Get the mean of all values and for the event years
        means[emotion]['average'] = round(np.mean(arr), 2)
        means[emotion]['war'] = round(np.mean(np.array([arr[2017 - j] for i in dates['wars'] for j in i])), 2)
        means[emotion]['recession'] = round(np.mean(np.array([arr[2017 - j] for i in dates['recessions'] for j in i])), 2)
        means[emotion]['pandemics'] = round(np.mean(np.array([arr[2017 - j] for i in dates['pandemics'] for j in i])), 2)

    # print(means)
    means_df = pd.DataFrame.from_dict(means)
    print(means_df)

    # x = PrettyTable()
    # x.field_names = ['Emotion', 'War', 'Recession', 'Pandemic']
    # for index in range(len(list(df))):
    #     x.add_row([emotions[index], war_mean[index], recession_mean[index], pandemics_mean[index]])
    
    # print(x)



    #TODO : Find a nice way to make a table of this data. Just make these array the columns and well get some nice data
    # print('-------------------------------')
    # for index in range(len(emotions)):
    #     print(f'{emotions[index]} | {war_mean[index]} | {recession_mean[index]} | {pandemic[index]}')
    #     print('-------------------------------')

if __name__ == "__main__":
    main()
