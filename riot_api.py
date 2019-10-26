import requests

#get information for input player using summoner name
def getSummonerData(region, summonerName, APIKey):
    URL = 'https://' + region + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summonerName + '?api_key=' + APIKey
    response = requests.get(URL)
    return response.json()

#get player match history using accountID
def getMatchHistory(region, accountID, APIKey):
    URL = 'https://' + region + '.api.riotgames.com/lol/match/v4/matchlists/by-account/' + accountID + '?api_key=' + APIKey
    response = requests.get(URL)
    return response.json()

#get match from match history using matchID
def getMatch(region, matchID, APIKey):
    URL = 'https://' + region + '.api.riotgames.com/lol/match/v4/matches/' + matchID + '?api_key=' + APIKey
    response = requests.get(URL)
    return response.json()

#get player info for all players in match using list of names
def getSummoners(region, summonerName_list, APIKey):
    summoners = {}
    for summonerName in summonerName_list:
        summoners[summonerName] = getSummonerData(region, summonerName, APIKey)
    return summoners

#get KDA of player using match and participantId
def getKDA(match, participantId):
    stats = match['participants'][participantId-1]["stats"]
    deaths = stats['deaths']
    if not deaths:
        deaths = 1
    return round((stats['kills'] + stats['assists'])/ deaths * 100) / 100

#get winrate of player using name and summonerID
def getWinrate(region, summonerName, summonerID, APIKey):
    URL = 'https://' + region + '.api.riotgames.com/lol/league/v4/entries/by_summoner/' + summonerID + '?api_key=' + APIKey
    response = requests.get(URL).json()
    return response[0]['wins']/(response[0]['losses'] + response[0]['wins'])

#get champion mastery using champ ID, name, and summonerID
def getChampionMastery(region, champID, summonerName, summonerID, APIKey):
    URL = 'https://' + region + '.api.riotgames.com/lol/lchampion-mastery/v4/champion-masteriess/by_summoner/' + summonerID + '?api_key=' + APIKey
    response = requests.get(URL).json()
    return response['championLevel']

#print all relevant information (in function) and return if player is "good" or "bad"
def getAllInfo(region, summonerName, summonerID, matchID, APIKey):
    good_or_bad = 'none'
    
    #access API for all relevant files
    match_JSON = getMatch(region, matchID, APIKey)
    participantId = [player['participantId'] for player in match_JSON['participantIdentities'] if player['player'][summonerId] == summonerID]
    
    #get winrate
    winrate = getWinrate(region, summonerName, summonerID, APIKey)
    print(winrate)
    #get KDA
    KDA = getKDA(match_JSON, participantId)
    print(KDA)
    #compare self gold to opponent gold

    #cs/min

    #opposing position has high KDA (>3)

    #if champion is supposed to win against opposing champ, did they win
    
    #get champ mastery of champ
    champID = 
    mastery = getChampionMastery(region, champID, summonerName, summonerID, APIKey) 

    #others?
    
    return good_or_bad

def main():
    region = (str(input('Choose region from following: ru, kr, br1, oc1, jp1, na1, eun1, euw1, tr1, la1, la2\n')))
    summonerName = str(input('Enter summoner name\n'))
    APIKey = str(input('Enter API Key\n'))

    responseJSON = getSummonerData(region, summonerName, APIKey)
    accountID = responseJSON['accountId']
    summonerID = responseJSON['Id']
    
    match_history_JSON = getMatchHistory(region, accountID, APIKey)
    recent_match = match_history_JSON['matches'][0]
    matchID = str(recent_match['gameId'])
    match_JSON = getMatch(region, matchID, APIKey)
    summoner_names = [player['player']['summonerName'] for player in match_JSON['participantIdentities']]

    teammates = []
    for summoner_name in summoner_names:
        teammates.append(getAllInfo(region, summoner_name, summonerID, matchID, APIKey))
    
    '''
    Cases: 
    self is good and majority team is bad and lost: unlucky
    self is good and majority team is good and lost: ???
    self is good and majority team is bad and won: carried garbage
    self is good and majority team is good and won: expected EZ Clap
    self is bad and majority team is bad and lost: all garbage
    self is bad and majority team is good and lost: you're garbage
    self is bad and majority team is bad and won: ???
    self is bad and majority team is good and won: got carried
    '''

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
