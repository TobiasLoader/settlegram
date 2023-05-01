from flask import Flask, request
import telegram
from settle.credentials import bot_token, bot_user_name, URL
global bot
import asyncio
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)
# start the flask app
app = Flask(__name__)

data = {}

@app.route('/', methods=['POST'])
def respond():
	# retrieve the message in JSON and then transform it to Telegram object
	update = telegram.Update.de_json(request.get_json(force=True), bot)
	if update.message is not None:
		chat_id = update.message.chat.id
		print("chat_id :", chat_id)

		# Telegram understands UTF-8, so encode text for unicode compatibility
		text = update.message.text.encode('utf-8').decode()
		# for debugging purposes only
		print("got text message :", text)
		# the first time you chat with the bot AKA the welcoming message
		if text == "/start":
			print('start')
			bot_reply = "Welcome! Type /register @your-username to get set up"
			print(chat_id,bot_reply)
			bot.sendMessage(chat_id=chat_id, text=bot_reply)
		elif text[:8] == "/register":
			print('reg')
			data[text[9:]] = chat_id
			bot_reply = "Ayy thanks! You have been registered."
			print(text[9:])
			print(chat_id,bot_reply)
			bot.sendMessage(chat_id=chat_id, text=bot_reply)
		else:
			print('else')
			bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name")
		return 'ok'
	else:
		print("no message sent in req")
		return 'no msg'
  
@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
	print('set web hook')
	# we use the bot object to link the bot to our app which live
	# in the link provided by URL
	s = asyncio.run(bot.setWebhook('{URL}'.format(URL=URL)))
	# something to let us know things work
	if s:
		return "webhook setup ok"
	else:
		return "webhook setup failed"

@app.route('/api/<string:from_handle>/<string:to_handle>/<string:amount_to_settle>', methods=['GET', 'POST'])
def api(from_handle,to_handle,amount_to_settle):
	# print(from_handle,to_handle,amount_to_settle)
	bot.sendMessage(chat_id=data[from_handle], text=from_handle+to_handle+amount_to_settle)
	return 'done'
# 
# @app.route('/')
# def index():
# 	return '.'

if __name__ == '__main__':
	# note the threaded arg which allow
	# your app to have more than one thread
	app.run(threaded=True)