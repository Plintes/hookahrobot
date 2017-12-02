import telebot
import logging
import random
import flask
import time

###############################################################
API_TOKEN = "447246469:AAETslLMelxZhW-nbpOTLRJQY0m2D-1fCjA"
WEBHOOK_HOST = '89.223.29.238'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr
WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % API_TOKEN
# logger = telebot.logger
# telebot.logger.setLevel(logger.info)
bot = telebot.TeleBot(API_TOKEN)
app = flask.Flask(__name__)


# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
###############################################################

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)-3s]# %(levelname)-5s [%(asctime)s] %(message)s'
                    , level=logging.INFO)
bot = telebot.TeleBot("447246469:AAETslLMelxZhW-nbpOTLRJQY0m2D-1fCjA")


def niceprint(string):
    tabindex = 0
    out = ''
    for i in string:
        if i == ',':
            out += i
            out += '\n'
            out += '\t' * tabindex
            continue
        if i == '{':
            tabindex += 1
        if i == '}':
            tabindex -= 1
            out += '\n'
        out += i
    return out


a = []
keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row(telebot.types.InlineKeyboardButton('Войти в АНУС', callback_data='reg'))
keyboard.row(telebot.types.InlineKeyboardButton('Выдать ЕБУЧИЙ калик', callback_data='chooser'))


@bot.callback_query_handler(func=lambda call: call.data == 'reg')
def reg(call):
    # bot.send_message(call.message.chat.id, 'Жопа')
    if call.from_user.username in a:
        bot.answer_callback_query(call.id, text='ТЫ ЧО СУКА!')
    else:
        a.append(call.from_user.username)
        print(a)
        out = '''Кто же будет первым курить *калик*?
Зарегистрируйся потом жми "Выдать ЕБУЧИЙ калик".\n\nУчастники:'''
        for i in a:
            out += '\n' + '- ' + str(i)
        bot.edit_message_text(out, call.message.chat.id, call.message.message_id, reply_markup=keyboard
                              , parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data == 'chooser')
def chooser(call):
    global a
    if len(a) == 0:
        bot.answer_callback_query(call.id, 'ты МУДАК и никто с тобой не курит калик')
    if len(a) == 1:
        bot.answer_callback_query(call.id, 'Нужно больше пидоров')
    #         out = '''Кто же будет первым курить *калик*?
    # Зарегистрируйся потом жми "Выдать ЕБУЧИЙ калик".\n\n'''
    #         logging.info(a)
    #         for indx, i in enumerate(a):
    #             out += '\n' + str(indx + 1) + '. ' + str(i)
    #         out += '\n\nНужно больше участников'
    #         bot.edit_message_text(out, call.message.chat.id, call.message.message_id, reply_markup=keyboard
    #                               , parse_mode='Markdown')

    if len(a) > 1:
        logging.info(a)
        random.shuffle(a)
        logging.info(a)
        out = '''Кто же будет первым курить *калик*?
Зарегистрируйся потом жми "Выдать ЕБУЧИЙ калик".\n\nУчастники:'''
        for indx, i in enumerate(a):
            out += '\n' + str(indx + 1) + '. ' + str(i)

        out += '\n\nПервым курит калик: ' + '@' + a[0]
        a = []
        bot.edit_message_text(out, call.message.chat.id, call.message.message_id
                              , parse_mode='Markdown')


@bot.message_handler(commands=['hookah'])
def send_welcome(message):
    global a
    a = []
    mes = bot.send_message(message.chat.id, '''Кто же будет первым курить *калик*?
Зарегистрируйся потом жми "Выдать ЕБУЧИЙ калик".''', parse_mode='Markdown', reply_markup=keyboard)
    # if mes.chat.type == 'supergroup':
    #     bot.pin_chat_message(mes.chat.id, mes.message_id)


###############################################################
# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()
time.sleep(1)


# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))


# Start flask server
app.run(host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
        debug=True)

