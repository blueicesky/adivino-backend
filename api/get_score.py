import falcon
import json
import sys
from get_stats import get_stats
sys.path.append("indexing/")

class get_score(object):

    def __init__(self):
        # self.predict_instance = predict()
        self.stats = get_stats()
        self.stats.get_data()
        self.stats.make_dict()

        print('hello')

    def on_get(self, req, resp):
        msg = {
            'score': '100!'
        }
        resp.body = json.dumps(msg)
        resp.status = falcon.HTTP_200
        print(resp.status)

    def on_post(self, req, resp):
        # print('post')
        # resp.body = json.dumps("yeah we can post")

        data = req.stream.read(req.content_length or 0)
        name = json.loads(data)
        player_data = self.stats.name_search(name['detected_text'])
        # print(player_data)

        # result = self.predict_instance.process_new_feature(player_json)
        # home_score = result[0]
        # away_score = result[1]
        # print result
        # result = player_json['team1_name'] + " " + str(home_score) + "-" + str(away_score) + " "+ player_json['team2_name']
        resp.status = falcon.HTTP_201
        msg = {
            'player_data': player_data
        }

        resp.body = json.dumps(msg)