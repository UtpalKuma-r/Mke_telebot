from hide import MKE_BOT_TOKEN
import telebot
import manage_mke as mke

bot = telebot.TeleBot(MKE_BOT_TOKEN)

user = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
	reply = "Welcome to Maa Kaushilya Enterprises\nI am assisting by providing the price of the items available in the shop.\nI can be inaccurate, pleace confirm it in the shop.\nFor available command send /help."
	bot.send_message(message.chat.id, reply)

@bot.message_handler(commands=['help'])
def send_help(message):
	reply = "Here is the list of commands:\n\
	/add_item - add item to inventory\nformate-->/add_item@<item name>@<item price>@<item category>\n\n\
	/item_info_byname - get item data by there name\nformate-->/item_info_byname@<item_name>\n\n\
	/item_info_bycategory - get item data by there category\nformate-->/item_info_byname@<item_category>\n\n\
	/modify_item_price - Change price of the item\nformate-->/modify_item_price@<item_name>@<item_price>\n\n\
	/modify_item_category - Change category of the item\nformate-->/modify_item_price@<item_name>@<item_category>\n\n"
	bot.send_message(message.chat.id, reply)

@bot.message_handler(commands=['add_item'])
def add_items(message):
	data = message.text.split('@')
	if len(data) != 4:
		reply = "I was not able to interprate that, please try again with followint formate:\n/add_item@<item name>@<item price>@<item category>\nReplace\n\"<item name>\" by name of the item\n\"<item price>\" by price of the item\n\"<item category>\" by the category of the item"
	
	else:
		item_name = data[1]
		item_price = data[2]
		item_category = data[3]
		print(item_name,item_price,item_category)
		try:
			item_price = float(item_price)
			transection = mke.add_item(item_name, item_price, item_category)
			if transection['code'] == 200:
				reply = f"Data added\n{item_name} : {item_price} : {item_category}"
			elif transection['code'] == 409:
				reply = f"Duplicate entry\n{item_name} already exists"
			else:
				reply = f"Some error occured. Send a screenshot of the chat with the error code {transection['code']} to some@email.come"

		except ValueError:
			reply = "I was not able to get the price, please try again with following formate:\n/add_item@<item name>@<item price>\nReplace\n\"<item name>\" by name of the item\n\"<item price>\" by price of the item\"<item category>\" by the category of the item\n"

		except Exception as e:
			reply = "Some error occured\nlogging is not working yet"+str(e)

	bot.reply_to(message, reply)

@bot.message_handler(commands=['item_info_byname'])
def item_info_byname(message):
	data = message.text.split('@')
	if len(data) != 2:
		reply = "I was not able to interprate that, please try again with following formate:\n/item_info_byname@<item_name>\nReplace\n<item_name> by name of the item"
	else:
		item_name = data[1]
		transection = mke.item_info_byname(item_name)
		if transection['code'] == 200:
			reply = ''
			for key in transection['data']:
				reply += f'\n{key}\n'.upper()
				for k in transection['data'][key]:
					reply += f"{k} : {transection['data'][key][k]}\n"
		
		elif transection.code == 204:
			reply = f"Item with name {item_name} was not found in database"

	bot.reply_to(message,reply)

@bot.message_handler(commands=['item_info_bycategory'])
def item_info_byname(message):
	data = message.text.split('@')
	if len(data) != 2:
		reply = "I was not able to interprate that, please try again with following formate:\n/item_info_byname@<item_category>\nReplace\n<item_name> by name of the item"
	else:
		item_category = data[1]
		transection = mke.item_info_bycategory(item_category)
		if transection['code'] == 200:
			reply = ''
			for key in transection['data']:
				reply += f'\n{key}\n'.upper()
				for k in transection['data'][key]:
					reply += f"{k} : {transection['data'][key][k]}\n"
		
		elif transection.code == 204:
			reply = f"Item with category {item_category} was not found in database"
			
	bot.reply_to(message,reply)

@bot.message_handler(commands=['modify_item_price'])
def modify_item_price(message):
	data = message.text.split('@')
	if len(data) != 3:
		reply = "I was not able to interprate that, please try again with following formate:\n/modify_item_price@<item_name>@<item_price>\nReplace\n<item_name> by name of the item\n<item_price> by new price of the item"
	
	else:
		item_name = data[1]
		new_price = data[2]

		try:
			new_price = float(new_price)
			transection = mke.modify_item_price(item_name,new_price)

			if transection['code'] == 200:
				reply = f"Price updated successfully\n{item_name} : {new_price}"
			elif transection['code'] == 204:
				reply = f"Item name not found in database"
			else:
				reply = f"Some error occured. Send a screenshot of the chat with the error code {transection['code']} to some@email.come"

		except ValueError:
			reply = "I was not able to get the price, please try again with following formate:\n/modify_item_price@<item_name>@<item_price>\nReplace\n<item_name> by name of the item\n<item_price> by new price of the item"
		except Exception as e:
			reply = "Some error occured\nlogging is not working yet"+str(e)

	bot.reply_to(message,reply)

@bot.message_handler(commands=['modify_item_category'])
def modify_item_price(message):
	data = message.text.split('@')
	if len(data) != 3:
		reply = "I was not able to interprate that, please try again with following formate:\n/modify_item_price@<item_name>@<item_category>\nReplace\n<item_name> by name of the item\n<item_category> by new category of the item"
	
	else:
		item_name = data[1]
		new_category = data[2]

		transection = mke.modify_item_category(item_name,new_category)

		if transection['code'] == 200:
			reply = f"Category updated successfully\n{item_name} : {new_category}"
		elif transection['code'] == 204:
			reply = f"Item name not found in database"
		else:
			reply = f"Some error occured. Send a screenshot of the chat with the error code {transection['code']} to some@email.come"

	bot.reply_to(message,reply)



bot.infinity_polling()