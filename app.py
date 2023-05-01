from flask import Flask, request
import telegram
from settle.credentials import bot_token, bot_user_name,URL
global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)
# start the flask app
app = Flask(__name__)

data = {}

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
	# retrieve the message in JSON and then transform it to Telegram object
	update = telegram.Update.de_json(request.get_json(force=True), bot)
	chat_id = update.message.chat.id
	
	# Telegram understands UTF-8, so encode text for unicode compatibility
	text = update.message.text.encode('utf-8').decode()
	# for debugging purposes only
	print("got text message :", text)
	# the first time you chat with the bot AKA the welcoming message
	if text == "/start":
		bot_reply = """Welcome! Type /register @your-username to get set up"""
		bot.sendMessage(chat_id=chat_id, text=bot_welcome)
	elif text[:8] == "/register":
		data[text[9:]] = chat_id
		bot_reply = """Ayy thanks! You have been registered."""
		print(text[9:])
		bot.sendMessage(chat_id=chat_id, text=bot_welcome)
	else:
	   bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name")
	return 'ok'
  
@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
	print('set web hook')
	# we use the bot object to link the bot to our app which live
	# in the link provided by URL
	s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
	# something to let us know things work
	if s:
		return "webhook setup ok"
	else:
		return "webhook setup failed"

@app.route('/api/<string:from_handle>/<string:to_handle>/<string:amount_to_settle>', methods=['GET', 'POST'])
def api(from_handle,to_handle,amount_to_settle):
	print(from_handle,to_handle,amount_to_settle)
	bot.sendMessage(chat_id=data[from_handle], text=from_handle+to_handle+amount_to_settle)
	return 'done'

@app.route('/')
def index():
	return '.'
if __name__ == '__main__':
	# note the threaded arg which allow
	# your app to have more than one thread
	app.run(threaded=True)