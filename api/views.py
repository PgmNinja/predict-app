from markupsafe import re
from .serializers import SelectTeamSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
import math

import pickle
import numpy as np
import pandas as pd

from .utils import find_polar, get_data_set


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
        
        home_team = request.data.get('home_team', None)
        away_team = request.data.get('away_team', None)

        home_polar = find_polar(home_team)
        away_polar = find_polar(away_team)

        if home_polar >= away_polar:
            X = np.array([[home_team, away_team]])
        else:
            X = np.array([[away_team, home_team]])

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

        return Response(content, status=status.HTTP_200_OK)



class AnalysisView(APIView):
    serializer_class = SelectTeamSerializer

    def find_stats(self, dataframe, team):
        stats_dict = {}

        for i in range(dataframe.shape[0]):
            if (dataframe['HomeTeam'].iloc[i] == team and dataframe['Results'].iloc[i] == 2) or \
            (dataframe['AwayTeam'].iloc[i] == team and dataframe['Results'].iloc[i] == 0):
                year = dataframe['Year'].iloc[i]
                if year in stats_dict:
                    stats_dict[int(year)] += 1 
                else:
                    stats_dict[int(year)] = 1

        return stats_dict


    def find_df_head_to_head(self, data, home_team, away_team):
        df_head_to_head = pd.concat([data.loc[(data['HomeTeam'] == home_team) & (data['AwayTeam'] == away_team)], \
            data.loc[(data['HomeTeam'] == away_team) & (data['AwayTeam'] == home_team)]])

        return df_head_to_head


    def find_team_wins(self, dataframe, team):
        wins = 0
        for i in range(dataframe.shape[0]):
            if ((dataframe['HomeTeam'].iloc[i] == team) and (dataframe['Results'].iloc[i] == 2)) or \
            ((dataframe['AwayTeam'].iloc[i] == team) and (dataframe['Results'].iloc[i] == 0)):
                wins += 1

        return wins
        

    def post(self, request, *args, **kwargs):
        data = get_data_set()
        home_team = request.data.get('home_team', None)
        away_team = request.data.get('away_team', None)
        home_polar = find_polar(home_team)
        away_polar = find_polar(away_team)

        home_team_df = pd.concat([data.loc[data['HomeTeam'] == home_team], data.loc[data['AwayTeam'] == home_team]])
        away_team_df = pd.concat([data.loc[data['HomeTeam'] == away_team], data.loc[data['AwayTeam'] == away_team]])

        df_head_to_head = self.find_df_head_to_head(data, home_team, away_team)

        home_stats = self.find_stats(home_team_df, home_team)
        away_stats = self.find_stats(away_team_df, away_team)

        home_team_win = self.find_team_wins(df_head_to_head, home_team)
        away_team_win = self.find_team_wins(df_head_to_head, away_team)

        
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


