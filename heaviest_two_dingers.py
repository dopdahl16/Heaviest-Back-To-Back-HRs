import statsapi
import datetime
import json


def CombineWeights(batter,batter_prev,player_weights_dict):
    try:
        p1 = player_weights_dict[batter]
    except:
        print("Unable to locate player: " + str(batter))
        return None
    try:
        p2 = player_weights_dict[batter_prev]
    except:
        print("Unable to locate player: " + str(batter_prev))
        return None
    return p1 + p2



# For each year, for each day, grab game_id of every game on that day
combined_weights_of_back_to_back_homers = {}
all_games = []
today = datetime.date.today()
for year in range(1875, 2023):
    print("INCREMENT YEAR: ")
    print(year)
    date = datetime.date(year,1,1)
    date_str = ""
    yearly_players = statsapi.get('sports_players',{'season':year})['people']
    player_weights_dict = {}
    for player in yearly_players:
        player_weight = player['weight']
        player_weights_dict[player['fullName']] = player_weight
        player_weights_dict[player['nameFirstLast']] = player_weight
        player_weights_dict[player['firstLastName']] = player_weight
        player_weights_dict[player['lastFirstName']] = player_weight
        player_weights_dict[player['lastInitName']] = player_weight
        player_weights_dict[player['initLastName']] = player_weight
        player_weights_dict[player['fullFMLName']] = player_weight
        player_weights_dict[player['fullLFMName']] = player_weight
        player_weights_dict[player['nameSlug']] = player_weight
    while date_str[0:4] != str(year+1):
        date += datetime.timedelta(days=1)
        date_str = str(date)
        date_formatted = ""
        date_formatted += date_str[5:7] + "/" + date_str[8:] + "/" + date_str[0:4]
        print(date_formatted)
        games_on_date = statsapi.schedule(date=date_formatted)
        print(len(games_on_date))
        for game in range(0, len(games_on_date)):
            gamePk = games_on_date[game]['game_id']
            all_games.append(gamePk)
            ABIdx_prev = -5
            batter_prev = ""
            plays = statsapi.game_scoring_play_data(gamePk)['plays']
            for play in range(0, len(plays)):
                batter= ""
                ABIdx = plays[play]['atBatIndex']
                if "homers" in plays[play]['result']['description']:
                    homer_bool = True
                    batter = plays[play]['result']['description'][:plays[play]['result']['description'].index("homers")]
                else:
                    homer_bool = False
                if ABIdx_prev == ABIdx - 1 and homer_bool and batter and batter_prev:
                    print(batter_prev + "and " + batter + "hit back-to-back homers!")
                    combined_weight = CombineWeights(batter.strip(),batter_prev.strip(),player_weights_dict)
                    if combined_weight != None:
                        combined_weights_of_back_to_back_homers[batter_prev + "and " + batter] = (combined_weight, date_formatted)
                        print("Their combined weights were: " + str(combined_weight))
                ABIdx_prev = ABIdx
                batter_prev = batter

with open('combined_weights_of_back_to_back_homers.txt', 'w') as f:
    f.write(json.dumps(combined_weights_of_back_to_back_homers))

heaviest_duo = ""
for duo in combined_weights_of_back_to_back_homers:
    if heaviest_duo == "":
        heaviest_duo = duo
    if combined_weights_of_back_to_back_homers[duo][0] > combined_weights_of_back_to_back_homers[heaviest_duo][0]:
        heaviest_duo = duo

print(heaviest_duo, combined_weights_of_back_to_back_homers[heaviest_duo])

# # Testing area for statsapi.get method
# players = statsapi.get('sports_players',{'season':1922})
# print(type(players))
# print(len(players))
# print(players.keys())
# print(len(players['people']))
# print(type(players['people']))
# print(players['people'][5])


# # Get dictionary of player weights {id:weight}
# player_weights_dict = {}

# for year in range(1980, 1981):
#     yearly_players = statsapi.get('sports_players',{'season':year})['people']
#     for player in yearly_players:
#         player_weight = player['weight']
#         player_weights_dict[player['id']] = player_weight


# Find players that have homered back-to-back
# for gamePk in range():
#     for play in range(0, len(statsapi.game_scoring_play_data(gamePk)['plays'])):
#         ABIdx = statsapi.game_scoring_play_data(gamePk)['plays'][play]['atBatIndex']



