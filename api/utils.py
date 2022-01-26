import tweepy
import re
from textblob import TextBlob
import pandas as pd




def twitter_api():
    login = pd.read_csv('login.csv')

    cons_key = login['Keys'][0]
    cons_key_sec = login['Keys'][1]
    acc_token = login['Keys'][2]
    acc_token_sec = login['Keys'][3]

    authenticate = tweepy.OAuthHandler(cons_key, cons_key_sec)

    authenticate.set_access_token(acc_token, acc_token_sec)

    api = tweepy.API(authenticate, wait_on_rate_limit=True)

    return api 



def clean_txt(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text) #removes @mentions
    text = re.sub(r'#', '', text) #removes the #
    text = re.sub(r'RT[\s]+', '', text) #removes RT
    text = re.sub(r':', '', text)
    text = re.sub(r'https?:\/\/\S+', '', text) #removes the hyperlink

    return text


def get_polar(text):
    return TextBlob(text).sentiment.polarity


def get_data_set():
    data = pd.read_csv('EPL.csv', sep=r'\s*,\s*', header=0, encoding='ascii', engine='python')
    res_num = []

    for i in range(data.shape[0]):
        if data['FTHG'][i] > data['FTAG'][i]:
            res_num.append(2)
        elif data['FTAG'][i] > data['FTHG'][i]:
            res_num.append(0)
        else:
            res_num.append(1)

    data['Result'] = res_num

    dataset = pd.DataFrame((data['HomeTeam'][i] for i in range(data.shape[0])), columns=['HomeTeam'])
    dataset['AwayTeam'] = data['AwayTeam']
    dataset['Results'] = data['Result']
    dataset['Year'] = data['Year']

    return dataset