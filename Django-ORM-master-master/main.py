import sys

sys.dont_write_bytecode = True
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
import django

django.setup()

from db.models import Register
from telegram import Update, ReplyMarkup, KeyboardButton, ReplyKeyboardMarkup, MessageEntity, InlineKeyboardButton, \
    InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, \
    ConversationHandler, MessageHandler, Filters, CallbackQueryHandler

Last_name_handler, First_name_handler, Phone_number_handler, Courses_handler, Time_handler, Get_all_handler = range(6)


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Botga xush kelibsiz.')
    update.message.reply_text('Ismingizni kiriting.')
    return First_name_handler


def first_name_handler(update: Update, context: CallbackContext):
    name = update.message.text
    if name == '/start' or type(name) == int or len(name) < 3:
        update.message.reply_html('<b>Ism xato kiritildi.\n'
                                  'Qaytadan urinib ko\'ring.</b>')
    else:
        context.chat_data.update({
            'first_name': update.message.text
        })
        update.message.reply_text('Familiyangizni kiriting.')
        return Last_name_handler


def first_name_resend_handler(update: Update, context: CallbackContext):
    update.message.reply_text('Xato kiritildi. Qaytadan urinib ko\'ring.')
    return Last_name_handler


def last_name_handler(update: Update, context: CallbackContext):
    last = update.message.text
    if last == '/start' or type(last) == int or len(last) < 5:
        update.message.reply_html('<b>Familiya xato kiritildi.\n'
                                  'Qaytadan urinib ko\'ring.</b>')
    else:
        context.chat_data.update({
            'last_name': update.message.text
        })
        update.message.reply_text('Telefon nomeringizni kiritish uchun pastdagi tugmani bosing.',
                                  reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Telefon raqam yuborish',
                                                                                    request_contact=True)]],
                                                                   resize_keyboard=True,
                                                                   one_time_keyboard=True))
        return Phone_number_handler


def last_name_resend_handler(update: Update, context: CallbackContext):
    update.message.reply_text('Xato nomer kiritildi. Ro\'g\'ri nomer kiriting yoki tugmani bosing.',
                              reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Telefon raqam yuborish',
                                                                                request_contact=True)]],
                                                               resize_keyboard=True,
                                                               one_time_keyboard=True))
    return Phone_number_handler


def phone_contact_handler(update: Update, context: CallbackContext):
    contact = update.message.contact
    context.chat_data.update({
        'phone_number': '+' + contact.phone_number
    })
    update.message.reply_text('Kursni tanlang.')
    update.message.reply_text('Bizda mavjud b\'lgan kurslar.',
                              reply_markup=ReplyKeyboardMarkup([
                                  [KeyboardButton('Web dasturlash')],
                                  [KeyboardButton('Mobil dasturlash')],
                                  [KeyboardButton('Robototexnika')],
                                  [KeyboardButton('Grafik dizayn')],
                                  [KeyboardButton('Moushn dizayn')],
                                  [KeyboardButton('SMM')],
                                  [KeyboardButton('3DsMax')],
                              ], resize_keyboard=True, one_time_keyboard=True
                              ))
    return Courses_handler


def courses_handler(update: Update, context: CallbackContext):
    c = update.message.text
    if c == 'Web dasturlash' or c == 'Mobil dasturlash' or c == 'Robototexnika' \
            or c == 'Grafik dizayn' or c == 'Moushn dizayn' or c == 'SMM' or c == '3DsMax':
        context.chat_data.update({
            'course': update.message.text
        })
        keyboard = [
            [
                InlineKeyboardButton(text='10:00-12:00', callback_data='10:00-12:00'),
                InlineKeyboardButton(text='12:00-14:00', callback_data='12:00-14:00'),
            ],
            [
                InlineKeyboardButton(text='14:00-16:00', callback_data='14:00-16:00'),
                InlineKeyboardButton(text='16:00-18:00', callback_data='16:00-18:00'),
            ]
        ]
        update.message.reply_text('Siz uchun qulay vaqtni tanlang.',
                                  reply_markup=InlineKeyboardMarkup(keyboard))
        return Time_handler
    else:
        update.message.reply_html('Bizda mavjud bo\'lmagan kurs tanladingiz.\n'
                                  '<b>Qaytadan urinib ko\'ring.</b>')


def courses_resend_handler(update: Update, context: CallbackContext):
    update.message.reply_html('Bizda mavjud bulmagan kursni tanladingiz.\n'
                              '<b>Qaytadan urinib ko\'ring.</b>',
                              reply_markup=ReplyKeyboardMarkup([
                                  [KeyboardButton('Web dasturlash')],
                                  [KeyboardButton('Mobil dasturlash')],
                                  [KeyboardButton('Robototexnika')],
                                  [KeyboardButton('Grafik dizayn')],
                                  [KeyboardButton('Moushn dizayn')],
                                  [KeyboardButton('SMM')],
                                  [KeyboardButton('3DsMax')],
                              ], resize_keyboard=True, one_time_keyboard=True
                              ))
    return Courses_handler


def time_handler(update: Update, context: CallbackContext):
    a = update.callback_query
    context.chat_data.update({
        'time': a.data
    })
    print(context.chat_data)
    _db = context.chat_data
    Register.objects.create(
        ism=_db['first_name'][0:255],
        familya=_db['last_name'][0:255],
        telefon_nomer=_db['phone_number'][0:255],
        kurs=_db['course'][0:255],
        vaqt=_db['time'][0:255],
    )
    a.edit_message_text('Ro\'yxatdan o\'tdingiz va tez orada admistratorlar siz bilan bog\'lanishadi.')


def help(update, context):
    db = Register.objects.all()
    for i in db:
        update.message.reply_html(f'Ism: <b>{i.ism}</b>\n'
                                  f'Familiya: <b>{i.familya}</b>\n'
                                  f'Telefon nomer: <b>{i.telefon_nomer}</b>\n'
                                  f'Kurs: <b>{i.kurs}</b>\n'
                                  f'Vaqt: <b>{i.vaqt}</b>\n'
                                  f'Ro\'yxatdan o\'tgan vaqti: <b>{i.registratsiya_vaqti}</b>')


updater = Updater('5267287419:AAEvQoum_UDHIS82Ur46Id5NKpkIwTd2Viw')
updater.dispatcher.add_handler(CommandHandler('malumotlar', help))
updater.dispatcher.add_handler(ConversationHandler(
    entry_points=[
        CommandHandler('start', start),
    ],
    states={
        First_name_handler: [
            MessageHandler(Filters.text, first_name_handler),
            MessageHandler(Filters.all, start)
        ],
        Last_name_handler: [
            MessageHandler(Filters.text, last_name_handler),
            MessageHandler(Filters.all, first_name_resend_handler)
        ],
        Phone_number_handler: [
            MessageHandler(Filters.contact, phone_contact_handler),
            MessageHandler(Filters.all, last_name_resend_handler),
        ],
        Courses_handler: [
            MessageHandler(Filters.text, courses_handler),
            MessageHandler(Filters.all, courses_resend_handler),
        ],
        Time_handler: [
            CallbackQueryHandler(time_handler),
            CallbackQueryHandler(time_handler),
        ]
    },
    fallbacks=[]
))

updater.start_polling()
updater.idle()
