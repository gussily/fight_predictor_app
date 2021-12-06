
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import random

import pandas as pd
import numpy as np
import math
from scipy import stats as scistats

import json
import array as arr
from datetime import datetime, date
import pickle

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]




app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list."}


class FightPredictor:

    
    def __init__(self, df_elo, df_fight_data, fighter_dict, name_dict, current_elo_values, 
        stat_type_mean_sd_counts, current_strike_dstrbs, columns, divby=400):

        """Takes as input:
            df_elo containing historical data for all fights and all fighter
         scores and metrics at the time of the fight (df_elo)"""
        
        self.divby = divby
        self.model = self.get_model(df_elo, df_fight_data, columns, divby)
        self.columns = columns
        
        self.fighter_dict = fighter_dict
        self.name_dict = name_dict
        self.current_elo_values = current_elo_values
        self.stat_type_mean_sd_counts = stat_type_mean_sd_counts
        self.current_strike_dstrbs = current_strike_dstrbs
        self.divby = divby
    

    def get_model(self, df_elo, df_fight_data, columns, divby):
        
        df_elo = df_elo.copy()
        df_elo = df_elo[['fight_id', 'fighter', 'fighter_id'] + columns]
        df_fight_data = df_fight_data.copy()
        df_fight_data['fighter_0'] = df_fight_data['fighter_0'].astype(str)
        df_fight_data['fighter_1'] = df_fight_data['fighter_1'].astype(str)
        
        df_fight_data = df_fight_data[['fighter_0', 'fighter_1', 'fight_id', 'winner']]

        df_elo_f0 = df_elo[df_elo['fighter'] == 0]\
            .drop(columns=['fighter'])\
            .rename(columns={'fighter_id': 'fighter_0'})

        df_elo_f1 = df_elo[df_elo['fighter'] == 1]\
            .drop(columns=['fighter'])\
            .rename(columns={'fighter_id': 'fighter_1'})
        
        df_fight_data = df_fight_data.merge(df_elo_f0, on=['fight_id', 'fighter_0'], how='inner')
        df_fight_data.rename(columns={c: c + '_0' for c in columns},
            inplace=True)
        
        df_fight_data = df_fight_data.merge(df_elo_f1, on=['fight_id', 'fighter_1'], how='inner')
        df_fight_data.rename(columns={c: c + '_1' for c in columns},
            inplace=True)
            
        for col in columns:
            df_fight_data[col] = df_fight_data[col + '_1'] - df_fight_data[col + '_0']
            df_fight_data[col] = df_fight_data[col].apply(lambda x: \
                1.0 / (1 + 1.0 * math.pow(10, x / divby)))
            df_fight_data.drop(columns = [col + '_0', col + '_1'], inplace=True)

        df_fight_data = df_fight_data[columns + ['winner']]

        for i in df_fight_data.index:
            if random.randint(0, 1) == 0:
                df_fight_data.loc[i] = [1-x for x in df_fight_data.loc[i]]

        x = df_fight_data[filter(lambda x: x != 'winner', df_fight_data.columns)]
        y = df_fight_data[['winner']]

        model = LogisticRegression().fit(x, y)
        return model

    def predict_fight(self, fighter0, fighter1, name=True):

        if name:
            fighter0 = self.name_dict[fighter0]
            fighter1 = self.name_dict[fighter1]

        fighter0_id, fighter1_id = (str(fighter0), str(fighter1))

        self.fighter0_stats = {}
        self.fighter1_stats = {}
        to_feed = []

        for stat_type in self.columns:

            if stat_type in ('win_loss', 'sig str'):
                elos = [self.current_elo_values[fighter0_id][stat_type],
                    self.current_elo_values[fighter1_id][stat_type]]

            elif stat_type in ('head', 'body', 'leg', 'distance', 'clinch', 'ground'):
                elos = []
                mean_sd_entry = self.stat_type_mean_sd_counts[stat_type]

                for fighter_id in (fighter0_id, fighter1_id):
                    fighter_stat_types = self.current_strike_dstrbs[fighter_id]

                    stat_type_perc = fighter_stat_types[stat_type] / fighter_stat_types['sig str']\
                        if fighter_stat_types['sig str'] != 0 else 1/3

                    z_val = (stat_type_perc - mean_sd_entry['mean']) / mean_sd_entry['sd']\
                        if (mean_sd_entry['sd'] != 0 ) and (mean_sd_entry['cnt'] != 0 ) else 0

                    elos.append(scistats.norm.cdf(z_val) * self.current_elo_values[fighter_id]['sig str'])

            self.fighter0_stats[stat_type] = elos[0]
            self.fighter1_stats[stat_type] = elos[1]
            
            to_feed.append(1.0 / (1 + 1.0 * math.pow(10, (elos[1] - elos[0]) / self.divby)))

        result = self.model.predict([to_feed])
        result = result[0]
        winner_id = fighter0_id if result == 0 else fighter1_id
        return fighter_dict[winner_id]['fighter_names'][0]

        
dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d')
df_stat_data = pd.read_csv('jupyter_notebooks/data/df_stat_data_10_25.csv')
df_fight_data = pd.read_csv('jupyter_notebooks/data/df_fight_data_10_25.csv',
                            parse_dates=['date'], date_parser=dateparse)

df_results = pd.read_csv('jupyter_notebooks/data/elo_results_11_30.csv')
df_results['fighter_id'] = df_results['fighter_id'].astype(str)

with open('jupyter_notebooks/data/fighter_hist.json') as json_file:
    fighter_dict = json.load(json_file)
    
with open('jupyter_notebooks/data/fighter_name_to_id.json') as json_file:
    name_dict = json.load(json_file)

with open('jupyter_notebooks/data/current_elo_values.json') as json_file:
    current_elo_values_load = json.load(json_file)

with open('jupyter_notebooks/data/stat_type_mean_sd_counts.json') as json_file:
    stat_type_mean_sd_counts_load = json.load(json_file)

with open('jupyter_notebooks/data/current_strike_dstrbs.json') as json_file:
    current_strike_dstrbs_load = json.load(json_file)


fp = FightPredictor(df_results, df_fight_data, fighter_dict, name_dict, current_elo_values_load, 
        stat_type_mean_sd_counts_load, current_strike_dstrbs_load, 
        ['win_loss', 'head', 'body', 'leg', 'distance', 'clinch', 'ground'], divby=400)



@app.get("/predict/")
async def predict_fight(fighter0: str, fighter1: str):

    has_fighter0 = fighter0 in name_dict.keys()
    has_fighter1 = fighter1 in name_dict.keys()
    
    if not (has_fighter0 and has_fighter1):
        return {'winner':'', 'fight_info_retrieved': False, 'error': '{}{}'\
            .format(
                f'{fighter0} not recognized\n' if not has_fighter0 else '',
                f'{fighter1} not recognized\n' if not has_fighter1 else '')}

    fighter0_id, fighter1_id = str(name_dict[fighter0]), str(name_dict[fighter1])
    winner = fp.predict_fight(fighter0, fighter1, name=True)
    return {
        'error': '',
        'fight_info_retrieved': True,
        'fighter0': fighter0,
        'fighter1': fighter1,
        'winner': winner,
        'fighter_stats': fp.columns,
        'fighter0_stats': fp.fighter0_stats,
        'fighter1_stats': fp.fighter1_stats
        
    }
