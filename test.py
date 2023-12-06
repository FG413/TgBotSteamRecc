import telebot
from telebot import types

import Parser
import algoritm
import pandas as pd
import urllib
import la_Finale

bot = telebot.TeleBot('6880357616:AAE-4K9sEO02HVMF9VKTb5frlwWDEFXNWNY')
d = {}


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, '<b>Приветствую!</b>\n\nПеред вами бот, который на основе вашей игровой '
                                      'библиотеки, анализируя ваши вкусы, может порекомендовать вам новые интересные '
                                      'тайтлы.\n\n Вам нужно лишь сообщить боту свой steamId и дальше он сможет '
                                      'порекомендовать вам интересные игры.\n\nЕсли вам требуется дополнительная '
                                      'информация, воспользуйтесь командой /help\n\nБот всё ещё в работе, так что вам '
                                      'могут встретиться различные мелкие баги.\n\n <b>Удачи!</b>', parse_mode='html')


@bot.message_handler(commands=['help'])
def main(message):
    file = open('./tempsnip.png', 'rb')
    bot.send_photo(message.chat.id, file, caption='Первое, что вам нужно сделать, начав работу с нашим ботом, '
                                                  'это сообщить свой'
                                                  ' <b>steamId</b>, воспользовавшись командой /setid. <u>Пожалуйста, '
                                                  'убедитесь,'
                                                  'что ваш профиль в steam открыт.</u>\n\nДалее просто воспользуйтесь '
                                                  'командой'
                                                  ' /getrecommendation и всё!\n\nБот дорабатывается, так что новые '
                                                  'функции будут'
                                                  ' добавлены в будущем.', parse_mode='html')


@bot.message_handler(commands=['setid'])
def main(message):
    bot.send_message(message.chat.id, 'пожалуйста, укажите свой steamid')
    bot.register_next_step_handler(message, read)


def read(message):
    user_id = message.chat.id
    steam = message.text.strip()
    d[user_id] = steam
    print(user_id)
    # conn = sqlite3.connect('userdata.csv')
    # cur = conn.cursor()
    # cur.execute(f"INSERT INTO users (id, steam) VALUES ('%s','%s' )" % (user_id, steam))
    # user_id = 1
    # cur.execute(f"INSERT INTO users (id, steam) VALUES ('%s','%s' )" % (user_id, steam))
    # cur.execute('SELECT * FROM users')
    # users = cur.fetchall()
    # print(users)
    # cur.close()
    # conn.close()
    bot.send_message(message.chat.id, 'id считан')


dset = pd.read_csv("steam_df.csv")
dset = dset.drop("Unnamed: 0", axis=1)


@bot.message_handler(commands=['getrecommendation'])
def main(message):
    par = Parser.pars(d.get(message.chat.id))
    print(par)
    df = pd.DataFrame(par, columns=['user', 'appid', 'rating'])
    print(df)
    df1 = la_Finale.generate_recommendationsSVD(df[df.columns[0]][0], 10)


    print(df1)

    markup = types.InlineKeyboardMarkup()
    for x in range(10):
        url = df1[x][2]
        f = open('out.jpg', 'wb')
        f.write(urllib.request.urlopen(url).read())
        f.close()
        img = open('out.jpg', 'rb')
        bot.send_photo(message.chat.id, img, caption=f'{df1[x][0]}\n\nОписание: {df1[x][1]}', parse_mode='html')
    #for i in answer:
    #    markup.add(
    #        types.InlineKeyboardButton('Страница игры в steam', url=f'https://store.steampowered.com/app/{i}/'))
    #    text = (
    #        'В платформере от создателей TowerFall Мэдлин сражается со своими демонами на пути к вершине горы Селеста. '
    #        'Преодолевай сотни хорошо продуманных сложностей, отыскивай тайники и постигай загадку горы.')
    #    file = open('./tempsnip.png', 'rb')

    #bot.send_message(message.chat.id, f'Вот ваша рекомендация: {df1[0][0]}', reply_markup=markup)
    # bot.send_photo(message.chat.id, file, caption=f'<b>{answer}</b>', parse_mode='html')


# bot.send_message(message.chat.id, '<b>Дата выхода:</b> <u>25 янв. 2018</u>\n<b>Описание:</b> В платформере от '
#                                   'создателей TowerFall Мэдлин сражается со своими демонами на пути к вершине '
#                                  'горы Селеста. Преодолевай сотни хорошо продуманных сложностей, '
#                                  'отыскивай тайники и постигай загадку горы.\n<b>Теги:</b>  Платформер на '
#                                   'точность, Сложная, Платформер', parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['getusersdata'])
def main(message):
    info = ''


bot.polling(none_stop=True)
