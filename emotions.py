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

# Returns the date a percent between 1900 and 2020
def perc(x):
    return int((100 * (x - 1900) / (2020 - 1900)))

def main():
    # Create the word to emotion dictionary
    wordToEmotions = readNRC('NRC-Emotion-Lexicon-Wordlevel-v0.92.txt')
    dir = './sotu_speeches/'

    # Create data dictionary to hold all of the years emotions
    data = dict()

    # Loop through all files and analyze
    files = os.listdir(dir)
    for f in files:
        if f[:4] != '2007':
            print(f'Analyzing {f[:4]}')
            data[f[:4]] = analyze(f'{dir}{f}', wordToEmotions)

    # Turn the data into a dataframe
    df = pd.DataFrame.from_dict(data, orient='index')

    # Make directory for graphs and tables
    if not os.path.exists('graphs/'):
        os.makedirs('graphs/')
    if not os.path.exists('tables/'):
        os.makedirs('tables/')

    # Open the file that contains important dates and read them into lists
    f = open('dates.txt', 'r')
    dates ={
        'war_i': None,
        'war_f': None,
        'pandemics': None
    }

    for line in f.readlines():
        split = line.strip().split(':')
        dates[split[0]] = [int(i) for i in split[1].split(',')]
    f.close()       

    #Plot each emotion with each event
    for emotion in list(df):  
        for event in dates.keys():
            ax = df[emotion].plot()
            # ax.plot() 
            # add in the lines for various dates
            for date in dates[event]:
                plt.axvline(x=perc(date), linewidth=2, linestyle='--', color='g', alpha=0.5)
            
            # plot.plot(plt.vlines(dates['war_i'], 0, 25))
            plt.xlabel('Year')
            plt.ylabel('Emotion Level')

            if event == 'war_i':
                plt.title(f'{emotion} during the start of wars')
            elif event == 'war_f':
                plt.title(f'{emotion} during the end of wars')
            elif event == 'pandemics':
                plt.title(f'{emotion} during pandemics')

            plt.savefig(f'graphs/{emotion}_{event}.png')
            plt.clf()
        
    # Generate a table to compare values
    mean = []
    war_i_mean = []
    war_f_mean = []
    pandemic = []
    emotions = list(df)
    
    for emotion in emotions:
        arr = df[emotion].values
        # Get the mean of all values and for the event years
        mean.append(int(np.mean(arr)))
        
        war_i_mean.append(round(np.mean(np.array([arr[2017 - i] for i in dates['war_i']])), 2))
        war_f_mean.append(round(np.mean(np.array([arr[2017 - i] for i in dates['war_f']])), 2))
        pandemic.append(round(np.mean(np.array([arr[2017 - i] for i in dates['pandemics']])), 2))

    x = PrettyTable()
    x.field_names = ['Emotion', 'War Start', 'War End', 'Pandemic']
    for index in range(len(emotions)):
        x.add_row([emotions[index], war_i_mean[index], war_f_mean[index], pandemic[index]])
    
    print(x)



    #TODO : Find a nice way to make a table of this data. Just make these array the columns and well get some nice data
    # print('-------------------------------')
    # for index in range(len(emotions)):
    #     print(f'{emotions[index]} | {war_i_mean[index]} | {war_f_mean[index]} | {pandemic[index]}')
    #     print('-------------------------------')

if __name__ == "__main__":
    main()
