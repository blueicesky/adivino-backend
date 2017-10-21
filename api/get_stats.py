import json
import urllib3
import csv
import datetime
import unidecode
import pandas as pd
import requests



class get_stats:

    def __init__(self):

        self.player_data_url = 'https://fantasy.premierleague.com/drf/elements/'
        self.team_code_dict = {}
        self.http = urllib3.PoolManager()
        with open('team_codes.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.team_code_dict[row['team_code']] = row['team_name']

    def get_data(self):
        http_pool = urllib3.connection_from_url(self.player_data_url)
        r = http_pool.urlopen('GET', self.player_data_url)
        myfile = r.data
        self.player_data = json.loads(myfile)

    def get_team_name(self, team_code):
        return self.team_code_dict[team_code]

    def make_dict(self):
        dictionary = {}
        dictionary['latest_player_data'] = []

        for player in self.player_data:
            print(player)
            if "Joined" in player["news"] or "Transferred" in player["news"]:
                print(player["news"])
                continue
            temp = {}
            temp['web_name'] = player['web_name'].lower()
            temp['filter_web_name'] = unidecode.unidecode(player['web_name'].lower())
            temp['team'] = self.get_team_name(str(player['team']))
            temp['first_name'] = player['first_name'].lower()
            temp['last_name'] = player['second_name'].lower()
            temp['filter_last_name'] = unidecode.unidecode(player['second_name'].lower())
            temp['fantasy_cost_change'] = float(player['cost_change_start'])
            temp['in_dreamteam'] = bool(player['in_dreamteam'])
            temp['dreamteam_count'] = float(player['dreamteam_count'])
            temp['selected_percentage'] = float(player['selected_by_percent'])
            temp['form'] = float(player['form'])
            temp['fantasy_transfers_out_in'] = float(player['transfers_out']) - float(player['transfers_in'])
            temp['fantasy_total_points'] = float(player['total_points'])
            temp['fantasy_points_per_game'] = float(player['points_per_game'])
            temp['minutes_played'] = float(player['minutes'])
            temp['goals_scored'] = float(player['goals_scored'])
            temp['assists'] = float(player['assists'])
            temp['bonus'] = float(player['bonus'])
            if player['squad_number'] == None:
                temp['squad_number'] = None
            else:
                temp['squad_number'] = float(player['squad_number'])
            temp['yellow_cards'] = float(player['yellow_cards'])
            temp['red_cards'] = float(player['red_cards'])
            temp['influence'] = float(player['influence'])
            temp['creativity'] = float(player['creativity'])
            temp['threat'] = float(player['threat'])
            temp['ict_index'] = float(player['ict_index'])
            temp['ea_index'] = float(player['ea_index'])
            dictionary['latest_player_data'].append(temp)
            print("added " + player['web_name'] + " to dictionary")

        dictionary['date_indexed'] = datetime.datetime.today()
        self.latest_player_data = pd.DataFrame(dictionary['latest_player_data'])

    def name_search(self, name):
        # stats = self.latest_player_data[self.latest_player_data['web_name'].str.contains(name)].to_dict()
        stats = self.latest_player_data[self.latest_player_data['filter_web_name'].str.contains(name)]
        result_array = []
        for item in stats.iterrows():
            result_array.append(item[1].to_dict())

        return result_array


# obj = get_stats()
# obj.get_data()
# obj.make_dict()
# print(lol.head())
# lesse = obj.name_search('rooney')
# print(lesse)
# print players.head()
# see = obj.name_search('roon')
# print(see)
# print players.info()
# for item in columns:
#     # print

