import requests
import bs4
from bs4 import BeautifulSoup

import numpy as np
from scipy.integrate import quad
from math import sqrt
def pars(str1):
    str2 = str(str1)
    session = requests.Session()
    login_data = {
        'username': 'prussiathegreat',
        'password': 'Pur_27_Sug'
    }
    response = session.post('https://steamcommunity.com/login/home/', data=login_data)
    username = str2
    page = requests.get('https://steamcommunity.com/id/' + username + '/games/?tab=all&xml=1')
    games = bs4.BeautifulSoup(page.text, 'xml')
    if games.find_all('error') == []:
        array = games.find_all('game')
        result = []
        for i in range(len(array)):
            arr = [username]
            a = int(array[i].appID.contents[0])
            arr.append(a)
            try:
                arr.append(float(array[i].hoursLast2Weeks.contents[0]))
            except:
                arr.append(0)
            try:
                arr.append(float(array[i].hoursOnRecord.contents[0].replace(',', '')))
            except:
                arr.append(0)
            result.append(arr)
    else:
        url = ('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=92C3748294E929E419D01B667D0EF944'
               '&steamid=') + username + '&include_played_free_games=1&format=xml'
        response = session.get(url)
        games = BeautifulSoup(response.text, 'xml')
        a = ('http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key'
             '=92C3748294E929E419D01B667D0EF944&steamid=') + username + '&format=xml'
        rs = session.get(a)
        ans = BeautifulSoup(rs.text, 'xml')
        ans = ans.find_all('message')
        result = []
        weekly = []
        for i in range(len(ans)):
            arr = [username]
            arr.append(int(ans[i].appid.contents[0]))
            arr.append(round(float(ans[i].playtime_2weeks.contents[0]) / 60, 1))
            weekly.append(arr)
        array = games.find_all('message')
        for i in range(len(array)):
            arr = [username]
            arr.append(int(array[i].appid.contents[0]))
            b = 0
            for j in range(len(weekly)):
                if weekly[j][1] == arr[1]:
                    b = weekly[j][2]
            arr.append(b)
            try:
                arr.append(round(float(array[i].playtime_forever.contents[0]) / 60, 1))
            except:
                arr.append(0)

            result.append(arr)

    if result == []:
        oshibka = "1"
        return oshibka
    def funct1(x):
        return sqrt(0.2 / x)


    def funct2(x):
        return sqrt(0.2 / x) + 4


    TotalHours = []
    Hours2Week = []
    for i in range(len(result)):
        if result[i][2] != 0:
            result[i][2] = quad(funct2, 0, result[i][2])[0]
        if result[i][3] != 0:
            result[i][3] = quad(funct1, 0, result[i][3])[0]
        TotalHours.append(result[i][3])
        Hours2Week.append(result[i][2])

    TotalHours = np.array(TotalHours)
    TotalHours = (TotalHours - TotalHours.min()) / (TotalHours.max() - TotalHours.min())
    TotalHours = list(TotalHours)
    Hours2Week = np.array(Hours2Week)
    if np.count_nonzero(Hours2Week) != 0:
        Hours2Week = (Hours2Week - Hours2Week.min()) / (Hours2Week.max() - Hours2Week.min())
    Hours2Week = list(Hours2Week)
    merged = []
    for i in range(len(TotalHours)):
        merged.append((TotalHours[i] + Hours2Week[i]) / 2)
    for row in result:
        del row[3]
    for i in range(len(result)):
        result[i][2] = merged[i]
    from operator import itemgetter

    result = sorted(result, key=itemgetter(2), reverse=True)
    return result[0:20]
