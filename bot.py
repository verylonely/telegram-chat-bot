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

def create_sandbox():
    if len(READY) >= 2:
        u1 = random.choice(READY)
        READY.remove(u1)
        u2 = random.choice(READY)

        filename = str(u1) + '.json'
        with open(filename, 'r') as f:
            user_1 = json.load(f)
            user = user_1[0]
            isgroup_1 = user_1[0]['isgroup']
        userinchat = {
            "inchat" : 'True',
            "with" : u2
        }
        data_to_dump = user, userinchat
        with open(filename, 'w') as f:
            json.dump(data_to_dump, f)

        filename = str(u2) + '.json'
        with open(filename, 'r') as f:
            user_1 = json.load(f)
            user = user_1[0]
            isgroup_2 = user_1[0]['isgroup']
        userinchat = {
            "inchat" : 'True',
            "with" : u1
        }
        data_to_dump = user, userinchat
        with open(filename, 'w') as f:
            json.dump(data_to_dump, f)

        answer_1 = textplus + 'Собеседник найден!'
        answer_2 = textplus + 'Собеседник найден!'
        if isgroup_2 == "True":
            plug = '\nВнимание! Ваш собеседник это группа.'
            answer_1 = textplus + 'Собеседник найден!' + plug
        if isgroup_1 == "True":
            plug = '\nВнимание! Ваш собеседник это группа.'
            answer_2 = textplus + 'Собеседник найден!' + plug
        bot.send_message(u1, answer_1)
        bot.send_message(u2, answer_2)
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

        data_to_dump = user, userinchat
        with open(filename, 'w') as f:
            json.dump(data_to_dump, f)
        answer = textplus + hello
        bot.send_message(message.chat.id, answer)

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
        data_to_dump = group, groupinchat
        with open(filename, 'w') as f:
            json.dump(data_to_dump, f)
        answer = textplus + 'Чтобы начать поиск введите /run'
        bot.send_message(message.chat.id, answer)


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
            data_to_dump = user, userinchat
            with open(filename, 'w') as f:
                json.dump(data_to_dump, f)
            READY.append(message.chat.id)
            text_to = textplus + "В поиске " + str(len(READY)) + " человек."
            text_to_2 = '\nДля выхода из поиска - /stop'
            answer = text_to + text_to_2
            bot.send_message(message.chat.id, answer)
            create_sandbox()
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
                    create_sandbox()
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
            data_to_dump = group, groupinchat
            with open(filename, 'w') as f:
                json.dump(data_to_dump, f)
            READY.append(message.chat.id)
            text_to = textplus + "В поиске " + str(len(READY)) + " человек."
            text_to_2 = '\nДля выхода из поиска - /stop'
            answer = text_to + text_to_2
            bot.send_message(message.chat.id, answer)
            create_sandbox()
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
                create_sandbox()


@bot.message_handler(commands=['exit'])
def exit_chat(message):
    try:
        filename = str(message.chat.id) + '.json'
        with open(filename, 'r') as f:
            loaded = json.load(f)
            user = loaded[0]
            userinchat = loaded[1]
            userinchat_2 = loaded[1]['inchat']
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
        if userinchat_2 == 'True':
            filename = str(message.chat.id) + '.json'
            userinchat = {
                "inchat" : 'False',
                "with" : 'None'
            }
            data_to_dump = user, userinchat
            with open(filename, 'w') as f:
                json.dump(data_to_dump, f)
            filename = str(withchat) + '.json'
            userinchat_2 = {
                "inchat" : 'False',
                "with" : 'None'
            }
            data_to_dump = user2, userinchat_2
            with open(supfile, 'w') as f:
                json.dump(data_to_dump, f)
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
            user_1 = json.load(f)
            user = user_1[0]
            user_2_id = user_1[1]['with']
            print(user_2_id)
        if message.chat.type == "private":
            plug = "[USER] "
        if message.chat.type == "group":
            plug = "[GROUP] "
        mess = plug + message.text
        requests.post(sendMessage + chat_id + str(user_2_id) + text + str(mess))


bot.polling()
