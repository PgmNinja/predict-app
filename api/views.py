from markupsafe import re
from .serializers import SelectTeamSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
import math

import pickle
import numpy as np
import pandas as pd

from .utils import twitter_api, clean_txt, get_polar, get_data_set 


def model_loaded():
    with open('saved.pkl', 'rb') as _file:
        data = pickle.load(_file)
    return data


class PredictView(APIView):
    serializer_class = SelectTeamSerializer

    def post(self, request, *args, **kwargs):
        data = model_loaded()

        model = data['model']
        le_home_team = data['le_home_team']
        le_away_team = data['le_away_team']

        
        api = twitter_api()

        home_team = request.data['home_team']
        away_team = request.data['away_team']
        request.session['home'] = home_team
        request.session['away'] = away_team

        home_twt = api.search_tweets(q=home_team, count=100000, lang='en', tweet_mode='extended')
        away_twt = api.search_tweets(q=away_team, count=100000, lang='en', tweet_mode='extended')

        df_home = pd.DataFrame([tweet.full_text for tweet in home_twt], columns=['Tweets'])
        df_away = pd.DataFrame([tweet.full_text for tweet in away_twt], columns=['Tweets'])

        df_home['Tweets'] = df_home['Tweets'].apply(clean_txt)
        df_away['Tweets'] = df_away['Tweets'].apply(clean_txt)

        df_home['Polarity'] = df_home['Tweets'].apply(get_polar)
        df_away['Polarity'] = df_away['Tweets'].apply(get_polar)

        home_polar = np.mean(df_home['Polarity'].values)
        away_polar = np.mean(df_away['Polarity'].values)
        request.session['home_polar'] = home_polar
        request.session['away_polar'] = away_polar

        if home_polar >= away_polar:
            X = np.array([[home_team, away_team]])
        else:
            X = np.array([[away_team, home_team]])

        # X = np.array([[away_team, home_team]])

        X1 = X[0].copy()

        X[:,0] = le_home_team.transform(X[:,0])
        X[:,1] = le_away_team.transform(X[:,1])
        
        X = X.astype('float')

        y_pred = model.predict(X)

        if y_pred == 2:
            result = X1[0] + ' wins'
        elif y_pred == 1:
            result = 'Match Draws'
        elif y_pred == 0:
            result = X1[1] + ' wins'

        probs = model.predict_proba(X)[0]
        probability = {"home_team": math.floor(probs[2]*100), "away_team": math.floor(probs[0]*100), "draw": math.floor(probs[1]*100)}

        content = {
                    "home_team": str(X1[0]),
                    "away_team": str(X1[1]),
                    "result": result,
                    "probability": probability
                    }

        print(result)

        return Response(content, status=status.HTTP_200_OK)




class AnalysisView(APIView):
    def get(self, request, *args, **kwargs):
        data = get_data_set()
        home_team = request.session['home']
        away_team = request.session['away']
        home_polar = request.session['home_polar']*100
        away_polar = request.session['away_polar']*100

        home_team_df = pd.concat([data.loc[data['HomeTeam'] == home_team], data.loc[data['AwayTeam'] == home_team]])
        away_team_df = pd.concat([data.loc[data['HomeTeam'] == away_team], data.loc[data['AwayTeam'] == away_team]])

        df_head_to_head = pd.concat([data.loc[(data['HomeTeam'] == home_team) & (data['AwayTeam'] == away_team)], \
            data.loc[(data['HomeTeam'] == away_team) & (data['AwayTeam'] == home_team)]])

        home_stats = {}
        away_stats = {}

        home_team_win = 0
        away_team_win = 0

        for i in range(home_team_df.shape[0]):
            if (home_team_df['HomeTeam'].iloc[i] == home_team and home_team_df['Results'].iloc[i] == 2) or \
            (home_team_df['AwayTeam'].iloc[i] == home_team and home_team_df['Results'].iloc[i] == 0):
                year = home_team_df['Year'].iloc[i]
                if year in home_stats:
                    home_stats[int(year)] += 1 
                else:
                    home_stats[int(year)] = 1

        for i in range(away_team_df.shape[0]):
            if (away_team_df['HomeTeam'].iloc[i] == away_team and away_team_df['Results'].iloc[i] == 2) or \
            (away_team_df['AwayTeam'].iloc[i] == away_team and away_team_df['Results'].iloc[i] == 0):
                year = away_team_df['Year'].iloc[i]
                if year in away_stats:
                    away_stats[int(year)] += 1 
                else:
                    away_stats[int(year)] = 1


        for i in range(df_head_to_head.shape[0]):
            if ((df_head_to_head['HomeTeam'].iloc[i] == home_team) and (df_head_to_head['Results'].iloc[i] == 2)) or \
            ((df_head_to_head['AwayTeam'].iloc[i] == home_team) and (df_head_to_head['Results'].iloc[i] == 0)):
                home_team_win += 1

            if ((df_head_to_head['HomeTeam'].iloc[i] == away_team) and (df_head_to_head['Results'].iloc[i] == 2)) or \
            ((df_head_to_head['AwayTeam'].iloc[i] == away_team) and (df_head_to_head['Results'].iloc[i] == 0)):
                away_team_win += 1


        content = {
        'home_team': home_team,
        'away_team': away_team,
        'home_stats': home_stats,
        'away_stats': away_stats,
        'home_count': home_team_win,
        'away_count': away_team_win,
        'home_polar': home_polar,
        'away_polar': away_polar,
        }

        print(home_stats)

        return Response(content, status=status.HTTP_200_OK)


