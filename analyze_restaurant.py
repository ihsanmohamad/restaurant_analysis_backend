from textblob import TextBlob
import pandas as pd
import numpy as np
import re

def analyze_data(dataframe ,**kwargs):

    positive = []
    neutral = []
    negative = []


    df = dataframe
    def cleanTxt(text):
        text=re.sub(r'@[A-Za-z0-9]+','', text)
        text=re.sub(r'#','',text)
        text=re.sub(r'RT[\s]+','',text)
        text=re.sub(r'https?:\/\/\S+','',text)
        
        return text

    df['text']=df['text'].apply(cleanTxt)
    
        # Create function to retrieve subjectivity
    def getSubjectivity(text):
        return TextBlob(text).sentiment.subjectivity

    # Create function to retrieve polarity
    def getPolarity(text):
        return TextBlob(text).sentiment.polarity

    # retrieve subjectivity
    df['Subjectivity']=df['text'].apply(getSubjectivity)

    #retrieve polarity
    df['Polarity']=df['text'].apply(getPolarity)

    # categorizing the tweets' sentiments to negative, positive or neutral
    def getAnalysis(score):
        if(score<0):
            return 'Negative'
        elif score==0:
            return 'Neutral'
        else:
            return 'Positive'
        
    df['Analysis']=df['Polarity'].apply(getAnalysis)

    j=1
    sortedDF=df.sort_values(by=['Polarity'])

    
    positive_count = 0
    neutral_count = 0
    negative_count = 0

    for i in range(0, sortedDF.shape[0]):

        data = {}

        if(sortedDF['Analysis'][i]=='Positive'):
           

            positive.append(sortedDF['text'][i])

            positive_count += 1
            print(str(j)+') '+sortedDF['text'][i])
            print()
            j=j+1
        elif(sortedDF['Analysis'][i]=='Neutral'):

            
            neutral.append(sortedDF['text'][i])

            neutral_count += 1
            print(str(j)+') '+sortedDF['text'][i])
            print()
            j=j+1
        elif(sortedDF['Analysis'][i]=='Negative'):

            
            negative.append(sortedDF['text'][i])

            negative_count += 1
            print(str(j)+') '+sortedDF['text'][i])
            print()
            j=j+1


    return {
        
            "review": {
                "positive": positive,
                "neutral": neutral,
                "negative": negative,
            },
            "positive_count": positive_count,
            "neutral_count": neutral_count,
            "negative_count": negative_count,
        
    }

