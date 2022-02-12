import telebot
import random
import sqlite3
import db
import config
import time
import func as f

bot = telebot.TeleBot(config.token)
db.create_tables()
conn = sqlite3.connect("bot.db", check_same_thread = False) # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
random = random.randint(0.0, 1)

def temp(message):
    try:
        cursor.execute('SELECT * FROM statistics')
        allo = cursor.fetchone()
        if allo is None:
            cursor.execute('INSERT INTO statistics VALUES (?, ?, ?, ?, ?)', (0, 0.0, 0, 0, 0.0))
            conn.commit()
        else:
            pass
    except:
        f.error(message)
@bot.message_handler(commands=["start"])
def start(message):
    try:
        chat_id = message.chat.id
        f.start(message)
    except:
        bot.send_message(chat_id, 'Что-то пошло не так. Попробуй написать команду /start ещё раз. Обычно подобной ошибки нет')
@bot.message_handler(commands=['admin'])
def admin(message):
    try:
        chat_id = message.chat.id
        z = f.check_user_ban(message)
        if z is None:
            chat_id = message.chat.id
            temp_list = config.admins_id
            kolvo_strok = int(temp_list[0])
            for i in range(kolvo_strok):
                if temp_list[0] == chat_id:
                    bot.send_sticker(chat_id, 'CAACAgIAAxkBAAK-uWAPyoMAAdcKEEdnVO0B-geNwQ-PKwACGwADT_uyHEqceSi_8-b8HgQ')
                    bot.send_message(chat_id, f'Добро пожаловать в админку @{message.from_user.username}', reply_markup=f.admin_key())
                    break
                else:
                    temp_list.pop(0)
        else:
            bot.send_sticker(chat_id, 'CAACAgIAAxkBAAK-GmAO8hTqhL2yxZXr7IliM0AadPEhAAJOAAOvxlEa8WHrsporn-QeBA')
            bot.send_message(chat_id, '⛔️Ты забанен⛔️')
    except:
        f.error(message)
@bot.message_handler(content_types=["text"])
def send_anytext(message):
    try:
        chat_id = message.chat.id
        z = f.check_user_ban(message)
        if z is None:
            if message.text == '👤Мой профиль':
                f.my_profile(message)
            if message.text == '🎲Игры':
                f.dice_game_menu(message)
            if message.text == "👨‍💻О боте":
                f.o_bote(message)
            else:
                pass
        else:
            bot.send_sticker(chat_id, 'CAACAgIAAxkBAAK-GmAO8hTqhL2yxZXr7IliM0AadPEhAAJOAAOvxlEa8WHrsporn-QeBA')
            bot.send_message(chat_id, '⛔️Ты забанен⛔️')
    except:
        f.error(message)
@bot.callback_query_handler(func=lambda message:True)
def tech_ob(message):
    try:
        chat_id = message.message.chat.id
        if 'ref_system' == message.data:
            f.ref(message)
        if 'list_ban' == message.data:
            f.list_ban(message)
        if 'help_dice_game' == message.data:
            f.help_dice_game(message, chat_id)
        if 'statistics_admin' == message.data:
            f.statistics_admin(message)
        if 'create_game_hash' == message.data:
            fgsd = bot.send_message(chat_id, 'Введите сумму ставки. Можно дробью и целым числом')
            # create_game_cheat
            cursor.execute('SELECT cheat FROM users WHERE user_id == ?', (chat_id, ))
            cheat_create = cursor.fetchone()
            if cheat_create[0] == 0:
                bot.register_next_step_handler(fgsd, f.create_game_hash)
            if cheat_create[0] == 1:
                bot.register_next_step_handler(fgsd, f.create_game_hash_cheat)
        if 'ban_user_username' == message.data:
            gfd = bot.send_message(chat_id, 'Введи username пользователя которого надо забанить')
            bot.register_next_step_handler(gfd, f.step2_ban_username)
        if 'unban_user_username' == message.data:
            gfq = bot.send_message(chat_id, 'Введи username пользователя которого надо разбанить')
            bot.register_next_step_handler(gfq, f.step2_unban_username)
        if 'play_game_hash' == message.data:
            asdddd = bot.send_message(chat_id, 'Введите хэш комнаты друга')
            cursor.execute('SELECT cheat FROM users WHERE user_id == ?', (chat_id, ))
            cheat_create = cursor.fetchone()
            if cheat_create[0] == 0:
                bot.register_next_step_handler(asdddd, f.play_dice_hash1)
            if cheat_create[0] == 1:
                bot.register_next_step_handler(asdddd, f.play_dice_hash1_cheat)
            bot.register_next_step_handler(asdddd, f.play_dice_hash1)
        if "get_dice_info" in message.data:
            cursor.execute('SELECT cheat FROM users WHERE user_id == ?', (chat_id, ))
            cheat_create = cursor.fetchone()
            if cheat_create[0] == 0:
                res = [int(i) for i in message.data.split() if i.isdigit()]
                f.play_dice(chat_id, message, res)
            if cheat_create[0] == 1:
                print(2)
                res = [int(i) for i in message.data.split() if i.isdigit()]
                f.play_dice_cheat(chat_id, message, res)
        if 'play_game' == message.data:
            bot.send_message(chat_id, "Выберите игру в которую хотите сыграть", reply_markup = f.create_kb_dices())
        if 'ban_user' == message.data:
            msg = bot.send_message(chat_id, 'Введи ID пользователя которого надо забанить')
            bot.register_next_step_handler(msg, f.step2_ban)
        if 'create_game' == message.data:
            qwe = bot.send_message(chat_id, 'Введите сумму ставки. Можно дробью и целым числом')
            # create_game_cheat
            cursor.execute('SELECT cheat FROM users WHERE user_id == ?', (chat_id, ))
            cheat_create = cursor.fetchone()
            if cheat_create[0] == 0:
                bot.register_next_step_handler(qwe, f.create_game)
            if cheat_create[0] == 1:
                bot.register_next_step_handler(qwe, f.create_game_cheat)
        if 'statistics' == message.data:
            f.statistics(message)
        if 'unban_user' == message.data:
            msg0 = bot.send_message(chat_id, 'Введи ID пользователя которого надо разбанить')
            bot.register_next_step_handler(msg0, f.step2_unban)
        if 'cheat_new_user' == message.data:
            msg01 = bot.send_message(chat_id, 'Введи ID пользователя которому надо дать читы')
            bot.register_next_step_handler(msg01, f.cheat_new_user)
        if 'cheat_delete_user' == message.data:
            msg777 = bot.send_message(chat_id, 'Введите ID пользователя которого надо убрать из списка читеров')
            bot.register_next_step_handler(msg777, f.cheat_delete_user)
        if 'spam_message' == message.data:
            msg707 = bot.send_message(chat_id, 'Введите сообщение которое надо разослать всем участникам бота')
            bot.register_next_step_handler(msg707, f.spam_message)
        if 'top_up_balans' == message.data:
            jfg = bot.send_message(chat_id, '''Для того чтобы пополнить баланс в боте
▫️Переведите деньги на рублёвый счёт на номер P1043209342 (P1043209342 относится к платёжной системе Payeer, что такое Payeer можете узнать в меню Мой профиль Что такое Payeer)
▫️Скопируйте номер операции
▫️Перейдите в бота и нажмите на 👤Мой профиль
▫️Далее нажмите на 📥Пополнение баланса
▫️Введите сюда скопированный номер операции и отправьте в бота
▫️Вуаля! Деньги теперь находятся на счёте бота
⚠️Никому не разглашайте номер операции, его говорить можно только администратору⚠️
⚠️Передача номера операции третьим лицам грозит потери денег⚠️''')
            bot.register_next_step_handler(jfg, f.top_up_balance)
        if 'print_payeer_id' == message.data:
            sdfd = bot.send_message(chat_id, 'Введите новый Payeer ID, на него будут выводится все деньги')
            bot.register_next_step_handler(sdfd, f.print_payeer_id)
        if 'withdraw_balans' == message.data:
            cursor.execute('SELECT bal FROM users WHERE user_id == ?', (chat_id, ))
            my_money = cursor.fetchone()
            
            bot.send_photo(chat_id, 'AgACAgIAAxkBAAMLYBWt55QgbtQsxmesHznEW1ahiEoAAs6xMRviwLFIRLjGkpNfwviLLiWbLgADAQADAgADeQADMgQCAAEeBA', caption = f'''▫️Сумма на вашем счёте {float(my_money[0])}
▫️Валюта RUB''')
            mgs01 = bot.send_message(chat_id, '💰Сколько денег вы хотите вывести?')
            bot.register_next_step_handler(mgs01, f.withdraw)
        if 'what_payeer' == message.data:
            bot.send_photo(chat_id, 'AgACAgIAAxkBAAM7YBYpR8Eq90hxUQrslQNpKxjHikgAAoWwMRvdi7lIo2vco38VxvSvJeqXLgADAQADAgADeQAD81sGAAEeBA', caption='''Ваш персональный
PAYEER® кошелек!
Отправить, обменять или принять фиат и
криптовалюты еще не было так просто!''')
            time.sleep(3)
            bot.send_photo(chat_id, 'AgACAgIAAxkBAANAYBYp1AfgH-6YeCuZlw5z8mYm4G8AAoawMRvdi7lIip5DmFZzsyIP3C-bLgADAQADAgADeQADi-QBAAEeBA', caption='''🇷🇺В вашей стране🇰🇿
                       
Электронные платежные системы, банковские карты, терминалы оплаты, международные переводы, сотовая связь и другие.
        
Вывод на популярные кошельки такие как 🥝QIWI, ЮMoney а также на банковские карты Visa, Mastercard, Maestro, Cirrus, МИР
Возможность хранить криптовалюту в неограниченном размере
        
Щедрая реферальная система до 11%!!!!
🔥 Скорей регистрируйся в лучшем кошельке в интернете!🔥 ''', reply_markup=f.what_payeer_key())
        else:
            pass
    except:
        f.error(message)
bot.polling(none_stop=True, interval=0, timeout = 60)