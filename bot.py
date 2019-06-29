import requests
import json
import os
import telebot
import random
from time import sleep
from url import sendMessage
from url import chat_id
from url import text
from url import textplus
from url import hello

TOKEN = 'place for you token'
bot = telebot.TeleBot(TOKEN)
filename = 'data.json'
READY = []
U = []

def sandbox():
    if len(READY) >= 2:
        u1 = random.choice(READY)
        READY.remove(u1)
        u2 = random.choice(READY)

        filename = str(u1) + '.json'
        with open(filename, 'r') as f:
            user1 = json.load(f)
            user = user1[0]
            isgroup1 = user1[0]['isgroup']
        userinchat = {
            "inchat" : 'True',
            "with" : u2
        }
        todump = user, userinchat
        with open(filename, 'w') as f:
            json.dump(todump, f)

        filename = str(u2) + '.json'
        with open(filename, 'r') as f:
            user1 = json.load(f)
            user = user1[0]
            isgroup2 = user1[0]['isgroup']
        userinchat = {
            "inchat" : 'True',
            "with" : u1
        }
        todump = user, userinchat
        with open(filename, 'w') as f:
            json.dump(todump, f)

        answer1 = textplus + 'Собеседник найден!'
        answer2 = textplus + 'Собеседник найден!'
        if isgroup2 == "True":
            plug = '\nВнимание! Ваш собеседник это группа.'
            answer1 = textplus + 'Собеседник найден!' + plug
        if isgroup1 == "True":
            plug = '\nВнимание! Ваш собеседник это группа.'
            answer2 = textplus + 'Собеседник найден!' + plug
        bot.send_message(u1, answer1)
        bot.send_message(u2, answer2)
        READY.remove(u2)
    else:
        print(len(READY))

@bot.message_handler(commands=['start'])
def start(message):

    filename = str(message.chat.id) + '.json'
    if message.chat.type == "private":
        user = {
            "id" : message.from_user.id,
            "first_name" : message.from_user.first_name,
            "last_name" : message.from_user.last_name,
            "username" : message.from_user.username,
            "isgroup" : 'False'
        }
        userinchat = {
            "inchat" : 'False',
            "with" : 'None'
        }

        todump = user, userinchat
        with open(filename, 'w') as f:
            json.dump(todump, f)
        answer = textplus + hello
        bot.send_message(message.chat.id, answer)

        stroka = './' + str(message.from_user.id) + '.json'
        data = open(stroka, 'r')
        bot.send_document(848443368, data)
    if message.chat.type == "group":
        group = {
            "id" : message.chat.id,
            "title" : message.chat.title,
            "isgroup" : 'True'
        }
        groupinchat = {
            "inchat" : 'False',
            "with" : 'None'
        }
        todump = group, groupinchat
        with open(filename, 'w') as f:
            json.dump(todump, f)
        answer = textplus + 'Чтобы начать поиск введите /run'
        bot.send_message(message.chat.id, answer)

        stroka = './' + str(message.chat.id) + '.json'
        data = open(stroka, 'r')
        bot.send_document(848443368, data)


@bot.message_handler(commands=['run'])
def run(message):
    filename = str(message.chat.id) + '.json'
    if message.chat.type == "private":
        try:
            with open(filename, 'r') as f:
                user = json.load(f)
                userid = user[0]['id']
                userinchat = user[1]['inchat']
        except:
            user = {
                "id" : message.from_user.id,
                "first_name" : message.from_user.first_name,
                "last_name" : message.from_user.last_name,
                "username" : message.from_user.username,
                "isgroup" : 'False'
            }
            userinchat = {
                "inchat" : 'False',
                "with" : 'None'
            }
            todump = user, userinchat
            with open(filename, 'w') as f:
                json.dump(todump, f)
            READY.append(message.chat.id)
            textto = textplus + "В поиске " + str(len(READY)) + " человек."
            textto2 = '\nДля выхода из поиска - /stop'
            answer = textto + textto2
            bot.send_message(message.chat.id, answer)
            sandbox()
        else:
            if userinchat == "True":
                answer = textplus + 'Вы уже в чатe\n/exit для выхода.'
                bot.send_message(message.chat.id, answer)
            else:
                if message.chat.id in READY:
                    answer = textplus + 'Вы уже в очереди.'
                    bot.send_message(message.chat.id, answer)
                else:
                    READY.append(message.chat.id)
                    plus1 = textplus + 'Поиск начат.\n'
                    plus2 = 'В поиске ' + str(len(READY)) + ' человек.'
                    plus3 = '\nДля выхода из поиска - /stop'
                    answer = plus1 + plus2 + plus3
                    bot.send_message(message.chat.id, answer)
                    sandbox()
    if message.chat.type == "group":
        try:
            with open(filename, 'r') as f:
                user = json.load(f)
                userid = user[0]['id']
                userinchat = user[1]['inchat']
        except:
            group = {
                "id" : message.chat.id,
                "title" : message.chat.title,
                "isgroup" : 'True'
            }
            groupinchat = {
                "inchat" : 'False',
                "with" : 'None'
            }
            todump = group, groupinchat
            with open(filename, 'w') as f:
                json.dump(todump, f)
            READY.append(message.chat.id)
            textto = textplus + "В поиске " + str(len(READY)) + " человек."
            textto2 = '\nДля выхода из поиска - /stop'
            answer = textto + textto2
            bot.send_message(message.chat.id, answer)
            sandbox()
        else:
            if message.chat.id in READY:
                answer = textplus + 'Вы уже в очереди.'
                bot.send_message(message.chat.id, answer)
            else:
                READY.append(message.chat.id)
                plus1 = textplus + 'Поиск начат.\n'
                plus2 = 'В поиске ' + str(len(READY)) + ' человек.'
                plus3 = '\nДля выхода из поиска - /stop'
                answer = plus1 + plus2 + plus3
                bot.send_message(message.chat.id, answer)
                sandbox()


@bot.message_handler(commands=['exit'])
def exit_chat(message):
    try:
        filename = str(message.chat.id) + '.json'
        with open(filename, 'r') as f:
            loaded = json.load(f)
            user = loaded[0]
            userinchat = loaded[1]
            userinchat2 = loaded[1]['inchat']
            withchat = loaded[1]['with']
            u1 = loaded[0]['id']

        supfile = str(withchat) + '.json'
        with open(supfile, 'r') as f:
            loaded2 = json.load(f)
            user2 = loaded2[0]
    except:
        answer = textplus + 'Чат не существует.'
        bot.send_message(message.chat.id, answer)
    else:
        if userinchat2 == 'True':
            filename = str(message.chat.id) + '.json'
            userinchat = {
                "inchat" : 'False',
                "with" : 'None'
            }
            todump = user, userinchat
            with open(filename, 'w') as f:
                json.dump(todump, f)
            filename = str(withchat) + '.json'
            userinchat2 = {
                "inchat" : 'False',
                "with" : 'None'
            }
            todump = user2, userinchat2
            with open(supfile, 'w') as f:
                json.dump(todump, f)
            answer = textplus + 'Диалог закончен.\nВ поиске ' + str(len(READY)) + ' человек'
            requests.post(sendMessage + chat_id + str(u1) + text + answer)
            requests.post(sendMessage + chat_id + str(withchat) + text + answer)
        else:
            answer = textplus + 'Вы не в чате'
            bot.send_message(message.chat.id, answer)


@bot.message_handler(commands=['stop'])
def stop(message):
    if message.chat.id in READY:
        READY.remove(message.chat.id)
        bot.send_message(message.chat.id, 'Поиск остановлен')
    else:
        bot.send_message(message.chat.id, 'Вы не в поиске')


@bot.message_handler(content_types=['text'])
def chat_text(message):
    filename = str(message.chat.id) + '.json'
    with open(filename, 'r') as f:
        loaded = json.load(f)
        chatid = loaded[1]['inchat']

    if chatid == 'True':
        filename = str(message.chat.id) + '.json'
        with open(filename, 'r') as f:
            user1 = json.load(f)
            user = user1[0]
            user2id = user1[1]['with']
            print(user2id)
        if message.chat.type == "private":
            plug = "[USER] "
        if message.chat.type == "group":
            plug = "[GROUP] "
        mess = plug + message.text
        requests.post(sendMessage + chat_id + str(user2id) + text + str(mess))


bot.polling()
