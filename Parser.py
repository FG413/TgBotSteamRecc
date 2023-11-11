import requests
import bs4
import numpy as np
from scipy.integrate import quad
from math import sqrt
username = str(input('Please enter your steam username: '))
page = requests.get('http://steamcommunity.com/id/'+username+'/games/?tab=all&xml=1')
games = bs4.BeautifulSoup(page.text, 'xml')
array = games.find_all('game')
result = []
for i in range (len(array)):
    arr = [username]
    a = int(array[i].appID.contents[0])
    arr.append(a)
    try:
        arr.append(float(array[i].hoursLast2Weeks.contents[0]))
    except:
        arr.append(0)
    try:
        arr.append(float(array[i].hoursOnRecord.contents[0].replace(',','')))
    except:
        arr.append(0)
    result.append(arr)
def funct1(x):
    return sqrt(0.2/x)
def funct2(x):
    return sqrt(0.2/x)+4
TotalHours = []
Hours2Week = []
for i in range(len(result)):
    if result[i][2] != 0:
        result[i][2] = quad(funct2,0,result[i][2])[0]
    if result[i][3] != 0:
        result[i][3] = quad(funct1,0,result[i][3])[0]
    TotalHours.append(result[i][3])
    Hours2Week.append(result[i][2])
TotalHours = np.array(TotalHours)
TotalHours = (TotalHours - TotalHours.min())/ (TotalHours.max() - TotalHours.min())
TotalHours = list(TotalHours)
Hours2Week = np.array(Hours2Week)
Hours2Week = (Hours2Week - Hours2Week.min())/ (Hours2Week.max() - Hours2Week.min())
Hours2Week = list(Hours2Week)
merged = []
for i in range(len(TotalHours)):
    merged.append((TotalHours[i] + Hours2Week[i])/2)
for row in result:
    del row[3]
for i in range(len(result)):
    result[i][2] = merged[i]
from operator import itemgetter
result = sorted(result, key=itemgetter(2),reverse=True)
result = result[0:20]
