import telebot
import sqlite3

bot = telebot.TeleBot('6880357616:AAE-4K9sEO02HVMF9VKTb5frlwWDEFXNWNY')
conn = sqlite3.connect('userdata.sql')
cur = conn.cursor()

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Привет')
    conn = sqlite3.connect('userdata.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int primary key, steam text)')
    conn.commit()
    cur.close()
    conn.close()


@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, 'Привет')


@bot.message_handler(commands=['setid'])
def main(message):
    bot.send_message(message.chat.id, 'пожалуйста, укажите свой steam id')
    bot.register_next_step_handler(message, read)


def read(message):
    user_id = message.chat.id
    steam = message.text.strip()
    print(user_id)
    conn = sqlite3.connect('userdata.sql')
    cur = conn.cursor()
    cur.execute(f"INSERT INTO users (id, steam) VALUES ('%s','%s' )" % (user_id, steam))
    user_id=1
    cur.execute(f"INSERT INTO users (id, steam) VALUES ('%s','%s' )" % (user_id, steam))
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    print(users)
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'id считан')


@bot.message_handler(commands=['getrecommendation'])
def main(message):
    file = open('./header.jpg', 'rb')
    bot.send_photo(message.chat.id, file)


@bot.message_handler(commands=['getusersdata'])
def main(message):
    conn = sqlite3.connect('userdata.sql')
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
