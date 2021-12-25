import random

import math
from scipy import stats as scistats


from sklearn.linear_model import LogisticRegression

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
        return self.fighter_dict[winner_id]['fighter_names'][0]

if __name__ == '__main__':
    pass