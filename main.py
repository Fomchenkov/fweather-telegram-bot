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

READY_TO_ADD_WEATHER = {}


def send_message_to_admin(text):
	"""
	Send message to admin
	"""
	for x in config.admins_id:
		try:
			bot.send_message(x, text)
		except Exception as e:
			print(e)


@bot.message_handler(commands=['start'])
def start_command_handler(message):
	cid = message.chat.id
	uid = message.from_user.id
	bot.send_message(cid, config.start_text)
	text = 'Выберите категорию'
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
	for command in config.categories:
		markup.row(command)
	return bot.send_message(cid, text, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def text_message_handler(message):
	cid = message.chat.id
	uid = message.from_user.id

	main_categories = []
	for command in config.categories:
		main_categories.append(command)
	print(main_categories)

	if uid in READY_TO_ADD_WEATHER:
		if 'low_category' not in READY_TO_ADD_WEATHER[uid]:
			if message.text not in config.categories[READY_TO_ADD_WEATHER[uid]['main_category']]:
				text = 'Выберите подкатегорию из списка!'
				return bot.send_message(cid, text)
			READY_TO_ADD_WEATHER[uid]['low_category'] = message.text
			text = 'Напишите свое описание к выбранной погоде'
			markup = types.ReplyKeyboardRemove()
			return bot.send_message(cid, text, reply_markup=markup)
		if 'description' not in READY_TO_ADD_WEATHER[uid]:
			READY_TO_ADD_WEATHER[uid]['description'] = message.text

			r_text = 'Категория:\n' + READY_TO_ADD_WEATHER[uid]['main_category'] + '\n\n'
			r_text += 'Подкатегория:\n' + READY_TO_ADD_WEATHER[uid]['low_category'] + '\n\n'
			r_text += 'Описание:\n' + READY_TO_ADD_WEATHER[uid]['description']
			send_message_to_admin(r_text)

			del READY_TO_ADD_WEATHER[uid]
			text = 'Твое сообщение - шикарно!'
			bot.send_message(cid, text)
			text = 'Спасибо'
			return bot.send_message(cid, text)


	if message.text in main_categories:
		READY_TO_ADD_WEATHER[uid] = {
			'main_category': message.text,
		}
		text = 'Отлично, выбери подкатегорию и погнали дальше'
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
		for command in config.categories[message.text]:
			markup.row(command)
		return bot.send_message(cid, text, reply_markup=markup)


def main():
	bot.polling(none_stop=True)


if __name__ == '__main__':
	main()
