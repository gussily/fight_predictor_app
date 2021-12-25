
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


import pandas as pd

import json
from datetime import datetime

from app.fight_predictor import FightPredictor

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

@app.get("/all-fighters")
async def getAllFighters():
    return {
        'all_fighters': list(name_dict.keys())
    }