import telebot
import logging
import random

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
        bot.edit_message_text(out, call.message.chat.id, call.message.message_id, reply_markup=keyboard
                              , parse_mode='Markdown')


@bot.message_handler(commands=['hookah'])
def send_welcome(message):
    global a
    a = []
    mes = bot.send_message(message.chat.id, '''Кто же будет первым курить *калик*?
Зарегистрируйся потом жми "Выдать ЕБУЧИЙ калик".''', parse_mode='Markdown', reply_markup=keyboard)
    # if mes.chat.type == 'supergroup':
    #     bot.pin_chat_message(mes.chat.id, mes.message_id)


bot.polling()

