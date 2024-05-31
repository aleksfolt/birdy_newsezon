# -*- coding: utf-8 -*-
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import telebot
from telebot import types
import json
import time
from os import path
import random
from PIL import Image
from io import BytesIO
import os
import logging
from aiocryptopay import AioCryptoPay, Networks
from datetime import datetime, timedelta
import re
import asyncio
import threading


def config_func():
	with open('config.json', 'r', encoding='utf-8') as file:
		data = json.load(file)
	return data

Ñonfig_data = config_func()

bot = telebot.TeleBot(Ñonfig_data['token'])
crypto = AioCryptoPay(token='184441:AAVfvJNbxjFh4FyvqvlHjym8TzlX8gtmTxr', network=Networks.MAIN_NET)
telebot.apihelper.READ_TIMEOUT = 60

DATA_FILE = 'tea_data_2.json'
DATA_FILE_2 = 'users_cards.json'
DATA_FILE_3 = "promo.json"
tea_names = Ñonfig_data['tea_names']
birds = Ñonfig_data['birds']
products = Ñonfig_data['products']
user_button = {}
loop = asyncio.new_event_loop()

def start_loop():
	asyncio.set_event_loop(loop)
	loop.run_forever()

thread = threading.Thread(target=start_loop)
thread.start()

def run_async(coro):
	future = asyncio.run_coroutine_threadsafe(coro, loop)
	return future.result()

if not path.exists(DATA_FILE):
	with open(DATA_FILE, 'w') as f:
		json.dump({}, f)

if not path.exists(DATA_FILE_3):
	with open(DATA_FILE_3, 'w') as f:
		json.dump({}, f)

if not path.exists(DATA_FILE_2):
	with open(DATA_FILE_2, 'w') as f:
		json.dump({}, f)

if not path.exists("user_coins.json"):
	with open("user_coins.json", 'w') as f:
		json.dump({}, f)


def load_data():
	with open(DATA_FILE, 'r') as f:
		return json.load(f)

def load_data_cards():
	with open(DATA_FILE_2, 'r') as f:
		return json.load(f)


def save_data(data):
	with open(DATA_FILE, 'w') as f:
		json.dump(data, f)


def save_data_2(data):
	try:
		with open(DATA_FILE_2, 'w') as f:
			json.dump(data, f)
		print("Data successfully saved.")
	except Exception as e:
		print(f"Failed to save data: {e}")



def load_premium_users():
	try:
		with open("birdy_premium_users.json", "r") as f:
			return json.load(f)
	except FileNotFoundError:
		return {}


def save_premium_users(users):
	with open("birdy_premium_users.json", "w") as f:
		json.dump(users, f, indent=4)


@bot.message_handler(commands=['start'])
def start_command(message):
	first_name = message.from_user.first_name
	text = f'''Ð¥ÐµÐµÐ¹ ðŸ•Š {first_name}! Ð¯ Birdy. Ð‘Ð¾Ñ‚ Ð´Ð»Ñ Ñ€Ð°Ð·Ð²Ð»ÐµÑ‡ÐµÐ½Ð¸Ð¹, Ñ‚ÑƒÑ‚ Ð¼Ð¾Ð¶ÐµÑˆÑŒ Ð¿Ð¸Ñ‚ÑŒ Ñ‡Ð°Ð¹ Ð¸Ð»Ð¸ Ð¾Ñ‚ÐºÑ€Ñ‹Ð²Ð°Ñ‚ÑŒ ÐºÐ°Ñ€Ñ‚Ð¾Ñ‡ÐºÐ¸, Ð²ÑÐµ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ‹ Ð¼Ð¾Ð¶Ð½Ð¾ Ð¿Ð¾ÑÐ¼Ð¾Ñ‚Ñ€ÐµÑ‚ÑŒ Ð¿Ð¾ ÐºÐ¾Ð¼Ð°Ð½Ð´Ðµ /help.'''
	bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help'])
def help_command(message):
	text = '''
ÐšÑ€Ð°Ñ‚ÐºÐ¾Ðµ Ð¾Ð¿Ð¸ÑÐ°Ð½Ð¸Ðµ ÐºÐ¾Ð¼Ð°Ð½Ð´:
/profile, "ÐŸÑ€Ð¾Ñ„Ð¸Ð»ÑŒ" - Ð²Ð°Ñˆ Ð¿Ñ€Ð¾Ñ„Ð¸Ð»ÑŒ
/chai, "Ð§Ð°Ð¹" - Ð²Ñ‹Ð¿Ð¸Ñ‚ÑŒ Ñ‡Ð°Ð¹
/chai\_top, "Ð¢Ð¾Ð¿ Ñ‡Ð°Ñ" - Ñ‚Ð¾Ð¿ Ð¿Ð¾ Ñ‡Ð°ÑŽ
/knock, "ÐŸÐ¾Ð»ÑƒÑ‡Ð¸Ñ‚ÑŒ ÐºÐ°Ñ€Ñ‚Ñƒ" - Ð½Ð°Ð±Ð»ÑŽÐ´ÐµÐ½Ð¸Ðµ Ð·Ð° Ð¿Ñ‚Ð¸Ñ‡ÐºÐ°Ð¼Ð¸"
/cards\_top "Ð¢Ð¾Ð¿ ÐºÐ°Ñ€Ñ‚Ð¾Ñ‡ÐµÐº" - Ñ‚Ð¾Ð¿ ÐºÐ°Ñ€Ñ‚Ð¾Ñ‡ÐµÐº Ð¿Ð¾ Ð¿Ð¾Ð¸Ð½Ñ‚Ð°Ð¼ Ð¸ ÐºÐ¾Ð»Ð¸Ñ‡ÐµÑÑ‚Ð²Ñƒ
/krone, "ÐœÐ¾Ð½ÐµÑ‚Ð°", "ÐšÑ€Ð¾Ð½Ð°" - Ð¿Ð¾Ð»ÑƒÑ‡ÐµÐ½Ð¸Ðµ Ð¼Ð¾Ð½ÐµÑ‚
/shop, "ÐœÐ°Ð³Ð°Ð·Ð¸Ð½" - Ð¼Ð°Ð³Ð°Ð·Ð¸Ð½, Ñ Ñ‚Ð¾Ð²Ð°Ñ€Ð°Ð¼Ð¸ Ð·Ð° Ð¼Ð¾Ð½ÐµÑ‚Ñ‹
/goods, "ÐŸÐ¾ÐºÑƒÐ¿ÐºÐ¸" - Ð²Ð°ÑˆÐ¸ Ð¿Ð¾ÐºÑƒÐ¿ÐºÐ¸

ÐŸÐ¾Ð»Ð½Ñ‹Ð¹ ÑÐ¿Ð¸ÑÐ¾Ðº ÐºÐ¾Ð¼Ð°Ð½Ð´ Ñ Ð¾Ð¿Ð¸ÑÐ°Ð½Ð¸ÐµÐ¼ [Ñ‚ÑƒÑ‚](https://teletype.in/@hlb_folt/jNICgr9tP50).'''
	bot.send_message(message.chat.id, text, parse_mode='Markdown', disable_web_page_preview=True)


def update_user_data(user_id, username, coins=0, purchase=None, last_request_time=None):
	try:
		with open("user_coins.json", 'r') as file:
			data = json.load(file)
	except FileNotFoundError:
		data = {}

	if user_id not in data:
		data[user_id] = {"username": username, "coins": 0, "purchases": [], "last_request_time": 0}

	data[user_id]['coins'] += coins
	if purchase:
		data[user_id]['purchases'].append(purchase)
	if last_request_time is not None:
		data[user_id]['last_request_time'] = last_request_time

	with open("user_coins.json", 'w') as file:
		json.dump(data, file, indent=4)


def chai_top(message):
	try:
		data = load_data()
		sorted_data = sorted(data.items(), key=lambda x: x[1]['total_volume'], reverse=True)
		top_10 = sorted_data[:10]

		premium_users = load_premium_users() 
		
		message_text = "Ð¢Ð¾Ð¿-10 Ð¿Ð¾Ð»ÑŒÐ·Ð¾Ð²Ð°Ñ‚ÐµÐ»ÐµÐ¹ Ð¿Ð¾ Ð¾Ð±ÑŠÐµÐ¼Ñƒ Ð²Ñ‹Ð¿Ð¸Ñ‚Ð¾Ð³Ð¾ Ñ‡Ð°Ñ:\n\n"
		for i, (user_id, user_data) in enumerate(top_10, 1):
			nickname = user_data.get('nickname', 'Unknown')
			total_volume = user_data['total_volume']

			if user_id in premium_users:
				premium_icon = "ðŸ’Ž"
			else:
				premium_icon = ""

			if i == 1:
				comment = " - ÐšÐ¾Ñ€Ð¾Ð»ÑŒ"
			elif 2 <= i <= 3:
				comment = " - Ð“ÐµÑ€Ñ†Ð¾Ð³"
			elif 4 <= i <= 5:
				comment = " - ÐœÐ°Ñ€ÐºÐ¸Ð·"
			elif 6 <= i <= 7:
				comment = " - Ð“Ñ€Ð°Ñ„"
			elif 8 <= i <= 9:
				comment = " - Ð’Ð¸ÐºÐ¾Ð½Ñ‚"
			elif i == 10:
				comment = " - Ð‘Ð°Ñ€Ð¾Ð½"

			message_text += f"{i}. {premium_icon} {nickname}: {total_volume} Ð¼Ð». {comment}\n"

		bot.send_message(message.chat.id, message_text)
	except Exception as e:
		bot.send_message(message.chat.id, "Ð’Ñ€ÐµÐ¼ÐµÐ½Ð½Ð°Ñ Ð¾ÑˆÐ¸Ð±ÐºÐ° Ð² Ð¾Ð±Ñ€Ð°Ð±Ð¾Ñ‚ÐºÐµ, Ð¿Ð¾Ð²Ñ‚Ð¾Ñ€Ð¸Ñ‚Ðµ Ð¿Ð¾Ð·Ð¶Ðµ.")
		bot.send_message(1130692453, f"ÐŸÑ€Ð¾Ð¸Ð·Ð¾ÑˆÐ»Ð° Ð¾ÑˆÐ¸Ð±ÐºÐ° Ð¿Ñ€Ð¸ Ð¾Ð±Ñ€Ð°Ð±Ð¾Ñ‚ÐºÐµ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ‹: /chai_top Ð² Ñ‡Ð°Ñ‚Ðµ: {message.chat.id}. {e}")


def send_random_tea(message):
	user_id = str(message.from_user.id)
	user_nickname = message.from_user.first_name
	data = load_data()
	total_volume = data.get(user_id, {'total_volume': 0, 'last_drink_time': 0})

	if 'nickname' not in total_volume:
		total_volume['nickname'] = user_nickname

	time_since_last_drink = time.time() - total_volume['last_drink_time']
	time_left = max(0, 600 - time_since_last_drink)

	if time_since_last_drink < 600:
		remaining_minutes = int(time_left // 60)
		remaining_seconds = int(time_left % 60)
		bot.reply_to(message, f"ÐŸÐ¾Ð¶Ð°Ð»ÑƒÐ¹ÑÑ‚Ð°, Ð¿Ð¾Ð´Ð¾Ð¶Ð´Ð¸Ñ‚Ðµ ÐµÑ‰Ðµ {remaining_minutes} Ð¼Ð¸Ð½ÑƒÑ‚ {remaining_seconds} ÑÐµÐºÑƒÐ½Ð´ Ð¿ÐµÑ€ÐµÐ´ ÑÐ»ÐµÐ´ÑƒÑŽÑ‰ÐµÐ¹ Ñ‡Ð°ÑˆÐºÐ¾Ð¹ Ñ‡Ð°Ñ.")
		return

	random_tea = random.choice(tea_names)
	premium_users = load_premium_users()
	is_premium = user_id in premium_users and datetime.fromisoformat(premium_users[user_id]) > datetime.now()
	if is_premium:
		random_volume = random.randint(500, 2000)
	else:
		random_volume = random.randint(200, 2000)
	bot.reply_to(message, f"{total_volume['nickname']} Ð’Ñ‹ ÑƒÑÐ¿ÐµÑˆÐ½Ð¾ Ð²Ñ‹Ð¿Ð¸Ð»Ð¸ Ñ‡Ð°Ð¹\n\nÐ’Ñ‹Ð¿Ð¸Ñ‚Ð¾: {random_volume} Ð¼Ð».\nÐ§Ð°Ð¹: {random_tea}\n\nÐ’ÑÐµÐ³Ð¾ Ð²Ñ‹Ð¿Ð¸Ñ‚Ð¾: {total_volume['total_volume'] + random_volume} Ð¼Ð».")

	data[user_id] = {'total_volume': total_volume['total_volume'] + random_volume, 'last_drink_time': time.time(), 'nickname': user_nickname}
	save_data(data)


def knock_cards_function(message):
	user_id = str(message.from_user.id)
	user_nickname = message.from_user.first_name
	data = load_data_cards()
	user_data = data.get(user_id, {'birds': [], 'last_usage': 0, 'points': 0, 'nickname': user_nickname})
	user_data['points'] = int(user_data['points'])
	time_since_last_usage = time.time() - user_data['last_usage']
	time_left = max(0, 21600 - time_since_last_usage)

	with open('user_coins.json', 'r+') as file:
		data_coins = json.load(file)
		user_data_coins = data_coins.get(user_id, {})

	inventory = user_data_coins.get('purchases', [])

	default_wait = 21600
	if "Ð‘Ð¸Ð½Ð¾ÐºÐ»ÑŒ Carl Zeiss Jena 40x105." in inventory:
		default_wait = min(default_wait, 12060)
	if "Ð‘Ð¸Ð½Ð¾ÐºÐ»ÑŒ Fujinon 25x150 MT-SX" in inventory:
		default_wait = min(default_wait, 15300)
	if "Ð‘Ð¸Ð½Ð¾ÐºÐ»ÑŒ Celestron SkyMaster 25x100" in inventory:
		default_wait = min(default_wait, 18360)
	if "Ð‘Ð¸Ð½Ð¾ÐºÐ»ÑŒ Canon 18x50 IS All Weather" in inventory:
		default_wait = min(default_wait, 19440)

	if time_since_last_usage < default_wait:
		remaining_time = default_wait - time_since_last_usage
		remaining_hours = int(remaining_time // 3600)
		remaining_minutes = int((remaining_time % 3600) // 60)
		remaining_seconds = int(remaining_time % 60)
		bot.reply_to(message, f"Ð’Ð°Ð¼ Ð½ÑƒÐ¶Ð½Ð¾ Ð¿ÐµÑ€ÐµÐ´Ð¾Ñ…Ð½ÑƒÑ‚ÑŒ ðŸ˜´ {remaining_hours} Ñ‡Ð°ÑÐ¾Ð² {remaining_minutes} Ð¼Ð¸Ð½ÑƒÑ‚ {remaining_seconds} ÑÐµÐºÑƒÐ½Ð´ Ð¿ÐµÑ€ÐµÐ´ ÑÐ»ÐµÐ´ÑƒÑŽÑ‰ÐµÐ¼ Ð½Ð°Ð±Ð»ÑŽÐ´ÐµÐ½Ð¸ÐµÐ¼ Ð·Ð° Ð¿Ñ‚Ð¸Ñ‡ÐºÐ°Ð¼Ð¸!")
		return

	random_number = random.randint(1, 95)
	if 0 <= random_number <= 14 or ("Ð¥Ð»ÐµÐ±, ÐžÐ¿Ð¸ÑÐ°Ð½Ð¸Ðµ: Ð¿Ð¾Ð²Ñ‹ÑˆÐµÐ½Ð¸Ðµ ÑˆÐ°Ð½ÑÐ¾Ð² Ð½Ð° Ð»ÐµÐ³ÐµÐ½Ð´Ð°Ñ€Ð½ÑƒÑŽ Ð¿Ñ‚Ð¸Ñ‡ÐºÑƒ Ð½Ð° Ð¾Ð´Ð¸Ð½ Ñ€Ð°Ð·." in inventory and 0 <= random_number <= 30):
		eligible_birds = [bird for bird in birds if bird["rarity"] == "Ð›ÐµÐ³ÐµÐ½Ð´Ð°Ñ€Ð½Ð°Ñ"]
	elif 15 <= random_number <= 29:
		eligible_birds = [bird for bird in birds if bird["rarity"] == "ÐœÐ¸Ñ„Ð¸Ñ‡ÐµÑÐºÐ°Ñ"]
	elif 30 <= random_number <= 49:
		eligible_birds = [bird for bird in birds if bird["rarity"] == "Ð¡Ð²ÐµÑ€Ñ…Ñ€ÐµÐ´ÐºÐ°Ñ"]
	elif 50 <= random_number <= 95:
		eligible_birds = [bird for bird in birds if bird["rarity"] == "Ð ÐµÐ´ÐºÐ°Ñ"]

	if eligible_birds:
		chosen_bird = random.choice(eligible_birds)
		photo_data = chosen_bird['photo']
		if chosen_bird['name'] in user_data['birds']:
			with open(photo_data, 'rb') as photo_file:
				bot.send_photo(message.chat.id, photo_file, caption=f"Ð’Ð°Ð¼ Ð¿Ð¾Ð¿Ð°Ð»Ð°ÑÑŒ Ð¿Ð¾Ð²Ñ‚Ð¾Ñ€ÐºÐ° {chosen_bird['name']}! Ð‘ÑƒÐ´ÑƒÑ‚ Ð½Ð°Ñ‡Ð¸ÑÐ»ÐµÐ½Ñ‹ Ñ‚Ð¾Ð»ÑŒÐºÐ¾ Ð¾Ñ‡ÐºÐ¸.\nÐ ÐµÐ´ÐºÐ¾ÑÑ‚ÑŒ: {chosen_bird['rarity']}\n+{chosen_bird['points']} Ð¾Ñ‡ÐºÐ¾Ð².\nÐžÐ±Ð¸Ñ‚Ð°Ð½Ð¸Ðµ: {chosen_bird['place']}\n\nÐ’ÑÐµÐ³Ð¾ Ð¿Ð¾Ð¸Ð½Ñ‚Ð¾Ð²: {user_data['points'] + int(chosen_bird['points'])}")
			user_data['points'] += int(chosen_bird['points'])
		else:
			with open(photo_data, 'rb') as photo_file:
				bot.send_photo(message.chat.id, photo_file, caption=f"Ð˜Ð· Ð²Ð°ÑˆÐ¸Ñ… Ð½Ð°Ð±Ð»ÑŽÐ´ÐµÐ½Ð¸Ð¹ Ð²Ñ‹ Ð¾Ñ‚ÐºÑ€Ñ‹Ð»Ð¸ Ð½Ð¾Ð²ÑƒÑŽ Ð¿Ñ‚Ð¸Ñ†Ñƒ: {chosen_bird['name']}\nÐ ÐµÐ´ÐºÐ¾ÑÑ‚ÑŒ: {chosen_bird['rarity']}\nÐžÑ‡ÐºÐ¸: {chosen_bird['points']}\nÐžÐ±Ð¸Ñ‚Ð°Ð½Ð¸Ðµ: {chosen_bird['place']}")
			user_data['birds'].append(chosen_bird['name'])
			user_data['points'] += int(chosen_bird['points'])
		user_data['last_usage'] = time.time()
		data[user_id] = user_data
		save_data_2(data)

		if "Ð¥Ð»ÐµÐ±, ÐžÐ¿Ð¸ÑÐ°Ð½Ð¸Ðµ: Ð¿Ð¾Ð²Ñ‹ÑˆÐµÐ½Ð¸Ðµ ÑˆÐ°Ð½ÑÐ¾Ð² Ð½Ð° Ð»ÐµÐ³ÐµÐ½Ð´Ð°Ñ€Ð½ÑƒÑŽ Ð¿Ñ‚Ð¸Ñ‡ÐºÑƒ Ð½Ð° Ð¾Ð´Ð¸Ð½ Ñ€Ð°Ð·." in inventory:
			inventory.remove("Ð¥Ð»ÐµÐ±, ÐžÐ¿Ð¸ÑÐ°Ð½Ð¸Ðµ: Ð¿Ð¾Ð²Ñ‹ÑˆÐµÐ½Ð¸Ðµ ÑˆÐ°Ð½ÑÐ¾Ð² Ð½Ð° Ð»ÐµÐ³ÐµÐ½Ð´Ð°Ñ€Ð½ÑƒÑŽ Ð¿Ñ‚Ð¸Ñ‡ÐºÑƒ Ð½Ð° Ð¾Ð´Ð¸Ð½ Ñ€Ð°Ð·.")
			data_coins[user_id]['purchases'] = inventory
		else:
			pass

		with open('user_coins.json', 'w') as file:
			json.dump(data_coins, file, indent=4)
			print("ÑÐ¾Ñ…Ñ€Ð°Ð½ÐµÐ½Ð¾")


@bot.callback_query_handler(func=lambda call: call.data.startswith('show_cards'))
def show_knock_cards(call):
	user_id = str(call.from_user.id)
	user_nickname = call.from_user.first_name
	unique_number = int(call.data.split('_')[-1])
	if user_button.get(user_id) != unique_number:
			bot.answer_callback_query(call.id, "ÐÐµ Ð²Ð°ÑˆÐ° ÐºÐ½Ð¾Ð¿ÐºÐ°.", show_alert=True)
			return
	data = load_data_cards()
	user_data = data.get(user_id, {'birds': [], 'last_usage': 0, 'points': 0, 'nickname': user_nickname})
	collected_cards = len(user_data['birds'])
	total_cards = len(birds)
	if user_data['birds']:
		birds_owned_by_user = {bird['name'] for bird in birds if bird['name'] in user_data['birds']}
		rarities = {bird['rarity'] for bird in birds if bird['name'] in birds_owned_by_user}
		keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
		for rarity in rarities:
			keyboard.add(telebot.types.InlineKeyboardButton(text=rarity, callback_data=f'show_{rarity}'))
		try:
			bot.send_message(call.from_user.id, f"Ð£ Ð²Ð°Ñ ÑÐ¾Ð±Ñ€Ð°Ð½Ð¾ {collected_cards} Ð¸Ð· {total_cards} Ð²Ð¾Ð·Ð¼Ð¾Ð¶Ð½Ñ‹Ñ…\nÐ’Ñ‹Ð±ÐµÑ€Ð¸Ñ‚Ðµ Ñ€ÐµÐ´ÐºÐ¾ÑÑ‚ÑŒ:", reply_markup=keyboard)
			chat_type = call.message.chat.type
			if chat_type in ['group', 'supergroup']:
					bot.send_message(call.message.chat.id, f"{call.from_user.first_name}, ÐºÐ°Ñ€Ñ‚Ð¾Ñ‡ÐºÐ¸ Ð¾Ñ‚Ð¿Ñ€Ð°Ð²Ð»ÐµÐ½Ñ‹ Ð²Ð°Ð¼ Ð² Ð»Ð¸Ñ‡Ð½Ñ‹Ðµ ÑÐ¾Ð¾Ð±Ñ‰ÐµÐ½Ð¸Ñ!")
			else:
					pass
		except telebot.apihelper.ApiException as e:
				logging.error(f"ÐÐµ ÑƒÐ´Ð°Ð»Ð¾ÑÑŒ Ð¾Ñ‚Ð¿Ñ€Ð°Ð²Ð¸Ñ‚ÑŒ ÑÐ¾Ð¾Ð±Ñ‰ÐµÐ½Ð¸Ðµ: {str(e)}")
				bot.send_message(call.message.chat.id, "ÐÐ°Ð¿Ð¸ÑˆÐ¸Ñ‚Ðµ Ð±Ð¾Ñ‚Ñƒ Ñ‡Ñ‚Ð¾-Ñ‚Ð¾ Ð² Ð»Ð¸Ñ‡Ð½Ñ‹Ðµ ÑÐ¾Ð¾Ð±Ñ‰ÐµÐ½Ð¸Ñ, Ñ‡Ñ‚Ð¾Ð±Ñ‹ Ð¾Ñ‚Ð¿Ñ€Ð°Ð²Ð¸Ñ‚ÑŒ Ð²Ð°Ð¼ ÐºÐ°Ñ€Ñ‚Ð¾Ñ‡ÐºÐ¸!")
	else:
		bot.send_message(call.message.chat.id, "Ð’Ñ‹ Ð¿Ð¾ÐºÐ° Ñ‡Ñ‚Ð¾ Ð½Ðµ Ð½Ð°Ð±Ð»ÑŽÐ´Ð°Ð»Ð¸ Ð·Ð° Ð¿Ñ‚Ð¸Ñ‡ÐºÐ°Ð¼Ð¸.")


@bot.callback_query_handler(func=lambda call: call.data.startswith('show_'))
def show_cards(call):
	rarity = call.data[len('show_'):]
	user_id = str(call.from_user.id)
	user_nickname = call.from_user.first_name
	data = load_data_cards()
	user_data = data.get(user_id, {'birds': [], 'last_usage': 0, 'points': 0, 'nickname': user_nickname})
	rarity_cards = [bird for bird in birds if bird['name'] in user_data['birds'] and bird['rarity'] == rarity]

	if rarity_cards:
		for bird in rarity_cards:
			photo_data = bird['photo']
			caption = f"{bird['name']}\nÐ ÐµÐ´ÐºÐ¾ÑÑ‚ÑŒ: {bird['rarity']}"
			if 'points' in bird:
				caption += f"\nÐžÑ‡ÐºÐ¸: {bird['points']}"
			caption += f"\nÐžÐ±Ð¸Ñ‚Ð°Ð½Ð¸Ðµ: {bird['place']}"
			with open(photo_data, 'rb') as photo_file:
				chat_type = call.message.chat.type
				bot.send_photo(call.message.chat.id, photo_file, caption=caption)
	else:
		bot.send_message(call.message.chat.id, f"Ð£ Ð²Ð°Ñ Ð½ÐµÑ‚ ÐºÐ°Ñ€Ñ‚Ð¾Ñ‡ÐµÐº Ñ€ÐµÐ´ÐºÐ¾ÑÑ‚Ð¸ {rarity}")


def handle_stocoin(message):
	try:
		user_id = str(message.from_user.id)
		username = message.from_user.username
		current_time = time.time()

		try:
			with open("user_coins.json", 'r') as file:
				data = json.load(file)
		except FileNotFoundError:
			data = {}

		last_request_time = data.get(user_id, {}).get("last_request_time", 0)
		if current_time - last_request_time < 1500:  # 5 minutes cooldown
			remaining_time = 1500 - (current_time - last_request_time)
			minutes, seconds = divmod(remaining_time, 60)
			bot.reply_to(message, f"Ð’Ñ‹ ÑƒÐ¶Ðµ Ð¿Ð¾Ð»ÑƒÑ‡Ð¸Ð»Ð¸ ÐºÑ€Ð¾Ð½Ñ‹. ÐŸÐ¾Ð¿Ñ€Ð¾Ð±ÑƒÐ¹Ñ‚Ðµ Ñ‡ÐµÑ€ÐµÐ· {int(minutes)} Ð¼Ð¸Ð½ÑƒÑ‚ {int(seconds)} ÑÐµÐºÑƒÐ½Ð´.")
			return

		premium_users = load_premium_users()
		is_premium = user_id in premium_users and datetime.fromisoformat(premium_users[user_id]) > datetime.now()

		if is_premium:
			coins = random.randint(1, 20)
		else:
			coins = random.randint(1, 10)
		update_user_data(user_id, username, coins)

		with open("user_coins.json", 'r') as file:
			data = json.load(file)
		if user_id not in data:
			data[user_id] = {"username": username, "coins": coins, "purchases": [], "last_request_time": current_time}
		else:
			data[user_id]["last_request_time"] = current_time
		with open("user_coins.json", 'w') as file:
			json.dump(data, file, indent=4)

		bot.reply_to(message, f"Ð’Ñ‹ ÑƒÑÐ¿ÐµÑˆÐ½Ð¾ Ð·Ð°Ñ€Ð°Ð±Ð¾Ñ‚Ð°Ð»Ð¸ {coins} Ð·Ð¾Ð»Ð¾Ñ‚Ñ‹Ñ… ÐºÑ€Ð¾Ð½.")
	except Exception as e:
		bot.send_message(message.chat.id, f"Ð’Ñ€ÐµÐ¼ÐµÐ½Ð½Ð°Ñ Ð¾ÑˆÐ¸Ð±ÐºÐ° Ð² Ð¾Ð±Ñ€Ð°Ð±Ð¾Ñ‚ÐºÐµ, Ð¿Ð¾Ð²Ñ‚Ð¾Ñ€Ð¸Ñ‚Ðµ Ð¿Ð¾Ð·Ð¶Ðµ!")
		print(e)



def handle_shop(message):
	try:
		user_id = str(message.from_user.id)
		username = message.from_user.username
		current_time = time.time()
		unique_number = random.randint(1000, 99999999)
		user_button[user_id] = unique_number


		try:
			with open("user_coins.json", 'r') as file:
				data = json.load(file)
		except FileNotFoundError:
			bot.send_message(message.chat.id, "ÐžÑˆÐ¸Ð±ÐºÐ°: Ð´Ð°Ð½Ð½Ñ‹Ðµ Ð¿Ð¾Ð»ÑŒÐ·Ð¾Ð²Ð°Ñ‚ÐµÐ»ÐµÐ¹ Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½Ñ‹.")
			return

		user_data = data.get(user_id, {})
		coins = user_data.get("coins", 0)

		last_request_time = user_data.get("last_request_time", 0)
		remaining_time = max(0, 1500 - (current_time - last_request_time))
		minutes, seconds = divmod(remaining_time, 60)

		if remaining_time > 0:
			time_message = f" Ð”Ð¾ ÑÐ»ÐµÐ´ÑƒÑŽÑ‰ÐµÐ³Ð¾ Ð¿Ð¾Ð»ÑƒÑ‡ÐµÐ½Ð¸Ñ ÐºÐ¾Ð¹Ð½Ð¾Ð² Ð¾ÑÑ‚Ð°Ð»Ð¾ÑÑŒ {int(minutes)} Ð¼Ð¸Ð½. {int(seconds)} ÑÐµÐº."
		else:
			time_message = ""

		shop_message = f"Ð’Ð°Ñˆ Ñ‚ÐµÐºÑƒÑ‰Ð¸Ð¹ Ð±Ð°Ð»Ð°Ð½Ñ: {coins} ÐºÑ€Ð¾Ð½Ñ‹." + time_message + "\nÐ’Ñ‹Ð±ÐµÑ€Ð¸Ñ‚Ðµ Ñ‚Ð¾Ð²Ð°Ñ€:"
		markup = types.InlineKeyboardMarkup(row_width=8)
		for product_id, product_info in products.items():
			button = types.InlineKeyboardButton(text=product_info["name"], callback_data=f"buy_{product_id}_{unique_number}")
			markup.add(button)
		bot.send_message(message.chat.id, shop_message, reply_markup=markup)
	except Exception as e:
		bot.send_message(message.chat.id, f"ÐŸÑ€Ð¾Ð¸Ð·Ð¾ÑˆÐ»Ð° Ð¾ÑˆÐ¸Ð±ÐºÐ° {e} (Ð½Ð°Ð¿Ð¸ÑˆÐ¸Ñ‚Ðµ @AleksFolt)")


@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def handle_buy_query(call):
	product_id, unique_number = call.data.split('_')[1:3]
	user_id = str(call.from_user.id)
	
	if user_button.get(user_id) != int(unique_number):
		bot.answer_callback_query(call.id, "ÐÐµ Ð²Ð°ÑˆÐ° ÐºÐ½Ð¾Ð¿ÐºÐ°.", show_alert=True)
		return

	product = products[product_id]
	markup = types.InlineKeyboardMarkup()
	buy_button = types.InlineKeyboardButton(text="ÐšÑƒÐ¿Ð¸Ñ‚ÑŒ", callback_data=f"confirm_{product_id}_{unique_number}")
	markup.add(buy_button)
	
	with open(product["image"], "rb") as photo:
		bot.send_photo(call.message.chat.id, photo, caption=f"{product['name']} - Ð¦ÐµÐ½Ð°: {product['price']} ÐºÑ€Ð¾Ð½.", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('confirm_'))
def confirm_purchase(call):
	user_id = str(call.from_user.id)
	product_id = call.data.split('_')[1]
	unique_number = int(call.data.split('_')[2])
	product = products[product_id]
	if user_button.get(user_id) != unique_number:
		bot.answer_callback_query(call.id, "ÐÐµ Ð²Ð°ÑˆÐ° ÐºÐ½Ð¾Ð¿ÐºÐ°.", show_alert=True)
		return

	with open("user_coins.json", 'r') as file:
		data = json.load(file)

	if data[user_id]["coins"] >= product["price"]:
		if product["name"] in data[user_id]["purchases"]:
			bot.answer_callback_query(call.id, f"Ð—Ð°Ñ‡ÐµÐ¼ Ñ‚ÐµÐ±Ðµ Ð´Ð²Ð° Ñ‚Ð°ÐºÐ¸Ñ…? ðŸ¤¨")
			return
		data[user_id]["coins"] -= product["price"]
		data[user_id]["purchases"].append(product["name"])
		with open("user_coins.json", 'w') as file:
			json.dump(data, file, indent=4)
		bot.answer_callback_query(call.id, f"ÐŸÐ¾ÐºÑƒÐ¿ÐºÐ° ÑƒÑÐ¿ÐµÑˆÐ½Ð°! Ð’Ñ‹ Ð¿Ñ€Ð¸Ð¾Ð±Ñ€ÐµÐ»Ð¸ {product['name']}.")
	else:
		bot.answer_callback_query(call.id, "ÐÐµÐ´Ð¾ÑÑ‚Ð°Ñ‚Ð¾Ñ‡Ð½Ð¾ Ð·Ð¾Ð»Ð¾Ñ‚Ñ‹Ñ… ÐºÑ€Ð¾Ð½ Ð´Ð»Ñ Ð¿Ð¾ÐºÑƒÐ¿ÐºÐ¸. Ð—Ð°Ñ€Ð°Ð±Ð°Ñ‚Ñ‹Ð²Ð°Ð¹ Ð±Ð¾Ð»ÑŒÑˆÐµ!")


def handle_goods(message):
	try:
		user_id = str(message.from_user.id)
		with open("user_coins.json", 'r') as file:
			data = json.load(file)
		purchases = data.get(user_id, {}).get("purchases", [])
		response = "Ð’Ð°ÑˆÐ¸ Ñ‚Ð¾Ð²Ð°Ñ€Ñ‹:\n" + "\n".join(purchases) if purchases else "Ð’Ñ‹ ÐµÑ‰Ðµ Ð½Ð¸Ñ‡ÐµÐ³Ð¾ Ð½Ðµ ÐºÑƒÐ¿Ð¸Ð»Ð¸."
		bot.send_message(message.chat.id, response)
	except Exception as e:
		bot.send_message(message.chat.id, f"ÐŸÑ€Ð¾Ð¸Ð·Ð¾ÑˆÐ»Ð° Ð¾ÑˆÐ¸Ð±ÐºÐ° {e} (Ð½Ð°Ð¿Ð¸ÑˆÐ¸Ñ‚Ðµ @AleksFolt)")


def cards_top(message):
	try:
		inline_markup = InlineKeyboardMarkup()
		button_1 = InlineKeyboardButton(text="Ð¢Ð¾Ð¿ Ð¿Ð¾ ÐºÐ°Ñ€Ñ‚Ð¾Ñ‡ÐºÐ°Ð¼", callback_data="top_cards_cards")
		button_2 = InlineKeyboardButton(text="Ð¢Ð¾Ð¿ Ð¿Ð¾ Ð¾Ñ‡ÐºÐ°Ð¼", callback_data="top_cards_point")
		inline_markup.add(button_1, button_2)
		bot.send_message(message.chat.id, "Ð¢Ð¾Ð¿ 10 Ð¿Ð¾Ð»ÑŒÐ·Ð¾Ð²Ð°Ñ‚ÐµÐ»ÐµÐ¹ Ð¿Ð¾ ÐºÐ°Ñ€Ñ‚Ð¾Ñ‡ÐºÐ°Ð¼. Ð’Ñ‹Ð±ÐµÑ€Ð¸Ñ‚Ðµ ÐºÐ½Ð¾Ð¿ÐºÑƒ:", reply_markup=inline_markup)
	except Exception as e:
		print(f"Error: {e}")
		bot.send_message(message.chat.id, "Ð’Ñ€ÐµÐ¼ÐµÐ½Ð½Ð°Ñ Ð¾ÑˆÐ¸Ð±ÐºÐ° Ð² Ð¾Ð±Ñ€Ð°Ð±Ð¾Ñ‚ÐºÐµ, Ð¿Ð¾Ð²Ñ‚Ð¾Ñ€Ð¸ Ð¿Ð¾Ð·Ð¶Ðµ.")


@bot.callback_query_handler(func=lambda call: call.data.startswith('top_cards_'))
def cards_top_callback(call):
    choice = call.data.split('_')[2]
    data = load_data_cards()
    user_id = str(call.message.from_user.id)
    user_data = data.get(user_id, {'points': 0, 'birds': []})
    if choice == "cards":
        sorted_data = sored(data.items(), key=lambda x: len(x[1].get('birds', [])), reverse=True)
        top_10 = sorted_data[:10]

        message_text = "Ð¢Ð¾Ð¿-10 Ð¿Ð¾Ð»ÑŒÐ·Ð¾Ð²Ð°Ñ‚ÐµÐ»ÐµÐ¹ Ð¿Ð¾ ÐºÐ¾Ð»Ð¸Ñ‡ÐµÑÑ‚Ð²Ñƒ ÑÐ¾Ð±Ñ€Ð°Ð½Ð½Ñ‹Ñ… ÐºÐ°Ñ€Ñ‚Ð¾Ñ‡ÐµÐº:\n\n"
        for i, (user_id, user_data) in enumerate(top_10, 1):
            nickname = user_data.get('nickname', 'Unknown')
            num_cards = len(user_data.get('birds', []))
            message_text += f"{i}. {nickname}: {num_cards} ÐºÐ°Ñ€Ñ‚Ð¾Ñ‡ÐµÐº\n"

        bot.send_message(call.message.chat.id, message_text)
    elif choice == "point":
        sorted_data_points = sorted(data.items(), key=lambda x: x[1].get('points', 0), reverse=True)
        top_10 = sorted_data_points[:10]

        message_text = "Ð¢Ð¾Ð¿-10 Ð¿Ð¾Ð»ÑŒÐ·Ð¾Ð²Ð°Ñ‚ÐµÐ»ÐµÐ¹ Ð¿Ð¾ ÐºÐ¾Ð»Ð¸Ñ‡ÐµÑÑ‚Ð²Ñƒ Ð½Ð°Ð±Ñ€Ð°Ð½Ð½Ñ‹Ñ… Ð¾Ñ‡ÐºÐ¾Ð²:\n\n"
        for j, (user_id, user_data) in enumerate(top_10, 1):
            nickname_2 = user_data.get('nickname', 'Unknown')
            points = user_data.get('points', 0)
            message_text += f"{j}. {nickname_2}: {points} Ð¾Ñ‡ÐºÐ¾Ð²\n"

        bot.send_message(call.message.chat.id, message_text)


def handle_profile(message, background_image_path="background_image.jpg"):
	waiting = bot.send_message(message.chat.id, "ÐžÑ‚ÐºÑ€Ñ‹Ð²Ð°ÑŽ Ð¿Ñ€Ð¾Ñ„Ð¸Ð»ÑŒ...")
	user_id = message.from_user.id
	str_user_id = str(user_id)
	first_name = message.from_user.first_name
	last_name = message.from_user.last_name or ""
	
	replied_user_id = None
	if message.reply_to_message:
		replied_user_id = message.reply_to_message.from_user.id
	
	if replied_user_id:
		user_id = replied_user_id
		str_user_id = str(user_id)
		first_name = message.reply_to_message.from_user.first_name
		last_name = message.reply_to_message.from_user.last_name or ""

	data = load_data_cards()
	user_data = data.get(str_user_id, {'birds': [], 'last_usage': 0, 'points': 0, 'nickname': first_name})
	collected_cards = len(user_data['birds'])
	total_cards = len(birds)
	try:
		with open("user_coins.json", 'r') as file:
			data_coin = json.load(file)
	except FileNotFoundError:
		bot.send_message(message.chat.id, "ÐžÑˆÐ¸Ð±ÐºÐ°: Ð´Ð°Ð½Ð½Ñ‹Ðµ Ð¿Ð¾Ð»ÑŒÐ·Ð¾Ð²Ð°Ñ‚ÐµÐ»ÐµÐ¹ Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½Ñ‹.")
		return

	user_data_coin = data_coin.get(str_user_id, {})
	premium_users = load_premium_users()
	coins = user_data_coin.get("coins", 0)
	if str_user_id in premium_users:
		expiration_time = datetime.fromisoformat(premium_users[str_user_id])
		remaining_time = expiration_time - datetime.now()
		if remaining_time.total_seconds() > 0:
			days = remaining_time.days
			hours = remaining_time.seconds // 3600
			minutes = (remaining_time.seconds % 3600) // 60
			premium_status = f"Ð°ÐºÑ‚Ð¸Ð²ÐµÐ½, Ð·Ð°ÐºÐ¾Ð½Ñ‡Ð¸Ñ‚ÑÑ Ñ‡ÐµÑ€ÐµÐ· {days} Ð´Ð½ÐµÐ¹ {hours} Ñ‡Ð°ÑÐ¾Ð² {minutes} Ð¼Ð¸Ð½ÑƒÑ‚"
		else:
			premium_status = "Ð¸ÑÑ‚ÐµÐº"
	else:
		premium_status = "Ð½Ðµ Ð°ÐºÑ‚Ð¸Ð²ÐµÐ½"
	caption = f"ðŸ¡ Ð›Ð¸Ñ‡Ð½Ñ‹Ð¹ Ð¿Ñ€Ð¾Ñ„Ð¸Ð»ÑŒ {first_name} {last_name}\nðŸƒ Ð¡Ð¾Ð±Ñ€Ð°Ð½Ð¾ {collected_cards} ÐºÐ°Ñ€Ñ‚Ð¾Ñ‡ÐµÐº Ð¸Ð· {total_cards} Ð²Ð¾Ð·Ð¼Ð¾Ð¶Ð½Ñ‹Ñ….\nðŸª™ Ð’Ð°Ñˆ Ð±Ð°Ð»Ð°Ð½Ñ ÐºÑ€Ð¾Ð½: {coins} ÐºÑ€Ð¾Ð½.\nðŸ† Ð‘Ð°Ð»Ð°Ð½Ñ Ð¿Ð¾Ð¸Ð½Ñ‚Ð¾Ð²: {user_data['points']}\nðŸ’Ž ÐŸÑ€ÐµÐ¼Ð¸ÑƒÐ¼ ÑÑ‚Ð°Ñ‚ÑƒÑ: {premium_status}"

	user_profile_photos = bot.get_user_profile_photos(user_id, limit=1)
	if user_profile_photos.photos:
			photo = user_profile_photos.photos[0][-1]
			file_id = photo.file_id
			file_info = bot.get_file(file_id)
			downloaded_file = bot.download_file(file_info.file_path)
			avatar_stream = BytesIO(downloaded_file)
	else:
			avatar_stream = open("avatar.jpg", 'rb')

	avatar_image = Image.open(avatar_stream)

	if avatar_image.mode != 'RGBA':
			avatar_image = avatar_image.convert('RGBA')

	background_image = Image.open(background_image_path)
	if background_image.mode != 'RGBA':
			background_image = background_image.convert('RGBA')

	avatar_image = avatar_image.resize((378, 398), Image.Resampling.LANCZOS)

	x = 275
	y = 144
	background_image.paste(avatar_image, (x, y), avatar_image)

	final_image_stream = BytesIO()
	background_image.save(final_image_stream, format='PNG')
	final_image_stream.seek(0)
	final_image_stream.name = 'modified_image.jpg'

	unique_number = random.randint(1000, 99999999)
	user_button[str_user_id] = unique_number
	keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
	button_1 = telebot.types.InlineKeyboardButton(text="ÐœÐ¾Ð¸ ÐºÐ°Ñ€Ñ‚Ð¾Ñ‡ÐºÐ¸", callback_data=f'show_cards_{unique_number}')
	button_2 = telebot.types.InlineKeyboardButton(text="ÐšÑƒÐ¿Ð¸Ñ‚ÑŒ ÐºÑ€ÑƒÑ‚ÐºÑƒ", callback_data=f'crutka_cards_{unique_number}')
	button_3 = telebot.types.InlineKeyboardButton(text="ÐŸÑ€ÐµÐ¼Ð¸ÑƒÐ¼", callback_data=f'birdy_prem_{unique_number}')
	keyboard.add(button_1, button_2, button_3)
	bot.delete_message(message.chat.id, waiting.message_id)
	bot.send_photo(message.chat.id, photo=final_image_stream, caption=caption, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith(f'birdy_prem'))
def crutki(call):
	unique_number = int(call.data.split('_')[-1])
	user_id = str(call.from_user.id)
	if user_button.get(user_id) != unique_number:
		bot.answer_callback_query(call.id, "ÐÐµ Ð²Ð°ÑˆÐ° ÐºÐ½Ð¾Ð¿ÐºÐ°.", show_alert=True)
		return
	bot.send_message(call.message.chat.id, "ðŸ’Ž Birdy Premium\n\nÐŸÑ€ÐµÐ¸Ð¼ÑƒÑ‰ÐµÑÑ‚Ð²Ð°:\nÐšÑ€Ð¾Ð½Ñ‹ Ð²Ñ‹Ð´Ð°ÑŽÑ‚ÑÑ Ð¾Ñ‚ 1 Ð´Ð¾ 20 Ð²Ð¼ÐµÑÑ‚Ð¾ 1 Ð´Ð¾ 10.\nÐ§Ð°Ð¹ Ð²Ñ‹Ð´Ð°ÐµÑ‚ÑÑ Ð¾Ñ‚ 500 Ð´Ð¾ 2000 Ð²Ð¼ÐµÑÑ‚Ð¾ 200 Ð´Ð¾ 2000.\nÐ’ Ñ‚Ð¾Ð¿Ðµ Ñ‡Ð°Ñ Ð¾Ñ‚Ð¾Ð±Ñ€Ð°Ð¶Ð°ÐµÑ‚ÑÑ Ð°Ð»Ð¼Ð°Ð·.\nÐ’ Ð±ÑƒÐ´ÑƒÑ‰ÐµÐ¼ Ð±ÑƒÐ´ÐµÑ‚ Ð´Ð¾Ð±Ð°Ð²Ð»ÐµÐ½Ð¾ Ð±Ð¾Ð»ÑŒÑˆÐµ Ð²ÑÐµÐ³Ð¾.\n\nÐŸÐ¾ÐºÑƒÐ¿ÐºÐ°:\nÐšÐ¾Ð¼Ð°Ð½Ð´Ð°: /prem.\nÐžÐ¿Ð»Ð°Ñ‚Ð° USDT, @CryptoBot")


@bot.callback_query_handler(func=lambda call: call.data.startswith(f'crutka_cards'))
def crutki(call):
	unique_number = int(call.data.split('_')[-1])
	user_id = str(call.from_user.id)
	if user_button.get(user_id) != unique_number:
		bot.answer_callback_query(call.id, "ÐÐµ Ð²Ð°ÑˆÐ° ÐºÐ½Ð¾Ð¿ÐºÐ°.", show_alert=True)
		return
	data = load_data_cards()
	user_nickname = call.from_user.first_name
	user_data = data.get(user_id, {'birds': [], 'last_usage': 0, 'points': 0, 'nickname': user_nickname})
	keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
	button_1 = telebot.types.InlineKeyboardButton(text="ÐšÑƒÐ¿Ð¸Ñ‚ÑŒ", callback_data=f'buying_crutka_{unique_number}')
	keyboard.add(button_1)
	bot.send_message(call.message.chat.id, f"ÐšÑƒÐ¿Ð¸Ñ‚ÑŒ ÐºÑ€ÑƒÑ‚ÐºÑƒ. Ð¦ÐµÐ½Ð°: 35000 Ð¿Ð¾Ð¸Ð½Ñ‚Ð¾Ð²:\nÐ‘Ð°Ð»Ð°Ð½Ñ Ð¿Ð¾Ð¸Ð½Ñ‚Ð¾Ð²: {user_data['points']}", reply_markup=keyboard)
	

@bot.callback_query_handler(func=lambda call: call.data.startswith('buying_crutka'))
def buy_crutka(call):
	user_id = str(call.from_user.id)
	unique_number = int(call.data.split('_')[-1])
	if user_button.get(user_id) != unique_number:
		bot.answer_callback_query(call.id, "ÐÐµ Ð²Ð°ÑˆÐ° ÐºÐ½Ð¾Ð¿ÐºÐ°.", show_alert=True)
		return
	data = load_data_cards()
	user_nickname = call.from_user.first_name
	user_data = data.get(user_id, {'birds': [], 'last_usage': 0, 'points': 0, 'nickname': user_nickname})
	if user_data['points'] >= 35000:
		eligible_birds = [bird for bird in birds if bird["rarity"] == "ÐšÑ€ÑƒÑ‚ÐºÐ°"]
		chosen_bird = None
		attempt_count = 0
		while attempt_count < 100:
			chosen_bird = random.choice(eligible_birds)
			if chosen_bird['name'] not in user_data['birds']:
				break
			attempt_count += 1
		
		if chosen_bird and chosen_bird['name'] not in user_data['birds']:
			user_data['birds'].append(chosen_bird['name'])
			user_data['points'] -= 35000
			data[user_id] = user_data
			save_data_2(data)
			photo_data = chosen_bird['photo']
			with open(photo_data, 'rb') as photo_file:
				bot.send_photo(call.message.chat.id, photo_file, caption=f"{user_nickname} Ð’Ð°Ð¼ Ð²Ñ‹Ð¿Ð°Ð»Ð° {chosen_bird['name']}!")
		else:
			bot.send_message(call.message.chat.id, f"{user_nickname} Ð’Ñ‹ ÑƒÐ¶Ðµ ÑÐ¾Ð±Ñ€Ð°Ð»Ð¸ Ð²ÑÐµ ÐºÑ€ÑƒÑ‚ÐºÐ¸.")
	else:
		bot.send_message(call.message.chat.id, f"{user_nickname} ÐÐµÐ´Ð¾ÑÑ‚Ð°Ñ‚Ð¾Ñ‡Ð½Ð¾ Ð¾Ñ‡ÐºÐ¾Ð² Ð´Ð»Ñ Ð¿Ð¾ÐºÑƒÐ¿ÐºÐ¸!")



async def create_and_send_invoice(sender_id, is_group=False, message=None):
	try:
		invoice = await crypto.create_invoice(asset='USDT', amount=0.5)
		if not invoice:
			if is_group:
				bot.send_message(message.chat.id, "ÐžÑˆÐ¸Ð±ÐºÐ° Ð¿Ñ€Ð¸ ÑÐ¾Ð·Ð´Ð°Ð½Ð¸Ð¸ Ð¸Ð½Ð²Ð¾Ð¹ÑÐ°. ÐŸÐ¾Ð¶Ð°Ð»ÑƒÐ¹ÑÑ‚Ð°, Ð½Ð°Ð¿Ð¸ÑˆÐ¸Ñ‚Ðµ Ñ‡Ñ‚Ð¾-Ñ‚Ð¾ Ð±Ð¾Ñ‚Ñƒ Ð² Ð»Ð¸Ñ‡ÐºÑƒ.")
			else:
				bot.send_message(sender_id, "ÐžÑˆÐ¸Ð±ÐºÐ° Ð¿Ñ€Ð¸ ÑÐ¾Ð·Ð´Ð°Ð½Ð¸Ð¸ Ð¸Ð½Ð²Ð¾Ð¹ÑÐ°. ÐŸÐ¾Ð¿Ñ€Ð¾Ð±ÑƒÐ¹Ñ‚Ðµ Ð¿Ð¾Ð·Ð¶Ðµ.")
			return None

		markup = types.InlineKeyboardMarkup()
		url_requisites = types.InlineKeyboardButton(text="ÐžÐ¿Ð»Ð°Ñ‚Ð¸Ñ‚ÑŒ", url=invoice.bot_invoice_url)
		markup.add(url_requisites)
		if is_group:
			bot.send_message(message.chat.id, "Ð ÐµÐºÐ²Ð¸Ð·Ð¸Ñ‚Ñ‹ Ð´Ð»Ñ Ð¾Ð¿Ð»Ð°Ñ‚Ñ‹ Ð¾Ñ‚Ð¿Ñ€Ð°Ð²Ð»ÐµÐ½Ñ‹ Ð² Ð»Ð¸Ñ‡Ð½Ñ‹Ðµ ÑÐ¾Ð¾Ð±Ñ‰ÐµÐ½Ð¸Ñ.")
			bot.send_message(sender_id, f"ÐŸÑ€ÐµÐ¼Ð¸ÑƒÐ¼ Ð°ÐºÑ‚Ð¸Ð²Ð¸Ñ€ÑƒÐµÑ‚ÑÑ Ñ‡ÐµÑ€ÐµÐ· 100 ÑÐµÐºÑƒÐ½Ð´ Ð² ÑÐ»ÑƒÑ‡Ð°Ðµ ÑƒÑÐ¿ÐµÑˆÐ½Ð¾Ð¹ Ð¾Ð¿Ð»Ð°Ñ‚Ñ‹. Ð•ÑÐ»Ð¸ Ð²Ñ‹ Ð¾Ð¿Ð»Ð°Ñ‚Ð¸Ñ‚Ðµ Ñ‡ÐµÐº Ð¿Ð¾ÑÐ»Ðµ Ð¸ÑÑ‚ÐµÑ‡ÐµÐ½Ð¸Ñ Ð²Ñ€ÐµÐ¼ÐµÐ½Ð¸ Ð²Ñ‹ Ð¿Ð¾Ñ‚ÐµÑ€ÑÐµÑ‚Ðµ Ð´ÐµÐ½ÑŒÐ³Ð¸! Ð ÐµÐºÐ²Ð¸Ð·Ð¸Ñ‚Ñ‹: {invoice.bot_invoice_url}", reply_markup=markup)
		else:
			bot.send_message(sender_id, f"ÐŸÑ€ÐµÐ¼Ð¸ÑƒÐ¼ Ð°ÐºÑ‚Ð¸Ð²Ð¸Ñ€ÑƒÐµÑ‚ÑÑ Ñ‡ÐµÑ€ÐµÐ· 100 ÑÐµÐºÑƒÐ½Ð´ Ð² ÑÐ»ÑƒÑ‡Ð°Ðµ ÑƒÑÐ¿ÐµÑˆÐ½Ð¾Ð¹ Ð¾Ð¿Ð»Ð°Ñ‚Ñ‹. Ð•ÑÐ»Ð¸ Ð²Ñ‹ Ð¾Ð¿Ð»Ð°Ñ‚Ð¸Ñ‚Ðµ Ñ‡ÐµÐº Ð¿Ð¾ÑÐ»Ðµ Ð¸ÑÑ‚ÐµÑ‡ÐµÐ½Ð¸Ñ Ð²Ñ€ÐµÐ¼ÐµÐ½Ð¸ Ð²Ñ‹ Ð¿Ð¾Ñ‚ÐµÑ€ÑÐµÑ‚Ðµ Ð´ÐµÐ½ÑŒÐ³Ð¸! Ð ÐµÐºÐ²Ð¸Ð·Ð¸Ñ‚Ñ‹: {invoice.bot_invoice_url}", reply_markup=markup)
		return invoice 
	except Exception as e:
		if is_group:
			bot.send_message(message.chat.id, "ÐŸÑ€Ð¾Ð¸Ð·Ð¾ÑˆÐ»Ð° Ð¾ÑˆÐ¸Ð±ÐºÐ° Ð¿Ñ€Ð¸ ÑÐ¾Ð·Ð´Ð°Ð½Ð¸Ð¸ Ð¸Ð½Ð²Ð¾Ð¹ÑÐ°. ÐŸÐ¾Ð¶Ð°Ð»ÑƒÐ¹ÑÑ‚Ð°, Ð½Ð°Ð¿Ð¸ÑˆÐ¸Ñ‚Ðµ Ñ‡Ñ‚Ð¾-Ñ‚Ð¾ Ð±Ð¾Ñ‚Ñƒ Ð² Ð»Ð¸Ñ‡ÐºÑƒ.")
		else:
			bot.send_message(sender_id, f"ÐžÑˆÐ¸Ð±ÐºÐ° Ð¿Ñ€Ð¸ ÑÐ¾Ð·Ð´Ð°Ð½Ð¸Ð¸ Ð¸Ð½Ð²Ð¾Ð¹ÑÐ°: {e}")
		return None

def check_payment(sender_id, invoice_url):
	status = run_async(get_invoice_status(invoice_url))
	if status == 'paid':
		premium_users = load_premium_users()
		if str(sender_id) in premium_users:
			current_expiration = datetime.fromisoformat(premium_users[str(sender_id)])
			new_expire_time = (current_expiration + timedelta(days=30)).isoformat()
		else:
			new_expire_time = (datetime.now() + timedelta(days=30)).isoformat()
		premium_users[str(sender_id)] = new_expire_time
		save_premium_users(premium_users)
		bot.send_message(sender_id, "ðŸŒŸ Ð¡Ð¿Ð°ÑÐ¸Ð±Ð¾ Ð·Ð° Ð¿Ð¾ÐºÑƒÐ¿ÐºÑƒ ÐŸÑ€ÐµÐ¼Ð¸ÑƒÐ¼Ð°! ÐÐ°ÑÐ»Ð°Ð¶Ð´Ð°Ð¹Ñ‚ÐµÑÑŒ ÑÐºÑÐºÐ»ÑŽÐ·Ð¸Ð²Ð½Ñ‹Ð¼Ð¸ Ð¿Ñ€ÐµÐ¸Ð¼ÑƒÑ‰ÐµÑÑ‚Ð²Ð°Ð¼Ð¸.")
	else:
		bot.send_message(sender_id, "ÐžÐ¿Ð»Ð°Ñ‚Ð° Ð½Ðµ Ð¿Ñ€Ð¾ÑˆÐ»Ð°! ÐŸÐ¾Ð¿Ñ€Ð¾Ð±ÑƒÐ¹Ñ‚Ðµ ÐµÑ‰Ðµ Ñ€Ð°Ð·.")

async def get_invoice_status(invoice):
	try:
		invoice = await crypto.get_invoices(invoice_ids=invoice.invoice_id)
		return invoice.status
	except Exception as e:
		print(f"ÐžÑˆÐ¸Ð±ÐºÐ° Ð¿Ñ€Ð¸ Ð¿Ð¾Ð»ÑƒÑ‡ÐµÐ½Ð¸Ð¸ Ð´Ð°Ð½Ð½Ñ‹Ñ… Ð¸Ð½Ð²Ð¾Ð¹ÑÐ°: {e}")
		return None


def buy_premium(message):
	sender_id = message.from_user.id
	if message.chat.type == "private":
		invoice = run_async(create_and_send_invoice(sender_id, message=message))
		if invoice:
			t = threading.Timer(100, check_payment, args=(sender_id, invoice))
			t.start()
		else:
			bot.send_message(sender_id, "ÐÐµ ÑƒÐ´Ð°Ð»Ð¾ÑÑŒ ÑÐ¾Ð·Ð´Ð°Ñ‚ÑŒ Ð¸Ð½Ð²Ð¾Ð¹Ñ.")
	else: 
		invoice = run_async(create_and_send_invoice(sender_id, is_group=True, message=message))
		if not invoice:
			bot.send_message(message.chat.id, "ÐŸÑ€Ð¾Ð¸Ð·Ð¾ÑˆÐ»Ð° Ð¾ÑˆÐ¸Ð±ÐºÐ° Ð¿Ñ€Ð¸ ÑÐ¾Ð·Ð´Ð°Ð½Ð¸Ð¸ Ð¸Ð½Ð²Ð¾Ð¹ÑÐ°. ÐŸÐ¾Ð¶Ð°Ð»ÑƒÐ¹ÑÑ‚Ð°, Ð½Ð°Ð¿Ð¸ÑˆÐ¸Ñ‚Ðµ Ñ‡Ñ‚Ð¾-Ñ‚Ð¾ Ð±Ð¾Ñ‚Ñƒ Ð² Ð»Ð¸Ñ‡ÐºÑƒ.")


@bot.message_handler(commands=['admin_send_files'])
def handle_send_files(message):
    try:
        user_id = message.from_user.id
        if user_id != 1130692453:
            bot.send_message(message.chat.id, "Ð£ Ð²Ð°Ñ Ð½ÐµÑ‚ Ð¿Ñ€Ð°Ð² Ð½Ð° Ð²Ñ‹Ð¿Ð¾Ð»Ð½ÐµÐ½Ð¸Ðµ ÑÑ‚Ð¾Ð¹ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ‹!")
            return
        filenames = message.text.split()[1:]
        if len(filenames) == 0:
            bot.reply_to(message, "ÐŸÐ¾Ð¶Ð°Ð»ÑƒÐ¹ÑÑ‚Ð°, ÑƒÐºÐ°Ð¶Ð¸Ñ‚Ðµ Ð¸Ð¼ÐµÐ½Ð° Ñ„Ð°Ð¹Ð»Ð¾Ð² Ð´Ð»Ñ Ð¾Ñ‚Ð¿Ñ€Ð°Ð²ÐºÐ¸.")
            return
        send_files(message.chat.id, filenames)
    except Exception as e:
        bot.reply_to(message, f"ÐžÑˆÐ¸Ð±ÐºÐ°: {e}")
        print(f"ÐžÑˆÐ¸Ð±ÐºÐ°: {e}")  # Ð’Ñ‹ÐÐ¾Ð´Ð¸Ð¼ Ð¾ÑˆÐ¸Ð±ÐºÑƒ Ð² ÐºÐ¾Ð½ÑÐ¾Ð»ÑŒ Ð´Ð»Ñ Ð¾Ñ‚Ð»Ð°Ð´ÐºÐ¸

def send_files(chat_id, filenames):
    try:
        for filename in filenames:
            with open(filename, 'rb') as file:
                bot.send_document(chat_id, file)
    except Exception as e:
        bot.send_message(chat_id, f"ÐÐµ ÑƒÐ´Ð°Ð»Ð¾ÑÑŒ Ð¾Ñ‚Ð¿Ñ€Ð°Ð²Ð¸Ñ‚ÑŒ Ñ„Ð°Ð¹Ð» {filename}: {e}")
        print(f"ÐÐµ ÑƒÐ´Ð°Ð»Ð¾ÑÑŒ Ð¾Ñ‚Ð¿Ñ€Ð°Ð²Ð¸Ñ‚ÑŒ Ñ„Ð°Ð¹Ð» {filename}: {e}")


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    try:
        if message.text in ["/chai", "Ñ‡Ð°Ð¹", "Ð§Ð°Ð¹"]:
            send_random_tea(message)
        elif message.text in ["/chai_top", "Ñ‡Ð°Ð¹ Ñ‚Ð¾Ð¿", "Ð§Ð°Ð¹ Ñ‚Ð¾Ð¿", "Ð¢Ð¾Ð¿ Ñ‡Ð°Ñ", "Ñ‚Ð¾Ð¿ Ñ‡Ð°Ñ"]:
            chai_top(message)
        elif message.text in ["/knock", "ÐºÐ½Ð¾Ðº", "ÐšÐ½Ð¾Ðº", "Ð¿Ð¾Ð»ÑƒÑ‡Ð¸Ñ‚ÑŒ ÐºÐ°Ñ€Ñ‚Ñƒ", "ÐŸÐ¾Ð»ÑƒÑ‡Ð¸Ñ‚ÑŒ ÐºÐ°Ñ€Ñ‚Ñƒ"]:
            knock_cards_function(message)
        elif message.text in ["/krone", "ÐºÑ€Ð¾Ð½Ð°", "ÐšÑ€Ð¾Ð½Ð°", "Ð¼Ð¾Ð½ÐµÑ‚Ð°", "ÐœÐ¾Ð½ÐµÑ‚Ð°"]:
            handle_stocoin(message)
        elif message.text in ["/shop", "Ð¼Ð°Ð³Ð°Ð·Ð¸Ð½", "ÐœÐ°Ð³Ð°Ð·Ð¸Ð½", "ÑˆÐ¾Ð¿", "Ð¨Ð¾Ð¿"]:
            handle_shop(message)
        elif message.text in ["/goods", "ÐŸÐ¾ÐºÑƒÐ¿ÐºÐ¸", "Ð¿Ð¾ÐºÑƒÐ¿ÐºÐ¸"]:
            handle_goods(message)
        elif message.text in ["/profile", "ÐŸÑ€Ð¾Ñ„Ð¸Ð»ÑŒ", "Ð¿Ñ€Ð¾Ñ„Ð¸Ð»ÑŒ"]:
            handle_profile(message)
        elif message.text in ["/cards_top", "Ð¢Ð¾Ð¿ ÐºÐ°Ñ€Ñ‚Ð¾Ñ‡ÐµÐº", "Ñ‚Ð¾Ð¿ ÐºÐ°Ñ€Ñ‚Ð¾Ñ‡ÐµÐº"]:
            cards_top(message)
        elif message.text in ["/prem", "Ð¿Ñ€ÐµÐ¼Ð¸ÑƒÐ¼", "ÐŸÑ€ÐµÐ¼Ð¸ÑƒÐ¼"]:
            buy_premium(message)
    except Exception as e:
        bot.send_message(message.chat.id, "Ð’Ñ€ÐµÐ¼ÐµÐ½Ð½Ð°Ñ Ð¾ÑˆÐ¸Ð±ÐºÐ° Ð² Ð¾Ð±Ñ€Ð°Ð±Ð¾Ñ‚ÐºÐµ, Ð¿Ð¾Ð²Ñ‚Ð¾Ñ€Ð¸Ñ‚Ðµ Ð¿Ð¾Ð·Ð¶Ðµ.")
        bot.send_message(1130692453, f"ÐŸÑ€Ð¾Ð¸Ð·Ð¾ÑˆÐ»Ð° Ð¾ÑˆÐ¸Ð±ÐºÐ° Ð¿Ñ€Ð¸ Ð¾Ð±Ñ€Ð°Ð±Ð¾Ñ‚ÐºÐµ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ‹: Ð² Ñ‡Ð°Ñ‚Ðµ: {message.chat.id}. ÐžÑˆÐ¸Ð±ÐºÐ°: {e}")

try:
	bot.infinity_polling()
except Exception as e:
	print(f"ÐžÑˆÐ¸Ð±ÐºÐ° {e}")
