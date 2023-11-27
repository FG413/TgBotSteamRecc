import requests
import bs4
def picture(game):
    page = requests.get('https://store.steampowered.com/app/'+game)
    games = bs4.BeautifulSoup(page.text, 'html.parser')
    array = games.find_all('img', class_='game_header_image_full')
    return array[0]['src']