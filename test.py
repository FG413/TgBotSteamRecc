import telebot
import sqlite3
from telebot import types

import Parser
import algoritm
import pandas as pd

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
    conn = sqlite3.connect('userdata.csv')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int primary key, steam text)')
    conn.commit()
    cur.close()
    conn.close()


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
    d[user_id]=steam
    print(user_id)
    #conn = sqlite3.connect('userdata.csv')
    #cur = conn.cursor()
    #cur.execute(f"INSERT INTO users (id, steam) VALUES ('%s','%s' )" % (user_id, steam))
    #user_id = 1
   # cur.execute(f"INSERT INTO users (id, steam) VALUES ('%s','%s' )" % (user_id, steam))
    #cur.execute('SELECT * FROM users')
    #users = cur.fetchall()
   # print(users)
    #cur.close()
   # conn.close()
    bot.send_message(message.chat.id, 'id считан')

dset = pd.read_csv("steam_df.csv")
dset = dset.drop("Unnamed: 0", axis=1)
@bot.message_handler(commands=['getrecommendation'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton('Страница игры в steam', url='https://store.steampowered.com/app/504230/Celeste/'))
    text = (
        'В платформере от создателей TowerFall Мэдлин сражается со своими демонами на пути к вершине горы Селеста. '
        'Преодолевай сотни хорошо продуманных сложностей, отыскивай тайники и постигай загадку горы.')
    file = open('./header.jpg', 'rb')
    par = Parser.pars(d.get(message.chat.id))
    print(par)
    df =pd.DataFrame(par, columns=['user','appid', 'rating'])

    print(df)
    print(df.axes)
    answer = list(algoritm.proxy(df))
    bot.send_photo(message.chat.id, file, caption=f'<b>{answer}</b>', parse_mode='html')
    bot.send_message(message.chat.id, '<b>Дата выхода:</b> <u>25 янв. 2018</u>\n<b>Описание:</b> В платформере от '
                                      'создателей TowerFall Мэдлин сражается со своими демонами на пути к вершине '
                                      'горы Селеста. Преодолевай сотни хорошо продуманных сложностей, '
                                      'отыскивай тайники и постигай загадку горы.\n<b>Теги:</b>  Платформер на '
                                      'точность, Сложная, Платформер', parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['getusersdata'])
def main(message):
    conn = sqlite3.connect('userdata.csv')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    info = ''
    for el in users:
        info += f'Id:{el[0]}, steam:{el[1]}\n'
    cur.close()
    conn.close()
    print(users)


bot.polling(none_stop=True)
