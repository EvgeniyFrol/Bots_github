import telebot
import config
import random


bot = telebot.TeleBot(config.BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    sticker = open('hello.tgs', 'rb')
    bot.send_sticker(message.chat.id, sticker)

    marcup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton('🎰 Проверь свою удачу!')
    item2 = telebot.types.KeyboardButton('😃 Как дела?')

    marcup.add(item1, item2)

    bot.send_message(message.chat.id, 'Добро пожаловать, {0.first_name}!\n'
                                      'Я - <b>{1.first_name}</b> бот который умеет немножечко! Давай протестим!'
                     .format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=marcup)


@bot.message_handler(content_types=['text'])
def echo(message):
    if message.chat.type == 'private':
        if message.text == '🎰 Проверь свою удачу!':
            user_num = random.randint(1, 10)
            my_num = random.randint(1, 10)
            bot.send_message(message.chat.id, f'У тебя выпало {str(user_num)}')
            bot.send_message(message.chat.id, f'У меня выпало {str(my_num)}')
            if user_num > my_num:
                bot.send_message(message.chat.id, 'Просто повезло!')
                sticker = open('fuck.tgs', 'rb')
                bot.send_sticker(message.chat.id, sticker)
            elif user_num == my_num:
                bot.send_message(message.chat.id, 'Невероятно! Вот это удача!')
                sticker = open('тщ_цфн.tgs', 'rb')
                bot.send_sticker(message.chat.id, sticker)
            else:
                bot.send_message(message.chat.id, 'Я победил! Не расстраивайся. Повезет в следующий раз')
                sticker = open('oueeeee.tgs', 'rb')
                bot.send_sticker(message.chat.id, sticker)
        elif message.text == '😃 Как дела?':
            marcup = telebot.types.InlineKeyboardMarkup(row_width=2)
            item1 = telebot.types.InlineKeyboardButton('Хорошо', callback_data='good')
            item2 = telebot.types.InlineKeyboardButton('Не очень', callback_data='bad')

            marcup.add(item1, item2)

            bot.send_message(message.chat.id, 'Потихонечку) Как сам?', reply_markup=marcup)
        else:
            bot.send_message(message.chat.id, 'Я не знаю, что ответить! Давай сменим тему)')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                sticker = open('cool.tgs', 'rb')
                bot.send_message(call.message.chat.id, 'Вот и славнененько!')
                bot.send_sticker(call.message.chat.id, sticker)
            elif call.data == 'bad':
                sticker = open('plumbus.tgs', 'rb')
                bot.send_message(call.message.chat.id, 'Не переживай! Вот тебе плюмбус на удачу)')
                bot.send_sticker(call.message.chat.id, sticker)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text='Тут был какой то вопрос, или тебе показалось?)))',
                reply_markup=None
            )

            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text='Ты просто душка!!!')

    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
