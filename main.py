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

сonfig_data = config_func()

bot = telebot.TeleBot(сonfig_data['token'])
crypto = AioCryptoPay(token='184441:AAVfvJNbxjFh4FyvqvlHjym8TzlX8gtmTxr', network=Networks.MAIN_NET)
telebot.apihelper.READ_TIMEOUT = 60

DATA_FILE = 'tea_data_2.json'
DATA_FILE_2 = 'users_cards.json'
DATA_FILE_3 = "promo.json"
tea_names = сonfig_data['tea_names']
birds = сonfig_data['birds']
products = сonfig_data['products']
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
	text = f'''Хеей 🕊 {first_name}! Я Birdy. Бот для развлечений, тут можешь пить чай или открывать карточки, все команды можно посмотреть по команде /help.'''
	bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help'])
def help_command(message):
	text = '''
Краткое описание команд:
/profile, "Профиль" - ваш профиль
/chai, "Чай" - выпить чай
/chai\_top, "Топ чая" - топ по чаю
/knock, "Получить карту" - наблюдение за птичками"
/cards\_top "Топ карточек" - топ карточек по поинтам и количеству
/krone, "Монета", "Крона" - получение монет
/shop, "Магазин" - магазин, с товарами за монеты
/goods, "Покупки" - ваши покупки

Полный список команд с описанием [тут](https://teletype.in/@hlb_folt/jNICgr9tP50).'''
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
		
		message_text = "Топ-10 пользователей по объему выпитого чая:\n\n"
		for i, (user_id, user_data) in enumerate(top_10, 1):
			nickname = user_data.get('nickname', 'Unknown')
			total_volume = user_data['total_volume']

			if user_id in premium_users:
				premium_icon = "💎"
			else:
				premium_icon = ""

			if i == 1:
				comment = " - Король"
			elif 2 <= i <= 3:
				comment = " - Герцог"
			elif 4 <= i <= 5:
				comment = " - Маркиз"
			elif 6 <= i <= 7:
				comment = " - Граф"
			elif 8 <= i <= 9:
				comment = " - Виконт"
			elif i == 10:
				comment = " - Барон"

			message_text += f"{i}. {premium_icon} {nickname}: {total_volume} мл. {comment}\n"

		bot.send_message(message.chat.id, message_text)
	except Exception as e:
		bot.send_message(message.chat.id, "Временная ошибка в обработке, повторите позже.")
		bot.send_message(1130692453, f"Произошла ошибка при обработке команды: /chai_top в чате: {message.chat.id}. {e}")


last_request_time = {}

def send_random_tea(message):
    user_id = str(message.from_user.id)
    user_nickname = message.from_user.first_name
    current_time = time.time()

    if user_id in last_request_time and (current_time - last_request_time[user_id]) < 0.3:
        bot.reply_to(message, "Пожалуйста, подождите немного перед следующим запросом.")
        return

    last_request_time[user_id] = current_time

    data = load_data()
    total_volume = data.get(user_id, {'total_volume': 0, 'last_drink_time': 0})

    if 'nickname' not in total_volume:
        total_volume['nickname'] = user_nickname

    time_since_last_drink = time.time() - total_volume['last_drink_time']
    time_left = max(0, 600 - time_since_last_drink)

    if time_since_last_drink < 600:
        remaining_minutes = int(time_left // 60)
        remaining_seconds = int(time_left % 60)
        bot.reply_to(message, f"Пожалуйста, подождите еще {remaining_minutes} минут {remaining_seconds} секунд перед следующей чашкой чая.")
        return

    random_tea = random.choice(tea_names)
    premium_users = load_premium_users()
    is_premium = user_id in premium_users and datetime.fromisoformat(premium_users[user_id]) > datetime.now()
    if is_premium:
        random_volume = random.randint(500, 2000)
    else:
        random_volume = random.randint(200, 2000)
    bot.reply_to(message, f"{total_volume['nickname']} Вы успешно выпили чай\n\nВыпито: {random_volume} мл.\nЧай: {random_tea}\n\nВсего выпито: {total_volume['total_volume'] + random_volume} мл.")

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
	if "Бинокль Carl Zeiss Jena 40x105." in inventory:
		default_wait = min(default_wait, 12060)
	if "Бинокль Fujinon 25x150 MT-SX" in inventory:
		default_wait = min(default_wait, 15300)
	if "Бинокль Celestron SkyMaster 25x100" in inventory:
		default_wait = min(default_wait, 18360)
	if "Бинокль Canon 18x50 IS All Weather" in inventory:
		default_wait = min(default_wait, 19440)

	if time_since_last_usage < default_wait:
		remaining_time = default_wait - time_since_last_usage
		remaining_hours = int(remaining_time // 3600)
		remaining_minutes = int((remaining_time % 3600) // 60)
		remaining_seconds = int(remaining_time % 60)
		bot.reply_to(message, f"Вам нужно передохнуть 😴 {remaining_hours} часов {remaining_minutes} минут {remaining_seconds} секунд перед следующем наблюдением за птичками!")
		return

	random_number = random.randint(1, 95)
	if 0 <= random_number <= 14 or ("Хлеб, Описание: повышение шансов на легендарную птичку на один раз." in inventory and 0 <= random_number <= 30):
		eligible_birds = [bird for bird in birds if bird["rarity"] == "Легендарная"]
	elif 15 <= random_number <= 29:
		eligible_birds = [bird for bird in birds if bird["rarity"] == "Мифическая"]
	elif 30 <= random_number <= 49:
		eligible_birds = [bird for bird in birds if bird["rarity"] == "Сверхредкая"]
	elif 50 <= random_number <= 95:
		eligible_birds = [bird for bird in birds if bird["rarity"] == "Редкая"]

	if eligible_birds:
		chosen_bird = random.choice(eligible_birds)
		photo_data = chosen_bird['photo']
		if chosen_bird['name'] in user_data['birds']:
			with open(photo_data, 'rb') as photo_file:
				bot.send_photo(message.chat.id, photo_file, caption=f"Вам попалась повторка {chosen_bird['name']}! Будут начислены только очки.\nРедкость: {chosen_bird['rarity']}\n+{chosen_bird['points']} очков.\nОбитание: {chosen_bird['place']}\n\nВсего поинтов: {user_data['points'] + int(chosen_bird['points'])}")
			user_data['points'] += int(chosen_bird['points'])
		else:
			with open(photo_data, 'rb') as photo_file:
				bot.send_photo(message.chat.id, photo_file, caption=f"Из ваших наблюдений вы открыли новую птицу: {chosen_bird['name']}\nРедкость: {chosen_bird['rarity']}\nОчки: {chosen_bird['points']}\nОбитание: {chosen_bird['place']}")
			user_data['birds'].append(chosen_bird['name'])
			user_data['points'] += int(chosen_bird['points'])
		user_data['last_usage'] = time.time()
		data[user_id] = user_data
		save_data_2(data)

		if "Хлеб, Описание: повышение шансов на легендарную птичку на один раз." in inventory:
			inventory.remove("Хлеб, Описание: повышение шансов на легендарную птичку на один раз.")
			data_coins[user_id]['purchases'] = inventory
		else:
			pass

		with open('user_coins.json', 'w') as file:
			json.dump(data_coins, file, indent=4)
			print("сохранено")


@bot.callback_query_handler(func=lambda call: call.data.startswith('show_cards'))
def show_knock_cards(call):
	user_id = str(call.from_user.id)
	user_nickname = call.from_user.first_name
	unique_number = int(call.data.split('_')[-1])
	if user_button.get(user_id) != unique_number:
			bot.answer_callback_query(call.id, "Не ваша кнопка.", show_alert=True)
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
			bot.send_message(call.from_user.id, f"У вас собрано {collected_cards} из {total_cards} возможных\nВыберите редкость:", reply_markup=keyboard)
			chat_type = call.message.chat.type
			if chat_type in ['group', 'supergroup']:
					bot.send_message(call.message.chat.id, f"{call.from_user.first_name}, карточки отправлены вам в личные сообщения!")
			else:
					pass
		except telebot.apihelper.ApiException as e:
				logging.error(f"Не удалось отправить сообщение: {str(e)}")
				bot.send_message(call.message.chat.id, "Напишите боту что-то в личные сообщения, чтобы отправить вам карточки!")
	else:
		bot.send_message(call.message.chat.id, "Вы пока что не наблюдали за птичками.")


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
			caption = f"{bird['name']}\nРедкость: {bird['rarity']}"
			if 'points' in bird:
				caption += f"\nОчки: {bird['points']}"
			caption += f"\nОбитание: {bird['place']}"
			with open(photo_data, 'rb') as photo_file:
				chat_type = call.message.chat.type
				bot.send_photo(call.message.chat.id, photo_file, caption=caption)
	else:
		bot.send_message(call.message.chat.id, f"У вас нет карточек редкости {rarity}")


def handle_stocoin(message):
    try:
        user_id = str(message.from_user.id)
        not_str_user_id = message.from_user.id
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
            bot.reply_to(message, f"Вы уже получили кроны. Попробуйте через {int(minutes)} минут {int(seconds)} секунд.")
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

        bot.reply_to(message, f"Вы успешно заработали {coins} золотых крон.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Временная ошибка в обработке, повторите позже!")
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
			bot.send_message(message.chat.id, "Ошибка: данные пользователей не найдены.")
			return

		user_data = data.get(user_id, {})
		coins = user_data.get("coins", 0)

		last_request_time = user_data.get("last_request_time", 0)
		remaining_time = max(0, 1500 - (current_time - last_request_time))
		minutes, seconds = divmod(remaining_time, 60)

		if remaining_time > 0:
			time_message = f" До следующего получения койнов осталось {int(minutes)} мин. {int(seconds)} сек."
		else:
			time_message = ""

		shop_message = f"Ваш текущий баланс: {coins} кроны." + time_message + "\nВыберите товар:"
		markup = types.InlineKeyboardMarkup(row_width=8)
		for product_id, product_info in products.items():
			button = types.InlineKeyboardButton(text=product_info["name"], callback_data=f"buy_{product_id}_{unique_number}")
			markup.add(button)
		bot.send_message(message.chat.id, shop_message, reply_markup=markup)
	except Exception as e:
		bot.send_message(message.chat.id, f"Произошла ошибка {e} (напишите @AleksFolt)")


@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def handle_buy_query(call):
	product_id, unique_number = call.data.split('_')[1:3]
	user_id = str(call.from_user.id)
	
	if user_button.get(user_id) != int(unique_number):
		bot.answer_callback_query(call.id, "Не ваша кнопка.", show_alert=True)
		return

	product = products[product_id]
	markup = types.InlineKeyboardMarkup()
	buy_button = types.InlineKeyboardButton(text="Купить", callback_data=f"confirm_{product_id}_{unique_number}")
	markup.add(buy_button)
	
	with open(product["image"], "rb") as photo:
		bot.send_photo(call.message.chat.id, photo, caption=f"{product['name']} - Цена: {product['price']} крон.", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('confirm_'))
def confirm_purchase(call):
	user_id = str(call.from_user.id)
	product_id = call.data.split('_')[1]
	unique_number = int(call.data.split('_')[2])
	product = products[product_id]
	if user_button.get(user_id) != unique_number:
		bot.answer_callback_query(call.id, "Не ваша кнопка.", show_alert=True)
		return

	with open("user_coins.json", 'r') as file:
		data = json.load(file)

	if data[user_id]["coins"] >= product["price"]:
		if product["name"] in data[user_id]["purchases"]:
			bot.answer_callback_query(call.id, f"Зачем тебе два таких? 🤨")
			return
		data[user_id]["coins"] -= product["price"]
		data[user_id]["purchases"].append(product["name"])
		with open("user_coins.json", 'w') as file:
			json.dump(data, file, indent=4)
		bot.answer_callback_query(call.id, f"Покупка успешна! Вы приобрели {product['name']}.")
	else:
		bot.answer_callback_query(call.id, "Недостаточно золотых крон для покупки. Зарабатывай больше!")


def handle_goods(message):
	try:
		user_id = str(message.from_user.id)
		with open("user_coins.json", 'r') as file:
			data = json.load(file)
		purchases = data.get(user_id, {}).get("purchases", [])
		response = "Ваши товары:\n" + "\n".join(purchases) if purchases else "Вы еще ничего не купили."
		bot.send_message(message.chat.id, response)
	except Exception as e:
		bot.send_message(message.chat.id, f"Произошла ошибка {e} (напишите @AleksFolt)")


def cards_top(message):
	try:
		inline_markup = InlineKeyboardMarkup()
		button_1 = InlineKeyboardButton(text="Топ по карточкам", callback_data="top_cards_cards")
		button_2 = InlineKeyboardButton(text="Топ по очкам", callback_data="top_cards_point")
		inline_markup.add(button_1, button_2)
		bot.send_message(message.chat.id, "Топ 10 пользователей по карточкам. Выберите кнопку:", reply_markup=inline_markup)
	except Exception as e:
		print(f"Error: {e}")
		bot.send_message(message.chat.id, "Временная ошибка в обработке, повтори позже.")


@bot.callback_query_handler(func=lambda call: call.data.startswith('top_cards_'))
def cards_top_callback(call):
    choice = call.data.split('_')[2]
    data = load_data_cards()
    user_id = str(call.message.from_user.id)
    user_data = data.get(user_id, {'points': 0, 'birds': []})
    if choice == "cards":
        sorted_data = sorted(data.items(), key=lambda x: len(x[1].get('birds', [])), reverse=True)
        top_10 = sorted_data[:10]

        message_text = "Топ-10 пользователей по количеству собранных карточек:\n\n"
        for i, (user_id, user_data) in enumerate(top_10, 1):
            nickname = user_data.get('nickname', 'Unknown')
            num_cards = len(user_data.get('birds', []))
            message_text += f"{i}. {nickname}: {num_cards} карточек\n"

        bot.send_message(call.message.chat.id, message_text)
    elif choice == "point":
        sorted_data_points = sorted(data.items(), key=lambda x: x[1].get('points', 0), reverse=True)
        top_10 = sorted_data_points[:10]

        message_text = "Топ-10 пользователей по количеству набранных очков:\n\n"
        for j, (user_id, user_data) in enumerate(top_10, 1):
            nickname_2 = user_data.get('nickname', 'Unknown')
            points = user_data.get('points', 0)
            message_text += f"{j}. {nickname_2}: {points} очков\n"

        bot.send_message(call.message.chat.id, message_text)


def handle_profile(message, background_image_path="background_image.jpg", premium_background_image_path="background2_image.jpg"):
    waiting = bot.send_message(message.chat.id, "Открываю профиль...")
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
        bot.send_message(message.chat.id, "Ошибка: данные пользователей не найдены.")
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
            premium_status = f"активен, закончится через {days} дней {hours} часов {minutes} минут"
            background_image_path = premium_background_image_path
            avatar_position = (337, 180)
            avatar_size = (293, 303)
        else:
            premium_status = "истек"
            avatar_position = (275, 144)
            avatar_size = (378, 398)
    else:
        premium_status = "не активен"
        avatar_position = (275, 144)
        avatar_size = (378, 398)
    
    caption = f"🏡 Личный профиль {first_name} {last_name}\n🃏 Собрано {collected_cards} карточек из {total_cards} возможных.\n🪙 Ваш баланс крон: {coins} крон.\n🏆 Баланс поинтов: {user_data['points']}\n💎 Премиум статус: {premium_status}"

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

    avatar_image = avatar_image.resize(avatar_size, Image.Resampling.LANCZOS)

    background_image.paste(avatar_image, avatar_position, avatar_image)

    final_image_stream = BytesIO()
    background_image.save(final_image_stream, format='PNG')
    final_image_stream.seek(0)
    final_image_stream.name = 'modified_image.jpg'

    unique_number = random.randint(1000, 99999999)
    user_button[str_user_id] = unique_number
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    button_1 = telebot.types.InlineKeyboardButton(text="Мои карточки", callback_data=f'show_cards_{unique_number}')
    button_2 = telebot.types.InlineKeyboardButton(text="Купить крутку", callback_data=f'crutka_cards_{unique_number}')
    button_3 = telebot.types.InlineKeyboardButton(text="Премиум", callback_data=f'birdy_prem_{unique_number}')
    keyboard.add(button_1, button_2, button_3)
    bot.delete_message(message.chat.id, waiting.message_id)
    bot.send_photo(message.chat.id, photo=final_image_stream, caption=caption, reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: call.data.startswith(f'birdy_prem'))
def crutki(call):
	unique_number = int(call.data.split('_')[-1])
	user_id = str(call.from_user.id)
	if user_button.get(user_id) != unique_number:
		bot.answer_callback_query(call.id, "Не ваша кнопка.", show_alert=True)
		return
	bot.send_message(call.message.chat.id, "💎 Birdy Premium\n\nПреимущества:\nКроны выдаются от 1 до 20 вместо 1 до 10.\nЧай выдается от 500 до 2000 вместо 200 до 2000.\nВ топе чая отображается алмаз.\nВ будущем будет добавлено больше всего.\n\nПокупка:\nКоманда: /prem.\nОплата USDT, @CryptoBot")


@bot.callback_query_handler(func=lambda call: call.data.startswith(f'crutka_cards'))
def crutki(call):
	unique_number = int(call.data.split('_')[-1])
	user_id = str(call.from_user.id)
	if user_button.get(user_id) != unique_number:
		bot.answer_callback_query(call.id, "Не ваша кнопка.", show_alert=True)
		return
	data = load_data_cards()
	user_nickname = call.from_user.first_name
	user_data = data.get(user_id, {'birds': [], 'last_usage': 0, 'points': 0, 'nickname': user_nickname})
	keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
	button_1 = telebot.types.InlineKeyboardButton(text="Купить", callback_data=f'buying_crutka_{unique_number}')
	keyboard.add(button_1)
	premium_users = load_premium_users()
	is_premium = user_id in premium_users and datetime.fromisoformat(premium_users[user_id]) > datetime.now()
	delay = 45000 if is_premium else 50000
	bot.send_message(call.message.chat.id, f"Купить крутку. Цена: {delay} поинтов:\nБаланс поинтов: {user_data['points']}", reply_markup=keyboard)
	

@bot.callback_query_handler(func=lambda call: call.data.startswith('buying_crutka'))
def buy_crutka(call):
    user_id = str(call.from_user.id)
    unique_number = int(call.data.split('_')[-1])
    if user_button.get(user_id) != unique_number:
        bot.answer_callback_query(call.id, "Не ваша кнопка.", show_alert=True)
        return
    
    data = load_data_cards()
    premium_users = load_premium_users()
    is_premium = user_id in premium_users and datetime.fromisoformat(premium_users[user_id]) > datetime.now()
    delay = 45000 if is_premium else 50000
    user_nickname = call.from_user.first_name
    user_data = data.get(user_id, {'birds': [], 'last_usage': 0, 'points': 0, 'nickname': user_nickname})
    
    if user_data['points'] >= delay:
        excluded_birds = ["Птичка зефирка", "Птичка тортик", "Птичка печенька", "Птичка Круассан", "Птица бог воды", "Птица бог огня", "Птица бог камня", "Птица бог грома", "Птица бог растений"]
        
        eligible_birds = [bird for bird in birds if bird["rarity"] == "Крутка" and bird["name"] not in excluded_birds]
        chosen_bird = None
        attempt_count = 0
        
        while attempt_count < 100:
            chosen_bird = random.choice(eligible_birds)
            if chosen_bird['name'] not in user_data['birds']:
                break
            attempt_count += 1
        
        if chosen_bird and chosen_bird['name'] not in user_data['birds']:
            user_data['birds'].append(chosen_bird['name'])
            user_data['points'] -= delay
            data[user_id] = user_data
            save_data_2(data)
            photo_data = chosen_bird['photo']
            with open(photo_data, 'rb') as photo_file:
                bot.send_photo(call.message.chat.id, photo_file, caption=f"{user_nickname} Вам выпала {chosen_bird['name']}!")
        else:
            bot.send_message(call.message.chat.id, f"{user_nickname} Вы уже собрали все крутки.")
    else:
        bot.send_message(call.message.chat.id, f"{user_nickname} Недостаточно очков для покупки!")



async def create_and_send_invoice(sender_id, is_group=False, message=None):
	try:
		invoice = await crypto.create_invoice(asset='USDT', amount=0.5)
		if not invoice:
			if is_group:
				bot.send_message(message.chat.id, "Ошибка при создании инвойса. Пожалуйста, напишите что-то боту в личку.")
			else:
				bot.send_message(sender_id, "Ошибка при создании инвойса. Попробуйте позже.")
			return None

		markup = types.InlineKeyboardMarkup()
		url_requisites = types.InlineKeyboardButton(text="Оплатить", url=invoice.bot_invoice_url)
		markup.add(url_requisites)
		if is_group:
			bot.send_message(message.chat.id, "Реквизиты для оплаты отправлены в личные сообщения.")
			bot.send_message(sender_id, f"Премиум активируется через 100 секунд в случае успешной оплаты. Если вы оплатите чек после истечения времени вы потеряете деньги! Реквизиты: {invoice.bot_invoice_url}", reply_markup=markup)
		else:
			bot.send_message(sender_id, f"Премиум активируется через 100 секунд в случае успешной оплаты. Если вы оплатите чек после истечения времени вы потеряете деньги! Реквизиты: {invoice.bot_invoice_url}", reply_markup=markup)
		return invoice 
	except Exception as e:
		if is_group:
			bot.send_message(message.chat.id, "Произошла ошибка при создании инвойса. Пожалуйста, напишите что-то боту в личку.")
		else:
			bot.send_message(sender_id, f"Ошибка при создании инвойса: {e}")
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
		bot.send_message(sender_id, "🌟 Спасибо за покупку Премиума! Наслаждайтесь эксклюзивными преимуществами.")
	else:
		bot.send_message(sender_id, "Оплата не прошла! Попробуйте еще раз.")

async def get_invoice_status(invoice):
	try:
		invoice = await crypto.get_invoices(invoice_ids=invoice.invoice_id)
		return invoice.status
	except Exception as e:
		print(f"Ошибка при получении данных инвойса: {e}")
		return None


def buy_premium(message):
	sender_id = message.from_user.id
	if message.chat.type == "private":
		invoice = run_async(create_and_send_invoice(sender_id, message=message))
		if invoice:
			t = threading.Timer(100, check_payment, args=(sender_id, invoice))
			t.start()
		else:
			bot.send_message(sender_id, "Не удалось создать инвойс.")
	else: 
		invoice = run_async(create_and_send_invoice(sender_id, is_group=True, message=message))
		if not invoice:
			bot.send_message(message.chat.id, "Произошла ошибка при создании инвойса. Пожалуйста, напишите что-то боту в личку.")


@bot.message_handler(commands=['admin_send_files'])
def handle_send_files(message):
    try:
        user_id = message.from_user.id
        if user_id != 1130692453:
            bot.send_message(message.chat.id, "У вас нет прав на выполнение этой команды!")
            return
        filenames = message.text.split()[1:]
        if len(filenames) == 0:
            bot.reply_to(message, "Пожалуйста, укажите имена файлов для отправки.")
            return
        send_files(message.chat.id, filenames)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")
        print(f"Ошибка: {e}")

def send_files(chat_id, filenames):
    try:
        for filename in filenames:
            with open(filename, 'rb') as file:
                bot.send_document(chat_id, file)
    except Exception as e:
        bot.send_message(chat_id, f"Не удалось отправить файл {filename}: {e}")
        print(f"Не удалось отправить файл {filename}: {e}")


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    try:
        if message.text in ["/chai", "чай", "Чай"]:
            send_random_tea(message)
        elif message.text in ["/chai_top", "чай топ", "Чай топ", "Топ чая", "топ чая"]:
            chai_top(message)
        elif message.text in ["/knock", "кнок", "Кнок", "получить карту", "Получить карту"]:
            knock_cards_function(message)
        elif message.text in ["/krone", "крона", "Крона", "монета", "Монета"]:
            handle_stocoin(message)
        elif message.text in ["/shop", "магазин", "Магазин", "шоп", "Шоп"]:
            handle_shop(message)
        elif message.text in ["/goods", "Покупки", "покупки"]:
            handle_goods(message)
        elif message.text in ["/profile", "Профиль", "профиль"]:
            handle_profile(message)
        elif message.text in ["/cards_top", "Топ карточек", "топ карточек"]:
            cards_top(message)
        elif message.text in ["/prem", "премиум", "Премиум"]:
            buy_premium(message)
    except Exception as e:
        bot.send_message(message.chat.id, "Временная ошибка в обработке, повторите позже.")
        bot.send_message(1130692453, f"Произошла ошибка при обработке команды: в чате: {message.chat.id}. Ошибка: {e}")

try:
	bot.infinity_polling()
except Exception as e:
	print(f"Ошибка {e}")
