import requests

def getSummonerData(region, summonerName, APIKey):
    URL = 'https://' + region + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summonerName + '?api_key=' + APIKey
    response = requests.get(URL)
    return response.json()

def getMatchHistory(region, accountID, APIKey):
    URL = 'https://' + region + '.api.riotgames.com/lol/match/v4/matchlists/by-account/' + accountID + '?api_key=' + APIKey
    response = requests.get(URL)
    return response.json()

def getMatch(region, matchID, APIKey):
    URL = 'https://' + region + '.api.riotgames.com/lol/match/v4/matches/' + matchID + '?api_key=' + APIKey
    response = requests.get(URL)
    return response.json()

def getSummoners(region, summonerName_list, APIKey):
    summoners = {}
    for summonerName in summonerName_list:
        summoners[summonerName] = getSummonerData(region, summonerName, APIKey)
    return summoners

def main():
    region = (str(input('Choose region from following: ru, kr, br1, oc1, jp1, na1, eun1, euw1, tr1, la1, la2\n')))
    summonerName = str(input('Enter summoner name without spaces\n'))
    APIKey = str(input('Enter API Key\n'))

    responseJSON = getSummonerData(region, summonerName, APIKey)
    #accountID for summonerName
    accountID = responseJSON['accountId']
    
    match_history_JSON = getMatchHistory(region, accountID, APIKey)
    x = 3
    #look through most recent x (3) matches for accountID
    for match in match_history_JSON['matches'][:x]:
        matchID = str(match['gameId'])
        match_JSON = getMatch(region, matchID, APIKey)
        #for each match, get other 4 players
        summoner_names = [player['player']['summonerName'] for player in match_JSON['participantIdentities']]
        print(summoner_names)
        summoners = getSummoners(region, summoner_names, APIKey)
        summoners.pop(summonerName)
        #get some data for each player e.g. winrates, hotstreak(?), champion mastery/winrate, 
        #ingame data (can be found in match_JSON) such as KDA, wards placed, etc
        #also can use champion matchup data
        #possibly use data to 1.give "suggestions" for teammates; 2.state whether player's team held them back; perform other toxic actions
        '''
        for summoner in summoners:
            summoner_accountID = summoner['accountId']
        '''
        #used to find out if you really are the problem or not
        '''
        If there have been 10 murder incidents, and there is a guy who has been at the incident scenes all the time, then he must be the culprit. 
        The guy is literally you when you are on losing streak. Stop blaming your luck or teammates. 
        True or Truen't
        '''


if __name__ == '__main__':
    main()