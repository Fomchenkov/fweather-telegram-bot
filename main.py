#!/usr/bin/env python3

import telebot
from telebot import types, apihelper

import config


"""
apihelper.proxy = {
	'https': 'socks5h://{}:{}@{}:{}'.format(
		config.proxy_user, config.proxy_password, 
		config.proxy_ip, config.proxy_port)
}
"""

bot = telebot.TeleBot(config.BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_command_handler(message):
    cid = message.chat.id
    uid = message.from_user.id
    return bot.send_message(cid, 'HELLO WORLD!')


@bot.message_handler(content_types=['text'])
def text_message_handler(message):
    cid = message.chat.id
    uid = message.from_user.id
    return bot.send_message(cid, message.text)


def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
