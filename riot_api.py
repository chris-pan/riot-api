import requests

def getSummonerData(region, summonerName, APIKey):
    URL = 'https://' + region + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summonerName + '?api_key=' + APIKey
    response = requests.get(URL)
    return response.json()

def getMatchHistory(region, accountID, APIKey):
    URL = 'https://' + region + '.api.riotgames.com/lol/match/v4/matchlists/by-account/' + accountID + '?queue=420&api_key=' + APIKey
    response = requests.get(URL)
    return response.json()

def getMatch(region, matchID, APIKey):
    URL = 'https://' + region + '.api.riotgames.com/lol/match/v4/matches/' + matchID + '?api_key=' + APIKey
    response = requests.get(URL)
    return response.json()

def getMatchTimeline(region, matchID, APIKey):
    URL = 'https://' + region + '.api.riotgames.com/lol/match/v4/timelines/by-match/' + matchID + '?api_key=' + APIKey
    response = requests.get(URL)
    return response.json()

def getSummoners(region, summonerName_list, APIKey):
    summoners = {}
    for summonerName in summonerName_list:
        summoners[summonerName] = getSummonerData(region, summonerName, APIKey)
    return summoners

def getKDA(match, participantId):
    stats = match['participants'][participantId-1]["stats"]
    deaths = stats['deaths']
    if not deaths:
        deaths = 1
    return round((stats['kills'] + stats['assists'])/ deaths * 100) / 100.0

def getWinrate(region, summonerName, summonerID, APIKey):
    URL = 'https://' + region + '.api.riotgames.com/lol/league/v4/entries/by-summoner/' + summonerID + '?api_key=' + APIKey
    response = requests.get(URL).json()
    return response[0]['wins']/(response[0]['losses'] + response[0]['wins'])

def getChampionMastery(region, champID, summonerName, summonerID, APIKey):
    URL = 'https://' + region + '.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/' + summonerID + '/by-champion/' + str(champID) + '?api_key=' + APIKey
    response = requests.get(URL).json()
    if 'championLevel' in response:
        return response['championLevel'] 
    return 0

def calcJungleProximity(frames, playerID, junglerID):
    near = 0
    for f in frames:
        playerx = f['participantFrames'][str(playerID)]['position']['x']
        playery = f['participantFrames'][str(playerID)]['position']['y']
        junglerx = f['participantFrames'][str(junglerID)]['position']['x']
        junglery = f['participantFrames'][str(junglerID)]['position']['y']
        if ((playerx-junglerx)**2 + (playery-junglery)**2) ** (1/2) < 2500:
            near +=1
    return near * 100 // len(frames) / 100

def getJungleProximitytoPlayer(match, matchTimeline, participantID):
    player_jungler = 0
    enemy_jungler = 0
    for i in range(5):
        if match['participants'][i]['timeline']['lane'] == 'JUNGLE':
            player_jungler = i+1
    for i in range(5, 10):
        if match['participants'][i]['timeline']['lane'] == 'JUNGLE':
            enemy_jungler = i+1
    if participantID > 5:
        player_jungler, enemy_jungler = enemy_jungler, player_jungler
    
    #make list of frames between 3 minutes and 15 minutes
    relevant_frames= [frame for frame in matchTimeline['frames'] if frame['timestamp'] >= 180000 and frame['timestamp']<= 900000]
    
    my_jungler= calcJungleProximity(relevant_frames, participantID, player_jungler)
    their_jungler = calcJungleProximity(relevant_frames, participantID, enemy_jungler)
    return my_jungler, their_jungler


#print all relevant information (in function) and return if player is "good" or "bad"
def getAllInfo(region, summonerName, summonerID, participantId, match_JSON, match_timeline_JSON, APIKey):
    good_or_bad = 'none'
    champID = match_JSON['participants'][participantId-1]['championId']
    
    print(summonerName)
    #get winrate
    winrate = int(getWinrate(region, summonerName, summonerID, APIKey) * 1000)/10.0
    print('winrate:', str(winrate) + '%')
    #get KDA
    KDA = getKDA(match_JSON, participantId)
    print('KDA:', KDA)
    
    #jungle proximity (yours, enemy)
    jungle_proximity= getJungleProximitytoPlayer(match_JSON, match_timeline_JSON, participantId)
    print('jungle proximity (your jg, enemy jg):', jungle_proximity)

    #cs/min

    #opposing position has high KDA (>3)

    #if champion is supposed to win against opposing champ, did they win
    
    #get champ mastery of champ
    mastery = getChampionMastery(region, champID, summonerName, summonerID, APIKey) 
    print('champion mastery:', mastery)
    #others?
    
    print()
    good_or_bad = True
    return good_or_bad

def main():
    '''
    region = (str(input('Choose region from following: ru, kr, br1, oc1, jp1, na1, eun1, euw1, tr1, la1, la2\n')))
    summonerName = str(input('Enter summoner name\n'))
    APIKey = str(input('Enter API Key\n'))
    '''
    #test
    region = 'na1'
    summonerName = 'hoodc'
    APIKey = 'RGAPI-a340c2a0-c330-4555-88ab-f60112cd52d7'


    responseJSON = getSummonerData(region, summonerName, APIKey)
    accountID = responseJSON['accountId']
    summonerID = responseJSON['id']
    
    match_history_JSON = getMatchHistory(region, accountID, APIKey)
    recent_match = match_history_JSON['matches'][0]
    matchID = str(recent_match['gameId'])
    match_JSON = getMatch(region, matchID, APIKey)
    match_timeline_JSON = getMatchTimeline(region, matchID, APIKey)
    participantId = [player['participantId'] for player in match_JSON['participantIdentities'] if player['player']['summonerId'] == summonerID].pop()
    
    summoner_names = [player['player']['summonerName'] for player in match_JSON['participantIdentities']]

    teammates = []
    for summoner_name in summoner_names:
        ID = getSummonerData(region, summoner_name, APIKey)['id']
        teammates.append(getAllInfo(region, summoner_name, ID, participantId, match_JSON, match_timeline_JSON, APIKey))
    
    self_performance = teammates[participantId]
    team_performance = 0
    team = 0 if participantId < 6 else 1
    for performance in range(team*5, team*5 + 5):
        if teammates[performance]:
            team_performance+=1
        team_performance-=1
    team_performance = team_performance > 0

    game = match_JSON['teams'][team]['win'] == 'Win'
    
    print(self_performance, team_performance, game)

    #cases
    if self_performance:
        if team_performance:
            if game:
                print('expected EZ Clappo')
            else:
                print('you guys threw')
        else:
            if game:
                print('carried garbage')
            else:
                print('team sucks')
    else:
        if team_performance:
            if game:
                print('you got carried')
            else:
                print("you're garbage")
        else:
            if game:
                print('how did you win this game')
            else:
                print('you all garbage')

    #get some data for each player e.g. winrates, hotstreak(?), champion mastery/winrate, 
    #ingame data (can be found in match_JSON) such as KDA, wards placed, etc
    #also can use champion matchup data
    #possibly use data to 1.give "suggestions" for teammates; 2.state whether player's team held them back; perform other toxic actions
    #used to find out if you really are the problem or not
    '''
    If there have been 10 murder incidents, and there is a guy who has been at the incident scenes all the time, then he must be the culprit. 
    The guy is literally you when you are on losing streak. Stop blaming your luck or teammates. 
    True or Truen't
    '''


if __name__ == '__main__':
    main()
