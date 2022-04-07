from csv import DictReader
import numpy as np
import pandas as pd
from feature_engineering import clean

LABELS = ['agree', 'disagree', 'discuss', 'unrelated']
LABELS_RELATED = ['unrelated','related']

class DataSet():
    def __init__(self, name="train", path="fnc-1"):
        self.path = path

        print("Reading dataset")
        bodies = name+"_bodies.csv"
        stances = name+"_stances.csv"

        self.stances = self.read(stances)
        articles = self.read(bodies)
        self.articles = dict()

        #make the body ID an integer value
        for s in self.stances:
            s['Body ID'] = int(s['Body ID'])

        #copy all bodies into a dictionary
        for article in articles:
            self.articles[int(article['Body ID'])] = article['articleBody']

        print("Total stances: " + str(len(self.stances)))
        print("Total bodies: " + str(len(self.articles)))

    def to_dataframe(self):
        stances = []
        headlines = []
        bodies = []

        for stance in self.stances:
            stances.append(LABELS.index(stance['Stance']))
            headlines.append(clean(stance['Headline']))
            bodies.append(clean(self.articles[stance['Body ID']]))
        # dictionary of lists
        dict = {'Stances': stances, 'Headlines': headlines, 'Bodies': bodies}


        return  pd.DataFrame(dict)


    def read(self,filename):
        rows = []
        with open(self.path + "/" + filename, "r", encoding='utf-8') as table:
            r = DictReader(table)

            for line in r:
                rows.append(line)
        return rows
