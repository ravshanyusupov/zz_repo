import sys

sys.dont_write_bytecode = True
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
import django

django.setup()

from db.models import Register
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, \
    InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, \
    ConversationHandler, MessageHandler, Filters, CallbackQueryHandler

Region_handler, First_name_handler, Phone_number_handler, Courses_handler, Time_handler, Response_handler, End_handler = range(7)


def start(update, context):
    update.message.reply_text(
        'Assalomu aleykum! Yoshlar ishlari Agentligi Buxoro viloyat boshqarmasi IT markazi botiga xush kelibsiz!\n'
        'Ro\'yxatdan o\'tish uchun \'/boshlash\' ni bosing.')


def boshlash(update, context):
    update.message.reply_text('Ism familiyangizni toʻliq kiriting!')
    return First_name_handler


def first_name_handler(update, context):
    name = update.message.text
    if name == '/start' or type(name) == int or len(name) <= 3:
        update.message.reply_html('<b>Ism xato kiritildi.\n'
                                  'Qaytadan urinib ko\'ring.</b>')
    else:
        context.chat_data.update({
            'first_name': update.message.text
        })
        update.message.reply_text('Telefon nomeringizni kiritish uchun pastdagi tugmani bosing.',
                                  reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Telefon raqam yuborish',
                                                                                    request_contact=True)]],
                                                                   resize_keyboard=True,
                                                                   one_time_keyboard=True))
        return Phone_number_handler


def first_name_resend_handler(update, context):
    update.message.reply_text('Telefon nomeringizni kiritish uchun pastdagi tugmani bosing.',
                              reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Telefon raqam yuborish',
                                                                                request_contact=True)]],
                                                               resize_keyboard=True,
                                                               one_time_keyboard=True))
    return Phone_number_handler


# def last_name_handler(update, context):
#     last = update.message.text
#     if last == '/start' or type(last) == int or len(last) < 5:
#         update.message.reply_html('<b>Familiya xato kiritildi.\n'
#                                   'Qaytadan urinib ko\'ring.</b>')
#     else:
#         context.chat_data.update({
#             'last_name': update.message.text
#         })
#
#         return Phone_number_handler


# def last_name_resend_handler(update, context):
#     update.message.reply_text('Xato nomer kiritildi. Ro\'g\'ri nomer kiriting yoki tugmani bosing.',
#                               reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Telefon raqam yuborish',
#                                                                                 request_contact=True)]],
#                                                                resize_keyboard=True,
#                                                                one_time_keyboard=True))
#     return Phone_number_handler


def phone_contact_handler(update, context):
    contact = update.message.contact
    context.chat_data.update({
        'phone_number': contact.phone_number
    })
    update.message.reply_text('Mavjud kurslarimizdan birini tanlang!',
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


def courses_handler(update, context):
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
        update.message.reply_text('Oʻzingizga qulay vaqtni tanlang!',
                                  reply_markup=InlineKeyboardMarkup(keyboard))
        return Time_handler
    else:
        update.message.reply_html('Bizda mavjud bo\'lmagan kurs tanladingiz.\n'
                                  '<b>Qaytadan urinib ko\'ring.</b>')


def courses_resend_handler(update, context):
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


def time_handler(update, context):
    a = update.callback_query
    context.chat_data.update({
        'time': a.data
    })
    a.message.delete()
    # print(context.chat_data)
    # _db = context.chat_data
    # Register.objects.create(
    #     ism=_db['first_name'][0:255],
    #     familya=_db['last_name'][0:255],
    #     telefon_nomer=_db['phone_number'][0:255],
    #     kurs=_db['course'][0:255],
    #     vaqt=_db['time'][0:255],
    # )
    a.message.reply_text(text='Siz qaysi tuman yoki shahardansiz?',
                              reply_markup=ReplyKeyboardMarkup([
                                  [KeyboardButton('Buxoro shahar'),
                                   KeyboardButton('Buxoro tuman')],
                                  [KeyboardButton('Olot'),
                                   KeyboardButton('Galaosiyo')],
                                  [KeyboardButton('Gʻijduvon'),
                                   KeyboardButton('Jondor')],
                                  [KeyboardButton('Kogon shahar'),
                                   KeyboardButton('Kogon tuman')],
                                  [KeyboardButton('Qorakoʻl'),
                                   KeyboardButton('Qorovulbozor')],
                                  [KeyboardButton('Yangibozor'),
                                   KeyboardButton('Romitan')],
                                  [KeyboardButton('Shofirkon'),
                                   KeyboardButton('Vobkent')],
                              ], resize_keyboard=True, one_time_keyboard=True
                              ))
    return Region_handler


def region_handler(update, context):
    region = update.message.text
    # if region == ''
    context.chat_data.update({
        'region': region
    })
    keyboard = [
            InlineKeyboardButton(text='Ha', callback_data='Ha'),
            InlineKeyboardButton(text='Yoq', callback_data='Yoq'),
        ],
    update.message.reply_text('Ushbu loyiha boʻyicha oʻtiladigan bepul darslar Buxoro shahridagi Yoshlar Ishlar Agentligi binosida boʻlib oʻtadi. Siz agentlik binosiga kelib, darslarga offlayn tarzda qatnasha olasizmi?',
                              reply_markup=InlineKeyboardMarkup(keyboard))
    return End_handler


def true_false_handler(update, context):
    response = update.callback_query
    context.chat_data.update({
        'javob': response.data
    })
    print(context.chat_data)
    # if update.callback_query.data == ''
    response.edit_message_text(text=
        'Tabriklaymiz, siz muvaffaqqiyatli roʻyhatdan oʻtdingiz. Tez orada administratorlarimiz siz bilan bog’lanishadi!')


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
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('malumotlar', help))
updater.dispatcher.add_handler(ConversationHandler(
    entry_points=[
        CommandHandler('boshlash', boshlash),
    ],
    states={
        First_name_handler: [
            MessageHandler(Filters.text, first_name_handler),
            MessageHandler(Filters.all, start)
        ],
        Phone_number_handler: [
            MessageHandler(Filters.contact, phone_contact_handler),
            MessageHandler(Filters.all, first_name_resend_handler),
        ],
        Courses_handler: [
            MessageHandler(Filters.text, courses_handler),
            MessageHandler(Filters.all, courses_resend_handler),
        ],
        Time_handler: [
            CallbackQueryHandler(time_handler),
            CallbackQueryHandler(time_handler),
        ],
        Region_handler: [
            MessageHandler(Filters.text, region_handler),
            MessageHandler(Filters.all, time_handler)
        ],
        Response_handler: [
            CallbackQueryHandler(true_false_handler),
            CallbackQueryHandler(true_false_handler),
        ],
        End_handler: [
            CallbackQueryHandler(true_false_handler),
            # MessageHandler(Filters.all, true_false_handler)
        ]
    },
    fallbacks=[]
))

updater.start_polling()
updater.idle()
