import telebot
import random
import sqlite3
import config as conf
import time
from telebot import types
from payeer_api import PayeerAPI

p = PayeerAPI(conf.account, conf.api_id, conf.api_pass)

conn = sqlite3.connect("bot.db", check_same_thread = False) # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
bot = telebot.TeleBot(conf.token)

def error(message):
    try:
        chat_id = message.chat.id
        bot.send_message(chat_id, 'Что-то пошло не так. Попробуй написать /start')
    except:
        chat_id = message.message.chat.id
        bot.send_message(chat_id, 'Что-то пошло не так. Попробуй написать /start')
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
        error(message)
def ref(message):
    try:
        chat_id = message.message.chat.id
        cursor.execute('SELECT ref_sum FROM users WHERE user_id == ?', (chat_id, ))
        bot.send_message(chat_id, f'👥Реферальная система:\n\nПолучай 3% от выигрыша пользователя, которого ты привёл в этого бота.\n\nВаша реферальная ссылка: https://t.me/{conf.bot_name}?start={chat_id}\n\nДенег заработано с рефералов: {cursor.fetchone()[0]}')
    except:
        error(message)
def check_user_ban(message):
    try:
        chat_id = message.chat.id
        for i in range(1, 4):
            if i == 3:
                error(message)
                break
            try:
                cursor.execute('SELECT user_id FROM ban WHERE user_id == ?', (chat_id, ))
                return cursor.fetchone()
                break
            except:
                time.sleep(random) 
    except:
        error(message)
def keyboard_main():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = 2)
    markup.row("🎲Игры", "👤Мой профиль")
    markup.row("👨‍💻О боте")
    return markup
def admin_key():
    markup = types.InlineKeyboardMarkup(row_width = 2)
    markup.add(
        types.InlineKeyboardButton(text = "⛔️Забанить пользователя", callback_data = 'ban_user'),
        types.InlineKeyboardButton(text = '📛Разбанить пользователя', callback_data='unban_user'),
        types.InlineKeyboardButton(text = "🎲Добавить пользователя в список читеров", callback_data = "cheat_new_user"),
        types.InlineKeyboardButton(text = "🎲Убрать пользователя из списка читеров", callback_data = "cheat_delete_user"),
        types.InlineKeyboardButton(text = "⛔️Забанить пользователя по username", callback_data = 'ban_user_username'),
        types.InlineKeyboardButton(text = '📛Разбанить пользователя по username', callback_data='unban_user_username'),
        types.InlineKeyboardButton(text = "📨Рассылка сообщений", callback_data = "spam_message"),
        types.InlineKeyboardButton(text = "📊Статистика", callback_data = 'statistics_admin'),
        types.InlineKeyboardButton(text='📝Список забаненых', callback_data='list_ban')
        )
    return markup
def o_bote_key():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text = "📊Статистика", callback_data = 'statistics'),
        )
    return markup
def game_menu_key():
    markup= types.InlineKeyboardMarkup(row_width = 2)
    markup.add(
        types.InlineKeyboardButton(text='⚔️Создать игру', callback_data='create_game'),
        types.InlineKeyboardButton(text='⚔️Создать игру для друга', callback_data='create_game_hash'),
        types.InlineKeyboardButton(text='🎲Сыграть в игры', callback_data='play_game'),
        types.InlineKeyboardButton(text='🎲Сыграть с другом', callback_data='play_game_hash'),
        types.InlineKeyboardButton(text='🐼Помощь', callback_data='help_dice_game'),
        )
    return markup
def my_profile_key():
    keyboard_profile = types.InlineKeyboardMarkup(row_width=2)
    keyboard_profile.add(
    types.InlineKeyboardButton(text='📥Пополнение баланса', callback_data='top_up_balans'),
    types.InlineKeyboardButton(text='📤Вывод средств', callback_data='withdraw_balans'),
    types.InlineKeyboardButton(text='🎫Указать Payeer ID', callback_data='print_payeer_id'),
    types.InlineKeyboardButton(text='👥Реферальная система', callback_data='ref_system'),
    types.InlineKeyboardButton(text='🧐Что такое Payeer', callback_data='what_payeer'),
    )
    return keyboard_profile
def create_kb_dices():
    dices = get_all_dice()
    markup = types.InlineKeyboardMarkup(row_width = 1)
    for i in dices:
        markup.add(
            types.InlineKeyboardButton(text = f"🎲 {i[1]} RUB", callback_data = f"get_dice_info user_data {i[0]}")
            )
    return markup
def what_payeer_key():
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="🔗Ссылка для регистрации в Payeer", url="https://bit.ly/39KBnky")
    keyboard.add(url_button)
    return keyboard
def dice_game_menu(message):
    chat_id = message.chat.id
    bot.send_photo(chat_id, 'AgACAgIAAxkBAAIDjmAYLUn6IXKLjDhe-WPw0uHP_LPgAAKOsTEbrLrASOM1CrAprvyCdrd3ly4AAwEAAwIAA3gAA0-GBgABHgQ', caption = 'Создайте новую игру или выберите из имеющихся', reply_markup=game_menu_key())
def start(message):
    try:
        chat_id = message.chat.id
        z = check_user_ban(message)
        if z is None:
            temp(message)
                                        
            cursor.execute('SELECT user_id FROM users WHERE user_id == ?', (chat_id, ))
            user = cursor.fetchone()
            
            if user is None:
                refer_id = str(message.text)[7:]
                try:
                    refer_id = int(refer_id)
                except:
                    refer_id = 0
                cursor.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)', (chat_id, message.from_user.username,  0.0, refer_id, 0.0, 0, 'Не указан ID'))
                conn.commit()
                bot.send_message(chat_id, f'Добро пожаловать, @{message.from_user.username}', reply_markup=keyboard_main())
            else:
                z = check_user_ban(message)
                if z is None:
                    bot.send_message(chat_id, f'Добро пожаловать, @{message.from_user.username}', reply_markup=keyboard_main())
                else:
                    bot.send_sticker(chat_id, 'CAACAgIAAxkBAAK-GmAO8hTqhL2yxZXr7IliM0AadPEhAAJOAAOvxlEa8WHrsporn-QeBA')
                    bot.send_message(chat_id, '⛔️Ты забанен⛔️')
        else:
            bot.send_sticker(chat_id, 'CAACAgIAAxkBAAK-GmAO8hTqhL2yxZXr7IliM0AadPEhAAJOAAOvxlEa8WHrsporn-QeBA')
            bot.send_message(chat_id, '⛔️Ты забанен⛔️')
    except:
        bot.send_message(chat_id, 'Что-то пошло не так. Попробуй написать команду /start ещё раз. Обычно подобной ошибки нет')
def zadolbalo(message):
    try:
        global isRunning
        isRunning = 0
        if not isRunning:
            chat_id = message.chat.id
            msg = bot.send_message(chat_id, 'Введите ID пользователя')
            bot.register_next_step_handler(msg, askAge) #askSource
            isRunning = True
    except:
        error(message)
def askAge(message):
    try:
        chat_id = message.chat.id
        text = message.text
        if not text.isdigit():
            msg = bot.send_message(chat_id, 'ID должно быль числом, попробуйте ещё раз')
            bot.register_next_step_handler(msg, askAge) #askSource
            return
        msg = bot.send_message(chat_id, 'ID для бана: ' + text)
    except:
        error(message)
def list_ban(message):
    try:
        chat_id = message.message.chat.id
    
        cursor.execute('SELECT user_id FROM ban')
        all_ban = cursor.fetchall()
        
        cursor.execute('SELECT count(*) FROM ban')
        kolvo_strok_tuple = cursor.fetchone()
        kolvo_strok = int(kolvo_strok_tuple[0])
        mes = 'Вот кто забанен: \n'
        for i in range(kolvo_strok):
            cursor.execute('SELECT username FROM users WHERE user_id == ?', (all_ban[0]))
            mes+=f'Пользователь: {cursor.fetchone()[0]}. Его ID: {all_ban[0][0]}'
            all_ban.pop(0)
        bot.send_message(chat_id, mes)
    except:
        error(message)
def step2_ban(message):
    try:
        chat_id = message.chat.id
        text = message.text
        if not text.isdigit():
            msg = bot.send_message(chat_id, 'ID должен быть числом. Попробуй ввести ещё раз')
            bot.register_next_step_handler(msg, step2_ban)
            return
        cursor.execute('SELECT user_id FROM users WHERE user_id == ?', (int(text), ))
        if cursor.fetchone() is None:
            bot.send_message(chat_id, '''ID не был найден в базе данных''')
        else:
            cursor.execute('INSERT INTO ban VALUES(?, ?)', (int(text), 0))
            conn.commit()
            bot.send_message(chat_id, f'ID {text} был забанен')
    except:
        error(message)
def step2_unban(message):
    try:
        chat_id = message.chat.id
        text = message.text
        if not text.isdigit():
            msg = bot.send_message(chat_id, 'ID должно быть числом. Попробуй ещё раз')
            bot.register_next_step_handler(msg, step2_unban)
            return
        cursor.execute('SELECT user_id FROM users WHERE user_id == ?', (int(text), ))
        if cursor.fetchone() is None:
            bot.send_message(chat_id, 'ID не был найден в базе данных')
        else:
            cursor.execute('SELECT user_id FROM ban WHERE user_id = ?', (int(text), ))
            if cursor.fetchone() is None:
                bot.send_message(chat_id, f'Пользователь {text} не забанен')
            else:
                cursor.execute('DELETE FROM ban WHERE user_id == ?', (int(text), ))
                conn.commit()
                bot.send_message(chat_id, f'ID {text} был разбанен')
    except:
        error(message)
def step2_ban_username(message):
    try:
        chat_id = message.chat.id
        text = message.text
        cursor.execute('SELECT username FROM users WHERE username == ?', (text, ))
        if cursor.fetchone() is None:
            bot.send_message(chat_id, '''Username не был найден в базе данных''')
        else:
            cursor.execute('SELECT user_id FROM users WHERE username == ?', (text, ))
            username_check = cursor.fetchone()
            cursor.execute('INSERT INTO ban VALUES(?, ?)', (username_check[0], 0))
            conn.commit()
            bot.send_message(chat_id, f'Юзер {text} был забанен')
    except:
        error(message)
def step2_unban_username(message):
    try:
        chat_id = message.chat.id
        text = message.text
        cursor.execute('SELECT username FROM users WHERE username == ?', (text, ))
        if cursor.fetchone() is None:
            bot.send_message(chat_id, 'Username не был найден в базе данных')
        else:
            cursor.execute('SELECT user_id FROM users WHERE username == ?', (text, ))
            username_check = cursor.fetchone()
            cursor.execute('SELECT user_id FROM ban WHERE user_id = ?', (username_check[0], ))
            if cursor.fetchone() is None:
                bot.send_message(chat_id, f'Пользователь {text} не забанен')
            else:
                cursor.execute('DELETE FROM ban WHERE user_id == ?', (username_check[0], ))
                conn.commit()
                bot.send_message(chat_id, f'Юзер {text} был разбанен')
    except:
        error(message)
def cheat_new_user(message):
    try:
        chat_id = message.chat.id
        text = message.text
        if not text.isdigit():
            msg = bot.send_message(chat_id, 'ID должно быть числом. Попробуй ещё раз')
            bot.register_next_step_handler(msg, cheat_new_user)
            return
        else:
            cursor.execute('SELECT user_id FROM users WHERE user_id == ?', (int(text), ))
            if cursor.fetchone() is None:
                bot.send_message(chat_id, 'ID не был найден в базе данных')
            else:
                cursor.execute('SELECT cheat FROM users WHERE user_id = ?', (int(text), ))
                if cursor.fetchone() == (0,):
                    cursor.execute('UPDATE users SET cheat = 1 WHERE user_id == ?', (int(text), ))
                    conn.commit()
                    bot.send_message(chat_id, f'ID {text} был добавлен в список читеров')
                else:
                    bot.send_message(chat_id, 'Этот пользователь уже в списке читеров. Зачем его ещё раз добавлять?')
    except:
        error(message)
def cheat_delete_user(message):
    try:
        chat_id = message.chat.id
        text = message.text
        if not text.isdigit():
            msg = bot.send_message(chat_id, 'ID должно быть числом. Попробуй ещё раз')
            bot.register_next_step_handler(msg, cheat_delete_user)
            return
        else:
            cursor.execute('SELECT user_id FROM users WHERE user_id == ?', (int(text), ))
            if cursor.fetchone() is None:
                bot.send_message(chat_id, 'ID не был найден в базе данных')
            else:
                cursor.execute('SELECT cheat FROM users WHERE user_id == ?', (int(text), ))
                if cursor.fetchone() == (0,):
                    bot.send_message(chat_id, 'Этот пользователь не читер. Зачем его убирать?')
                else:
                    cursor.execute('UPDATE users SET cheat = 0 WHERE user_id = ?', (int(text), ))
                    conn.commit()
                    bot.send_message(chat_id, f'Пользователь {text} убран из списка читеров')
    except:
        error(message)
def get_all_users_inform(message):
    try:
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    except:
        error(message)
def spam_message(message):
        chat_id = message.chat.id
        text = message.text
        
        cursor.execute('SELECT count(*) FROM users')
        kolvo_strok_tuple = cursor.fetchone()
        kolvo_strok = int(kolvo_strok_tuple[0])
        
        cursor.execute('SELECT user_id FROM users')
        vse_user = cursor.fetchall()
        vse_user_list = list(vse_user)
        if message.text != None:
            user = 0
            for i in vse_user_list:
                try:                    
                    bot.send_message(i[0], f'{text}')
                    user += 1
                except telebot.apihelper.ApiException:
                    print(i[0])
            # for i in range(kolvo_strok):
            #     try:
            #         bot.send_message(vse_user[0][0], f'{text}')
            #         vse_user.pop(0)
            #         user += 1
            #     except:
            #         print(vse_user[0][0])
            bot.send_message(chat_id, f'✅Рассылка успешно завершена. Сообщение отправлено {user}')
        if message.photo != None:
            user = 0
            file_id = message.photo[len(message.photo)-1].file_id
            user = 0
            for i in vse_user_list:
                try:                    
                    bot.send_photo(i[0], f'{file_id}')
                    user += 1
                except telebot.apihelper.ApiException:
                    print(i[0])
            bot.send_message(chat_id, f'✅Рассылка успешно завершена. Сообщение отправлено {user}')
def my_profile(message):
    try:
        chat_id = message.chat.id
        cursor.execute('SELECT bal, payeer_id, ref_id FROM users WHERE user_id == ?', (chat_id, ))
        users = cursor.fetchone()
        if users[2] != 0:
            bot.send_photo(chat_id, 'AgACAgIAAxkBAAMQYBWuUvVQ0lb9YzqA4Rtjseeqw_UAAjayMRu5gbFIT0IWVt-la4wLUVWZLgADAQADAgADeQADRCMEAAEeBA', caption = f'''👤 Профиль
        
▫️Ваш ID: {chat_id}
▫Ваш реферал: {users[2]}
▫️Ваш Payeer ID: {users[1]}
        
Баланс: {float(users[0])} RUB 🔥''', reply_markup=my_profile_key())
        else:
            bot.send_photo(chat_id, 'AgACAgIAAxkBAAMQYBWuUvVQ0lb9YzqA4Rtjseeqw_UAAjayMRu5gbFIT0IWVt-la4wLUVWZLgADAQADAgADeQADRCMEAAEeBA', caption = f'''👤 Профиль
        
▫️Ваш ID: {chat_id}
▫Ваш реферал: Отсутвует
▫️Ваш Payeer ID: {users[1]}
        
Баланс: {float(users[0])} RUB 🔥''', reply_markup=my_profile_key())
    except:
        error(message)
def print_payeer_id(message):
    try:
        text = message.text
        chat_id = message.chat.id
        
        check = p.check_user(text)
        if check == True:
            cursor.execute('UPDATE users SET payeer_id = ? WHERE user_id == ?', (text, chat_id, ))
            conn.commit()
            bot.send_message(chat_id, f'✅Ваш Payeer ID был успешно изменён на {text}')
        if check == False:
            bot.send_message(chat_id, 'Возможно вы неправильно указали ID, проверьте на ошибки в вводе и напишите ёще раз')
    except:
        error(message)
def withdraw(message):
    try:
        chat_id = message.chat.id
        text = message.text
        try:
            text = float(text)
            cursor.execute('SELECT bal FROM users WHERE user_id == ?', (chat_id, ))
            my_money = cursor.fetchone()
            my_money = my_money[0]
            if text > my_money:
                bot.send_message(chat_id, 'Сумма для вывода больше чем на балансе. Вывод не возможен, уменьшите сумму вывода')
            if text < 1:
                bot.send_message(chat_id, 'Сумма вывода должна быть больше 1 RUB')
            else:       
                cursor.execute('SELECT payeer_id FROM users WHERE user_id == ?', (chat_id, ))
                payeer_id = cursor.fetchone()
        
                if payeer_id[0] == 'Не указан ID':
                    bot.send_message(chat_id, 'Пожалуйста добавьте кошелёк Payeer в бота. Для этого зайдите в меню Профиль и нажмите на Указать Payeer ID')
                if payeer_id[0] != 'Не указан ID':
                    perevod = p.transfer(text, payeer_id[0], cur_in='RUB', cur_out='RUB', comment='Выплата от бота @kosti_money_bot')
                    if perevod == True:
                        bot.send_message(chat_id, '✅Перевод успешно прошел')
                        cursor.execute('INSERT INTO withdraw VALUES (?, ?, ?, ?)', (chat_id, text, payeer_id[0], 'Successful', ))      
                        conn.commit()
                        minus_bablo = my_money - text
                        cursor.execute('UPDATE users SET bal = ? WHERE user_id = ?', (minus_bablo, chat_id, ))
                        conn.commit()
                    if perevod == False:
                        bot.send_message(chat_id, '❌Перевод не прошел успешно')
                        cursor.execute('INSERT INTO withdraw VALUES (?, ?, ?, ?)', (chat_id, text, payeer_id[0], 'Error', ))
                        conn.commit()
        except:
            bot.send_message(chat_id, 'Сумма должна быть числом')
    except:
        error(message)   
def top_up_balance(message):
    try:
        chat_id = message.chat.id
        text = message.text
        if not text.isdigit():
            msg = bot.send_message(chat_id, 'Номер операции должен быть числом. Введите правильно номер операции')
            bot.register_next_step_handler(msg, top_up_balance)
            return
        cursor.execute('SELECT id_operation FROM top_up_balans WHERE id_operation == ?', (int(text), ))
        id_operation = cursor.fetchone()
        if id_operation is None:
            history = p.history(id = int(text))
            if history == []:
                bot.send_sticker(chat_id, 'CAACAgIAAxkBAALFXmAYFQtIR739dRKUme6IZQim7mazAALhAQADOKAKb5eoZebua24eBA')
                bot.send_message(chat_id, 'Бот не нашёл записи о переводе по вашему номеру операции. Проверьте в точности ли вы написали номер операции')
            else:
                history_rub_dict = history.get(f'{int(text)}')
                history_rub = history_rub_dict.get('creditedAmount')
                
                cursor.execute('SELECT bal FROM users WHERE user_id == ?', (chat_id, ))
                my_money = cursor.fetchone()
                my_money = my_money[0]
                
                top_up = float(my_money) + float(history_rub)
                
                cursor.execute('INSERT INTO top_up_balans VALUES (?)', (int(text), ))
                conn.commit()
                
                cursor.execute('UPDATE users SET bal = ? WHERE user_id = ?', (top_up, chat_id, ))
                conn.commit()
                bot.send_message(chat_id, f'Ваш баланс был пополнен на {history_rub}')
        else:
            bot.send_message(chat_id, 'Этот номер операции уже использован')
    except:
        error(message)
def statistics(message):
    try:
        chat_id = message.message.chat.id
        
        cursor.execute('SELECT * FROM statistics')
        allo = cursor.fetchone()
        print(allo)
        
        cursor.execute('SELECT count(*) FROM users')
        kolvo_strok_tuple = cursor.fetchone()
        bot.send_message(chat_id, f'''📊Статистика
▫️Всего пользователей бота: {kolvo_strok_tuple[0]}
▫️Всего игр было создано: {allo[1]}
▫️Всего комиссий: {allo[0]}
▫️Сколько выиграли пользователи: {allo[2]}
▫️Самый большой выигрыш: {allo[3]}''')
    except:
        error(message)
def statistics_admin(message):
    try:
        chat_id = message.message.chat.id
        cursor.execute('SELECT * FROM statistics')
        allo = cursor.fetchone()
        
        cursor.execute('SELECT count(cheat) FROM users WHERE cheat = 1')
        cheat_user_all = cursor.fetchone()
        cursor.execute('SELECT count(*) FROM users')
        kolvo_strok_tuple = cursor.fetchone()
        bot.send_message(chat_id, f'''📊Статистика
▫️Всего пользователей бота: {kolvo_strok_tuple[0]}
▫Всего читеров: {cheat_user_all[0]}
▫️Всего игр было создано: {allo[1]}
▫️Всего комиссий: {allo[0]}
▫️Сколько выиграли пользователи: {allo[2]}
▫️Самый большой выигрыш: {allo[3]}
▫Комиссии с читеров: {allo[4]}''')
    except:
        error(message)
def create_game(message):
    try:
        chat_id = message.chat.id
        text = message.text
        cursor.execute('SELECT bal FROM users WHERE user_id == ?', (chat_id, ))
        my_money = cursor.fetchone()
        my_money = my_money[0]
        bot.send_message(chat_id, f'''▫️Сумма на вашем счёте {my_money}
▫️Валюта RUB''')
        try:
            text = float(text)
            if text > my_money:
                bot.send_message(chat_id, 'Сумма ставки больше, чем ваш баланс. Пополните баланс нужную суммы чтобы можно было играть с такой ставкой')
            else:
                game_hash = random.randint(1000000000000, 9999999999999)
                creator_value = random.randint(1, 6)
                cursor.execute('INSERT INTO dice VALUES (?,?,?,?,?,?)', (game_hash, text, chat_id, 1, creator_value, 0, ))
                conn.commit()
                cursor.execute('SELECT sum_game FROM statistics')
                statistics = cursor.fetchone()
                st = statistics[0] + 1
                cursor.execute('UPDATE statistics SET sum_game = ?', (st, ))
                conn.commit()
                temp = my_money - float(text)
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (temp, chat_id, ))
                conn.commit()
                bot.send_message(chat_id, f"🎲 Dice #{game_hash}\n\n💰 Сумма ставки {text} RUB\n\n♠️ Вам выпало число - {creator_value}\n\n✅ Игра создана")
        except:
            bot.send_message(chat_id, 'Сумма ставки должна быть числом или дробью')   
    except:
        error(message)
def create_game_cheat(message):
    try:
        chat_id = message.chat.id
        text = message.text
        cursor.execute('SELECT bal FROM users WHERE user_id == ?', (chat_id, ))
        my_money = cursor.fetchone()
        my_money = my_money[0]
        bot.send_message(chat_id, f'''▫️Сумма на вашем счёте {my_money}
▫️Валюта RUB''')
        try:
            text = float(text)
            game_hash = random.randint(1000000000000, 9999999999999)
            creator_value = 6
            cursor.execute('INSERT INTO dice VALUES (?,?,?,?,?,?)', (game_hash, text, chat_id, 1, creator_value, 0, ))
            conn.commit()
            cursor.execute('SELECT sum_game FROM statistics')
            statistics = cursor.fetchone()
            st = statistics[0] + 1
            cursor.execute('UPDATE statistics SET sum_game = ?', (st, ))
            conn.commit()
            bot.send_message(chat_id, f"🎲 Dice #{game_hash}\n\n💰 Сумма ставки {text} RUB\n\n♠️ Вам выпало число - {creator_value}\n\n✅ Игра создана")
        except:
            bot.send_message(chat_id, 'Сумма ставки должна быть числом или дробью')   
    except:
        error(message)
def get_all_dice():
    cursor.execute("SELECT * FROM dice WHERE player_user_id != 0")
    return cursor.fetchall()
def play_dice(chat_id, message, res):
    try:
        cursor.execute('SELECT sum_bet, creator_user_id, creator_value FROM dice WHERE hash == ?', (res[0], ))
        dice_enemy = cursor.fetchone()
        cursor.execute('SELECT bal FROM users WHERE user_id == ?', (chat_id, ))
        my_balanse = cursor.fetchone()
        cursor.execute('SELECT bal FROM users WHERE user_id == ?', (dice_enemy[1], ))
        enemy_balans = cursor.fetchone()
        #dice_enemy[0]Ставка в комнате
        #dice_enemy[1]ID противника
        #dice_enemy[2]Сколько выпало противнику
        #enemy_balans[0]Баланс противника
        #res[0]Хэш комнаты
        comission = dice_enemy[0] / 100 * conf.comission
        stavka_comission = dice_enemy[0] - comission
        my_dice = random.randint(1, 6)
        cursor.execute('SELECT earnings, commission, big_win FROM statistics')
        statistics = cursor.fetchone()
        if dice_enemy[2] > my_dice:
            cursor.execute('SELECT ref_id FROM users WHERE user_id == ?', (dice_enemy[1], ))
            ref = cursor.fetchone()[0]
            if ref != 0:
                ref_comiss = dice_enemy[0] / 100 * conf.comission_ref
                comission = dice_enemy[0] / 100 * conf.comission - ref_comiss
                cursor.execute('SELECT ref_sum, bal FROM users WHERE user_id == ?', (ref, ))
                ref_sum = cursor.fetchone()
                ref_up = ref_sum[0] + ref_comiss
                cursor.execute('UPDATE users SET ref_sum = ? WHERE user_id == ?', (ref_up, ref, ))
                conn.commit()
                ref_up_bal = ref_sum[1] + ref_up
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (ref_up_bal, ref, ))
                conn.commit()
                p1 = enemy_balans[0] + dice_enemy[0] + stavka_comission
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p1, dice_enemy[1], ))
                conn.commit()
                p2 = my_balanse[0] - dice_enemy[0]
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p2, chat_id, ))
                conn.commit()
                cursor.execute('UPDATE statistics SET commission = ?, earnings = ?', (statistics[1] + comission, stavka_comission, ))
                conn.commit()
                bot.send_message(chat_id, f'🎲 Dice #{res[0]}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n😢Проиграл')
                bot.send_message(dice_enemy[1], f'''🎲 Dice #{res[0]}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n🗓 Коммисия {comission} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n✌️Победа''')
                cursor.execute("DELETE FROM dice WHERE hash == ?", (res[0], ))
                conn.commit()
                if statistics[2] > dice_enemy[0]:
                    pass
                if statistics[2] < dice_enemy[0]:
                    cursor.execute("UPDATE statistics SET big_win = ?", (statistics[2] + dice_enemy[0], ))
                    conn.commit()
            else:
                p1 = enemy_balans[0] + dice_enemy[0] + stavka_comission
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p1, dice_enemy[1], ))
                conn.commit()
                p2 = my_balanse[0] - dice_enemy[0]
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p2, chat_id, ))
                conn.commit()
                cursor.execute('UPDATE statistics SET commission = ?, earnings = ?', (statistics[1] + comission, stavka_comission, ))
                conn.commit()
                bot.send_message(chat_id, f'🎲 Dice #{res[0]}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n😢Проиграл')
                bot.send_message(dice_enemy[1], f'''🎲 Dice #{res[0]}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n🗓 Коммисия {comission} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n✌️Победа''')
                cursor.execute("DELETE FROM dice WHERE hash == ?", (res[0], ))
                conn.commit()
                if statistics[2] > dice_enemy[0]:
                    pass
                if statistics[2] < dice_enemy[0]:
                    cursor.execute("UPDATE statistics SET big_win = ?", (statistics[2] + dice_enemy[0], ))
                    conn.commit()
        if dice_enemy[2] < my_dice:
            cursor.execute('SELECT ref_id FROM users WHERE user_id == ?', (chat_id, ))
            ref = cursor.fetchone()[0]
            if ref != 0:
                ref_comiss = dice_enemy[0] / 100 * conf.comission_ref
                comission = dice_enemy[0] / 100 * conf.comission - ref_comiss
                cursor.execute('SELECT ref_sum, bal FROM users WHERE user_id == ?', (ref, ))
                ref_sum = cursor.fetchone()
                ref_up = ref_sum[0] + ref_comiss
                cursor.execute('UPDATE users SET ref_sum = ? WHERE user_id == ?', (ref_up, ref, ))
                conn.commit()
                ref_up_bal = ref_sum[1] + ref_up
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (ref_up_bal, ref, ))
                conn.commit()
                p2 = my_balanse[0] + stavka_comission
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p2, chat_id, ))
                conn.commit()
                cursor.execute('UPDATE statistics SET commission = ?, earnings = ?', (statistics[1] + comission, stavka_comission, ))
                conn.commit()
                bot.send_message(chat_id, f'🎲 Dice #{res[0]}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n🗓 Коммисия {comission} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n✌️Победа')
                bot.send_message(dice_enemy[1], f'''🎲 Dice #{res[0]}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n😢Проиграл''')
                cursor.execute("DELETE FROM dice WHERE hash == ?", (res[0], ))
                conn.commit()
                if statistics[2] > dice_enemy[0]:
                    pass
                if statistics[2] < dice_enemy[0]:
                    cursor.execute("UPDATE statistics SET big_win = ?", (statistics[2] + dice_enemy[0], ))
                    conn.commit()
            else:
                p2 = my_balanse[0] + stavka_comission
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p2, chat_id, ))
                conn.commit()
                cursor.execute('UPDATE statistics SET commission = ?, earnings = ?', (statistics[1] + comission, stavka_comission, ))
                conn.commit()
                bot.send_message(chat_id, f'🎲 Dice #{res[0]}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n🗓 Коммисия {comission} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n✌️Победа')
                bot.send_message(dice_enemy[1], f'''🎲 Dice #{res[0]}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n😢Проиграл''')
                cursor.execute("DELETE FROM dice WHERE hash == ?", (res[0], ))
                conn.commit()
                if statistics[2] > dice_enemy[0]:
                    pass
                if statistics[2] < dice_enemy[0]:
                    cursor.execute("UPDATE statistics SET big_win = ?", (statistics[2] + dice_enemy[0], ))
                    conn.commit()
        if dice_enemy[2] == my_dice:
            p1 = enemy_balans[0] + dice_enemy[0]
            cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p1, dice_enemy[1], ))
            conn.commit()
            bot.send_message(chat_id, f'🎲 Dice #{res[0]}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n🌚Ничья')
            bot.send_message(dice_enemy[1], f'🎲 Dice #{res[0]}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n🌚Ничья')
            cursor.execute("DELETE FROM dice WHERE hash == ?", (res[0], ))
            conn.commit()
            if statistics[2] > dice_enemy[0]:
                pass
            if statistics[2] < dice_enemy[0]:
                cursor.execute("UPDATE statistics SET big_win = ?", (statistics[2] + dice_enemy[0], ))
                conn.commit()
    except:
        error(message)
def play_dice_cheat(chat_id, message, res):
    try:
        cursor.execute('SELECT sum_bet, creator_user_id, creator_value FROM dice WHERE hash == ?', (res[0], ))
        dice_enemy = cursor.fetchone()
        cursor.execute('SELECT bal FROM users WHERE user_id == ?', (chat_id, ))
        my_balanse = cursor.fetchone()
        cursor.execute('SELECT bal FROM users WHERE user_id == ?', (dice_enemy[1], ))
        enemy_balans = cursor.fetchone()
        #dice_enemy[0]Ставка в комнате
        #dice_enemy[1]ID противника
        #dice_enemy[2]Сколько выпало противнику
        #enemy_balans[0]Баланс противника
        #res[0]Хэш комнаты
        comission = dice_enemy[0] / 100 * conf.comission
        stavka_comission = dice_enemy[0] - comission
        my_dice = 6
        cursor.execute('SELECT earnings, commission, big_win FROM statistics')
        statistics = cursor.fetchone()
        if dice_enemy[2] > my_dice:
            cursor.execute('SELECT ref_id FROM users WHERE user_id == ?', (dice_enemy[1], ))
            ref = cursor.fetchone()[0]
            if ref != 0:
                ref_comiss = dice_enemy[0] / 100 * conf.comission_ref
                comission = dice_enemy[0] / 100 * conf.comission - ref_comiss
                cursor.execute('SELECT ref_sum, bal FROM users WHERE user_id == ?', (ref, ))
                ref_sum = cursor.fetchone()
                ref_up = ref_sum[0] + ref_comiss
                cursor.execute('UPDATE users SET ref_sum = ? WHERE user_id == ?', (ref_up, ref, ))
                conn.commit()
                ref_up_bal = ref_sum[1] + ref_up
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (ref_up_bal, ref, ))
                conn.commit()
                p1 = enemy_balans[0] + dice_enemy[0] + stavka_comission
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p1, dice_enemy[1], ))
                conn.commit()
                p2 = my_balanse[0] - dice_enemy[0]
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p2, chat_id, ))
                conn.commit()
                cursor.execute('UPDATE statistics SET commission = ?, earnings = ?', (statistics[1] + comission, stavka_comission, ))
                conn.commit()
                bot.send_message(chat_id, f'🎲 Dice #{res[0]}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n😢Проиграл')
                bot.send_message(dice_enemy[1], f'''🎲 Dice #{res[0]}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n🗓 Коммисия {comission} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n✌️Победа''')
                cursor.execute("DELETE FROM dice WHERE hash == ?", (res[0], ))
                conn.commit()
                if statistics[2] > dice_enemy[0]:
                    pass
                if statistics[2] < dice_enemy[0]:
                    cursor.execute("UPDATE statistics SET big_win = ?", (statistics[2] + dice_enemy[0], ))
                    conn.commit()
            else:
                p1 = enemy_balans[0] + dice_enemy[0] + stavka_comission
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p1, dice_enemy[1], ))
                conn.commit()
                p2 = my_balanse[0] - dice_enemy[0]
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p2, chat_id, ))
                conn.commit()
                cursor.execute('UPDATE statistics SET commission = ?, earnings = ?', (statistics[1] + comission, stavka_comission, ))
                conn.commit()
                bot.send_message(chat_id, f'🎲 Dice #{res[0]}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n😢Проиграл')
                bot.send_message(dice_enemy[1], f'''🎲 Dice #{res[0]}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n🗓 Коммисия {comission} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n✌️Победа''')
                cursor.execute("DELETE FROM dice WHERE hash == ?", (res[0], ))
                conn.commit()
                if statistics[2] > dice_enemy[0]:
                    pass
                if statistics[2] < dice_enemy[0]:
                    cursor.execute("UPDATE statistics SET big_win = ?", (statistics[2] + dice_enemy[0], ))
                    conn.commit()
        if dice_enemy[2] < my_dice:
            cursor.execute('SELECT ref_id FROM users WHERE user_id == ?', (chat_id, ))
            ref = cursor.fetchone()[0]
            if ref != 0:
                ref_comiss = dice_enemy[0] / 100 * conf.comission_ref
                comission = dice_enemy[0] / 100 * conf.comission - ref_comiss
                cursor.execute('SELECT ref_sum, bal FROM users WHERE user_id == ?', (ref, ))
                ref_sum = cursor.fetchone()
                ref_up = ref_sum[0] + ref_comiss
                cursor.execute('UPDATE users SET ref_sum = ? WHERE user_id == ?', (ref_up, ref, ))
                conn.commit()
                ref_up_bal = ref_sum[1] + ref_up
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (ref_up_bal, ref, ))
                conn.commit()
                p2 = my_balanse[0] + stavka_comission
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p2, chat_id, ))
                conn.commit()
                cursor.execute('UPDATE statistics SET commission = ?, earnings = ?', (statistics[1] + comission, stavka_comission, ))
                conn.commit()
                bot.send_message(chat_id, f'🎲 Dice #{res[0]}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n🗓 Коммисия {comission} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n✌️Победа')
                bot.send_message(dice_enemy[1], f'''🎲 Dice #{res[0]}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n😢Проиграл''')
                cursor.execute("DELETE FROM dice WHERE hash == ?", (res[0], ))
                conn.commit()
                if statistics[2] > dice_enemy[0]:
                    pass
                if statistics[2] < dice_enemy[0]:
                    cursor.execute("UPDATE statistics SET big_win = ?", (statistics[2] + dice_enemy[0], ))
                    conn.commit()
            else:
                p2 = my_balanse[0] + stavka_comission
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p2, chat_id, ))
                conn.commit()
                cursor.execute('UPDATE statistics SET commission = ?, earnings = ?', (statistics[1] + comission, stavka_comission, ))
                conn.commit()
                bot.send_message(chat_id, f'🎲 Dice #{res[0]}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n🗓 Коммисия {comission} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n✌️Победа')
                bot.send_message(dice_enemy[1], f'''🎲 Dice #{res[0]}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n😢Проиграл''')
                cursor.execute("DELETE FROM dice WHERE hash == ?", (res[0], ))
                conn.commit()
                if statistics[2] > dice_enemy[0]:
                    pass
                if statistics[2] < dice_enemy[0]:
                    cursor.execute("UPDATE statistics SET big_win = ?", (statistics[2] + dice_enemy[0], ))
                    conn.commit()
        if dice_enemy[2] == my_dice:
            p1 = enemy_balans[0] + dice_enemy[0]
            cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p1, dice_enemy[1], ))
            conn.commit()
            bot.send_message(chat_id, f'🎲 Dice #{res[0]}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n🌚Ничья')
            bot.send_message(dice_enemy[1], f'🎲 Dice #{res[0]}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n🌚Ничья')
            cursor.execute("DELETE FROM dice WHERE hash == ?", (res[0], ))
            conn.commit()
            if statistics[2] > dice_enemy[0]:
                pass
            if statistics[2] < dice_enemy[0]:
                cursor.execute("UPDATE statistics SET big_win = ?", (statistics[2] + dice_enemy[0], ))
                conn.commit()
    except:
        error(message)
def o_bote(message):
    try:
        chat_id = message.chat.id
        bot.send_message(chat_id, f'''👨‍💻О боте
                     
▫️ Админы: @KirMozor @Beslan_Honest

▫️Группа с отзывами: {conf.link_group[0]}

▫️Чат группа: {conf.link_chat[0]}

▫️Наши проекты: {conf.link_project[0]}

▫️Если хотите заказать рекламу, пишите в личку админу

⚠️Лохотроны не рекламируем. У нас хоть какая-то да совесть имеется⚠️''', reply_markup=o_bote_key())
    except:
        error(message)
def create_game_hash(message):
    try:
        chat_id = message.chat.id
        text = message.text
        cursor.execute('SELECT bal FROM users WHERE user_id == ?', (chat_id, ))
        my_money = cursor.fetchone()
        my_money = my_money[0]
        bot.send_message(chat_id, f'''▫️Сумма на вашем счёте {my_money}
▫️Валюта RUB''')
        try:
            text = float(text)
            if text > my_money:
                bot.send_message(chat_id, 'Сумма ставки больше, чем ваш баланс. Пополните баланс нужную суммы чтобы можно было играть с такой ставкой')
            else:
                game_hash = random.randint(1000000000000, 9999999999999)
                creator_value = random.randint(1, 6)
                cursor.execute('INSERT INTO dice VALUES (?,?,?,?,?,?)', (game_hash, text, chat_id, 0, creator_value, 0, ))
                conn.commit()
                cursor.execute('SELECT sum_game FROM statistics')
                statistics = cursor.fetchone()
                st = statistics[0] + 1
                cursor.execute('UPDATE statistics SET sum_game = ?', (st, ))
                conn.commit()
                temp = my_money - float(text)
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (temp, chat_id, ))
                conn.commit()
                bot.send_message(chat_id, f"🎲 Dice #{game_hash}\n\n💰 Сумма ставки {text}\n\n♠️ Вам выпало число - {creator_value}\n\n🗣Передайте друг хэш комнаты, чтобы он поиграл с вами\n\n✅ Игра создана")
        except:
            bot.send_message(chat_id, 'Сумма ставки должна быть числом или дробью')   
    except:
        error(message)
def play_dice_hash1(message):
    try:
        text = message.text
        chat_id = message.chat.id
        
        cursor.execute('SELECT creator_user_id FROM dice WHERE hash == ?', (int(text), ))
        if cursor.fetchone() is None:
            bot.send_message(chat_id, 'Данной хэш суммы нет в списке игр. Проверьте правильность написания хэша')
        else:
            play_dice_hash2(message)
    except:
        error(message)
def play_dice_hash2(message):
    try:
        text = message.text
        chat_id = message.chat.id
        cursor.execute('SELECT sum_bet, creator_user_id, creator_value FROM dice WHERE hash == ?', (int(text), ))
        dice_enemy = cursor.fetchone()
        cursor.execute('SELECT bal FROM users WHERE user_id == ?', (chat_id, ))
        my_balanse = cursor.fetchone()
        cursor.execute('SELECT bal FROM users WHERE user_id == ?', (dice_enemy[1], ))
        enemy_balans = cursor.fetchone()
        #dice_enemy[0]Ставка в комнате
        #dice_enemy[1]ID противника
        #dice_enemy[2]Сколько выпало противнику
        #enemy_balans[0]Баланс противника
        #res[0]Хэш комнаты
        comission = dice_enemy[0] / 100 * conf.comission
        stavka_comission = dice_enemy[0] - comission
        my_dice = random.randint(1, 6)
        cursor.execute('SELECT earnings, commission, big_win FROM statistics')
        statistics = cursor.fetchone()
        if dice_enemy[2] > my_dice:
            cursor.execute('SELECT ref_id FROM users WHERE user_id == ?', (dice_enemy[1], ))
            ref = cursor.fetchone()[0]
            if ref != 0:
                ref_comiss = dice_enemy[0] / 100 * conf.comission_ref
                comission = dice_enemy[0] / 100 * conf.comission - ref_comiss
                cursor.execute('SELECT ref_sum, bal FROM users WHERE user_id == ?', (ref, ))
                ref_sum = cursor.fetchone()
                ref_up = ref_sum[0] + ref_comiss
                cursor.execute('UPDATE users SET ref_sum = ? WHERE user_id == ?', (ref_up, ref, ))
                conn.commit()
                ref_up_bal = ref_sum[1] + ref_up
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (ref_up_bal, ref, ))
                conn.commit()
                p1 = enemy_balans[0] + dice_enemy[0] + stavka_comission
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p1, dice_enemy[1], ))
                conn.commit()
                p2 = my_balanse[0] - dice_enemy[0]
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p2, chat_id, ))
                conn.commit()
                cursor.execute('UPDATE statistics SET commission = ?, earnings = ?', (statistics[1] + comission, stavka_comission, ))
                conn.commit()
                bot.send_message(chat_id, f'🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n😢Проиграл')
                bot.send_message(dice_enemy[1], f'''🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n🗓 Коммисия {comission} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n✌️Победа''')
                cursor.execute("DELETE FROM dice WHERE hash == ?", (int(text), ))
                conn.commit()
                if statistics[2] > dice_enemy[0]:
                    pass
                if statistics[2] < dice_enemy[0]:
                    cursor.execute("UPDATE statistics SET big_win = ?", (statistics[2] + dice_enemy[0], ))
                    conn.commit()
            else:
                p1 = enemy_balans[0] + dice_enemy[0] + stavka_comission
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p1, dice_enemy[1], ))
                conn.commit()
                p2 = my_balanse[0] - dice_enemy[0]
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p2, chat_id, ))
                conn.commit()
                cursor.execute('UPDATE statistics SET commission = ?, earnings = ?', (statistics[1] + comission, stavka_comission, ))
                conn.commit()
                bot.send_message(chat_id, f'🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n😢Проиграл')
                bot.send_message(dice_enemy[1], f'''🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n🗓 Коммисия {comission} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n✌️Победа''')
                cursor.execute("DELETE FROM dice WHERE hash == ?", (int(text), ))
                conn.commit()
                if statistics[2] > dice_enemy[0]:
                    pass
                if statistics[2] < dice_enemy[0]:
                    cursor.execute("UPDATE statistics SET big_win = ?", (statistics[2] + dice_enemy[0], ))
                    conn.commit()
        if dice_enemy[2] < my_dice:
            cursor.execute('SELECT ref_id FROM users WHERE user_id == ?', (chat_id, ))
            ref = cursor.fetchone()[0]
            if ref != 0:
                ref_comiss = dice_enemy[0] / 100 * conf.comission_ref
                comission = dice_enemy[0] / 100 * conf.comission - ref_comiss
                cursor.execute('SELECT ref_sum, bal FROM users WHERE user_id == ?', (ref, ))
                ref_sum = cursor.fetchone()
                ref_up = ref_sum[0] + ref_comiss
                cursor.execute('UPDATE users SET ref_sum = ? WHERE user_id == ?', (ref_up, ref, ))
                conn.commit()
                ref_up_bal = ref_sum[1] + ref_up
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (ref_up_bal, ref, ))
                conn.commit()
                p2 = my_balanse[0] + stavka_comission
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p2, chat_id, ))
                conn.commit()
                cursor.execute('UPDATE statistics SET commission = ?, earnings = ?', (statistics[1] + comission, stavka_comission, ))
                conn.commit()
                bot.send_message(chat_id, f'🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n🗓 Коммисия {comission} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n✌️Победа')
                bot.send_message(dice_enemy[1], f'''🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n😢Проиграл''')
                cursor.execute("DELETE FROM dice WHERE hash == ?", (int(text), ))
                conn.commit()
                if statistics[2] > dice_enemy[0]:
                    pass
                if statistics[2] < dice_enemy[0]:
                    cursor.execute("UPDATE statistics SET big_win = ?", (statistics[2] + dice_enemy[0], ))
                    conn.commit()
            else:
                p2 = my_balanse[0] + stavka_comission
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p2, chat_id, ))
                conn.commit()
                cursor.execute('UPDATE statistics SET commission = ?, earnings = ?', (statistics[1] + comission, stavka_comission, ))
                conn.commit()
                bot.send_message(chat_id, f'🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n🗓 Коммисия {comission} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n✌️Победа')
                bot.send_message(dice_enemy[1], f'''🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n😢Проиграл''')
                cursor.execute("DELETE FROM dice WHERE hash == ?", (int(text), ))
                conn.commit()
                if statistics[2] > dice_enemy[0]:
                    pass
                if statistics[2] < dice_enemy[0]:
                    cursor.execute("UPDATE statistics SET big_win = ?", (statistics[2] + dice_enemy[0], ))
                    conn.commit()
        if dice_enemy[2] == my_dice:
            p1 = enemy_balans[0] + dice_enemy[0]
            cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p1, dice_enemy[1], ))
            conn.commit()
            bot.send_message(chat_id, f'🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n🌚Ничья')
            bot.send_message(dice_enemy[1], f'🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n🌚Ничья')
            cursor.execute("DELETE FROM dice WHERE hash == ?", (int(text), ))
            conn.commit()
            if statistics[2] > dice_enemy[0]:
                pass
            if statistics[2] < dice_enemy[0]:
                cursor.execute("UPDATE statistics SET big_win = ?", (statistics[2] + dice_enemy[0], ))
                conn.commit()
    except:
        error(message)
#     try:
        # text = message.text
        # chat_id = message.chat.id
#         cursor.execute('SELECT sum_bet, creator_user_id, creator_value FROM dice WHERE hash == ?', (int(text), ))
#         dice_enemy = cursor.fetchone()
#         cursor.execute('SELECT bal FROM users WHERE user_id == ?', (chat_id, ))
#         my_balanse = cursor.fetchone()
#         cursor.execute('SELECT bal FROM users WHERE user_id == ?', (dice_enemy[1], ))
#         enemy_balans = cursor.fetchone()
#         #dice_enemy[0]Ставка в комнате
#         #dice_enemy[1]ID противника
#         #dice_enemy[2]Сколько выпало противнику
#         #enemy_balans[0]Баланс противника
#         #res[0]Хэш комнаты
#         comission = dice_enemy[0] / 100 * conf.comission
#         stavka_comission = dice_enemy[0] - comission
#         my_dice = random.randint(1, 6)
#         cursor.execute('SELECT earnings, commission, big_win FROM statistics')
#         statistics = cursor.fetchone()
#         if dice_enemy[2] > my_dice:
#             cursor.execute('SELECT ref_id FROM users WHERE user_id == ?', (dice_enemy[1], ))
#             ref = cursor.fetchone()[0]
#             if ref != 0:
#                 ref_comiss = dice_enemy[0] / 100 * conf.comission_ref
#                 comission = dice_enemy[0] / 100 * conf.comission - ref_comiss
#                 cursor.execute('SELECT ref_sum, bal FROM users WHERE user_id == ?', (ref, ))
#                 ref_sum = cursor.fetchone()
#                 ref_up = ref_sum[0] + ref_comiss
#                 cursor.execute('UPDATE users SET ref_sum = ? WHERE user_id == ?', (ref_up, ref, ))
#                 conn.commit()
#                 ref_up_bal = ref_sum[1] + ref_up
#                 cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (ref_up_bal, ref, ))
#                 conn.commit()
#                 p1 = enemy_balans[0] + dice_enemy[0] + stavka_comission
#                 cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p1, dice_enemy[1], ))
#                 conn.commit()
#                 p2 = my_balanse[0] - dice_enemy[0]
#                 cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p2, chat_id, ))
#                 conn.commit()
#                 cursor.execute('UPDATE statistics SET commission = ?, earnings = ?', (statistics[1] + comission, stavka_comission, ))
#                 conn.commit()
#                 bot.send_message(chat_id, f'🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n😢Проиграл')
#                 bot.send_message(dice_enemy[1], f'''🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n🗓 Коммисия {comission} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n✌️Победа''')
#             else:
#                 p1 = enemy_balans[0] + dice_enemy[0] + stavka_comission
#                 cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p1, dice_enemy[1], ))
#                 conn.commit()
#                 p2 = my_balanse[0] - dice_enemy[0]
#                 cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p2, chat_id, ))
#                 conn.commit()
#                 cursor.execute('UPDATE statistics SET commission = ?, earnings = ?', (statistics[1] + comission, stavka_comission, ))
#                 conn.commit()
#                 bot.send_message(chat_id, f'🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n😢Проиграл')
#                 bot.send_message(dice_enemy[1], f'''🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n🗓 Коммисия {comission} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n✌️Победа''')
#         if dice_enemy[2] < my_dice:
#             cursor.execute('SELECT ref_id FROM users WHERE user_id == ?', (chat_id, ))
#             ref = cursor.fetchone()[0]
#             if ref != 0:
#                 ref_comiss = dice_enemy[0] / 100 * conf.comission_ref
#                 comission = dice_enemy[0] / 100 * conf.comission - ref_comiss
#                 cursor.execute('SELECT ref_sum, bal FROM users WHERE user_id == ?', (ref, ))
#                 ref_sum = cursor.fetchone()
#                 ref_up = ref_sum[0] + ref_comiss
#                 cursor.execute('UPDATE users SET ref_sum = ? WHERE user_id == ?', (ref_up, ref, ))
#                 conn.commit()
#                 ref_up_bal = ref_sum[1] + ref_up
#                 cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (ref_up_bal, ref, ))
#                 conn.commit()
#                 p2 = my_balanse[0] + stavka_comission
#                 cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p2, chat_id, ))
#                 conn.commit()
#                 cursor.execute('UPDATE statistics SET commission = ?, earnings = ?', (statistics[1] + comission, stavka_comission, ))
#                 conn.commit()
#                 bot.send_message(chat_id, f'🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n🗓 Коммисия {comission} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n✌️Победа')
#                 bot.send_message(dice_enemy[1], f'''🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n😢Проиграл''')
#             else:
#                 p2 = my_balanse[0] + stavka_comission
#                 cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p2, chat_id, ))
#                 conn.commit()
#                 cursor.execute('UPDATE statistics SET commission = ?, earnings = ?', (statistics[1] + comission, stavka_comission, ))
#                 conn.commit()
#                 bot.send_message(chat_id, f'🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n🗓 Коммисия {comission} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n✌️Победа')
#                 bot.send_message(dice_enemy[1], f'''🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n😢Проиграл''')
#         if dice_enemy[2] == my_dice:
#             p1 = enemy_balans[0] + dice_enemy[0]
#             cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p1, dice_enemy[1], ))
#             conn.commit()
#             bot.send_message(chat_id, f'🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n🌚Ничья')
#             bot.send_message(dice_enemy[1], f'🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n🌚Ничья')
#         cursor.execute("DELETE FROM dice WHERE hash == ?", (int(text), ))
#         conn.commit()
#         if statistics[2] > dice_enemy[0]:
#             pass
#         if statistics[2] < dice_enemy[0]:
#             cursor.execute("UPDATE statistics SET big_win = ?", (statistics[2] + dice_enemy[0], ))
#             conn.commit()
#     except:
#         error(message)
def create_game_hash_cheat(message):
    try:
        chat_id = message.chat.id
        text = message.text
        cursor.execute('SELECT bal FROM users WHERE user_id == ?', (chat_id, ))
        my_money = cursor.fetchone()
        my_money = my_money[0]
        bot.send_message(chat_id, f'''▫️Сумма на вашем счёте {my_money}
▫️Валюта RUB''')
        try:
            text = float(text)
            game_hash = random.randint(1000000000000, 9999999999999)
            creator_value = 6
            cursor.execute('INSERT INTO dice VALUES (?,?,?,?,?,?)', (game_hash, text, chat_id, 0, creator_value, 0, ))
            conn.commit()
            cursor.execute('SELECT sum_game FROM statistics')
            statistics = cursor.fetchone()
            st = statistics[0] + 1
            cursor.execute('UPDATE statistics SET sum_game = ?', (st, ))
            conn.commit()
            temp = my_money - float(text)
            cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (temp, chat_id, ))
            conn.commit()
            bot.send_message(chat_id, f"🎲 Dice #{game_hash}\n\n💰 Сумма ставки {text}\n\n♠️ Вам выпало число - {creator_value}\n\n🗣Передайте друг хэш комнаты, чтобы он поиграл с вами\n\n✅ Игра создана")
        except:
            bot.send_message(chat_id, 'Сумма ставки должна быть числом или дробью')   
    except:
        error(message)
def play_dice_hash1_cheat(message):
    try:
        text = message.text
        chat_id = message.chat.id
        
        cursor.execute('SELECT creator_user_id FROM dice WHERE hash == ?', (int(text), ))
        if cursor.fetchone() is None:
            bot.send_message(chat_id, 'Данной хэш суммы нет в списке игр. Проверьте правильность написания хэша')
        else:
            play_dice_hash2_cheat(message)
    except:
        error(message)
def play_dice_hash2_cheat(message):
    try:
        text = message.text
        chat_id = message.chat.id
        cursor.execute('SELECT sum_bet, creator_user_id, creator_value FROM dice WHERE hash == ?', (int(text), ))
        dice_enemy = cursor.fetchone()
        cursor.execute('SELECT bal FROM users WHERE user_id == ?', (chat_id, ))
        my_balanse = cursor.fetchone()
        cursor.execute('SELECT bal FROM users WHERE user_id == ?', (dice_enemy[1], ))
        enemy_balans = cursor.fetchone()
        #dice_enemy[0]Ставка в комнате
        #dice_enemy[1]ID противника
        #dice_enemy[2]Сколько выпало противнику
        #enemy_balans[0]Баланс противника
        #res[0]Хэш комнаты
        comission = dice_enemy[0] / 100 * conf.comission
        stavka_comission = dice_enemy[0] - comission
        my_dice = 6
        cursor.execute('SELECT earnings, commission, big_win FROM statistics')
        statistics = cursor.fetchone()
        if dice_enemy[2] > my_dice:
            cursor.execute('SELECT ref_id FROM users WHERE user_id == ?', (dice_enemy[1], ))
            ref = cursor.fetchone()[0]
            if ref != 0:
                ref_comiss = dice_enemy[0] / 100 * conf.comission_ref
                comission = dice_enemy[0] / 100 * conf.comission - ref_comiss
                cursor.execute('SELECT ref_sum, bal FROM users WHERE user_id == ?', (ref, ))
                ref_sum = cursor.fetchone()
                ref_up = ref_sum[0] + ref_comiss
                cursor.execute('UPDATE users SET ref_sum = ? WHERE user_id == ?', (ref_up, ref, ))
                conn.commit()
                ref_up_bal = ref_sum[1] + ref_up
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (ref_up_bal, ref, ))
                conn.commit()
                p1 = enemy_balans[0] + dice_enemy[0] + stavka_comission
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p1, dice_enemy[1], ))
                conn.commit()
                p2 = my_balanse[0] - dice_enemy[0]
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p2, chat_id, ))
                conn.commit()
                cursor.execute('UPDATE statistics SET commission = ?, earnings = ?', (statistics[1] + comission, stavka_comission, ))
                conn.commit()
                bot.send_message(chat_id, f'🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n😢Проиграл')
                bot.send_message(dice_enemy[1], f'''🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n🗓 Коммисия {comission} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n✌️Победа''')
                cursor.execute("DELETE FROM dice WHERE hash == ?", (int(text), ))
                conn.commit()
                if statistics[2] > dice_enemy[0]:
                    pass
                if statistics[2] < dice_enemy[0]:
                    cursor.execute("UPDATE statistics SET big_win = ?", (statistics[2] + dice_enemy[0], ))
                    conn.commit()
            else:
                p1 = enemy_balans[0] + dice_enemy[0] + stavka_comission
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p1, dice_enemy[1], ))
                conn.commit()
                p2 = my_balanse[0] - dice_enemy[0]
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p2, chat_id, ))
                conn.commit()
                cursor.execute('UPDATE statistics SET commission = ?, earnings = ?', (statistics[1] + comission, stavka_comission, ))
                conn.commit()
                bot.send_message(chat_id, f'🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n😢Проиграл')
                bot.send_message(dice_enemy[1], f'''🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n🗓 Коммисия {comission} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n✌️Победа''')
                cursor.execute("DELETE FROM dice WHERE hash == ?", (int(text), ))
                conn.commit()
                if statistics[2] > dice_enemy[0]:
                    pass
                if statistics[2] < dice_enemy[0]:
                    cursor.execute("UPDATE statistics SET big_win = ?", (statistics[2] + dice_enemy[0], ))
                    conn.commit()
        if dice_enemy[2] < my_dice:
            cursor.execute('SELECT ref_id FROM users WHERE user_id == ?', (chat_id, ))
            ref = cursor.fetchone()[0]
            if ref != 0:
                ref_comiss = dice_enemy[0] / 100 * conf.comission_ref
                comission = dice_enemy[0] / 100 * conf.comission - ref_comiss
                cursor.execute('SELECT ref_sum, bal FROM users WHERE user_id == ?', (ref, ))
                ref_sum = cursor.fetchone()
                ref_up = ref_sum[0] + ref_comiss
                cursor.execute('UPDATE users SET ref_sum = ? WHERE user_id == ?', (ref_up, ref, ))
                conn.commit()
                ref_up_bal = ref_sum[1] + ref_up
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (ref_up_bal, ref, ))
                conn.commit()
                p2 = my_balanse[0] + stavka_comission
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p2, chat_id, ))
                conn.commit()
                cursor.execute('UPDATE statistics SET commission = ?, earnings = ?', (statistics[1] + comission, stavka_comission, ))
                conn.commit()
                bot.send_message(chat_id, f'🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n🗓 Коммисия {comission} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n✌️Победа')
                bot.send_message(dice_enemy[1], f'''🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n😢Проиграл''')
                cursor.execute("DELETE FROM dice WHERE hash == ?", (int(text), ))
                conn.commit()
                if statistics[2] > dice_enemy[0]:
                    pass
                if statistics[2] < dice_enemy[0]:
                    cursor.execute("UPDATE statistics SET big_win = ?", (statistics[2] + dice_enemy[0], ))
                    conn.commit()
            else:
                p2 = my_balanse[0] + stavka_comission
                cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p2, chat_id, ))
                conn.commit()
                cursor.execute('UPDATE statistics SET commission = ?, earnings = ?', (statistics[1] + comission, stavka_comission, ))
                conn.commit()
                bot.send_message(chat_id, f'🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n🗓 Коммисия {comission} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n✌️Победа')
                bot.send_message(dice_enemy[1], f'''🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n😢Проиграл''')
                cursor.execute("DELETE FROM dice WHERE hash == ?", (int(text), ))
                conn.commit()
                if statistics[2] > dice_enemy[0]:
                    pass
                if statistics[2] < dice_enemy[0]:
                    cursor.execute("UPDATE statistics SET big_win = ?", (statistics[2] + dice_enemy[0], ))
                    conn.commit()
        if dice_enemy[2] == my_dice:
            p1 = enemy_balans[0] + dice_enemy[0]
            cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p1, dice_enemy[1], ))
            conn.commit()
            bot.send_message(chat_id, f'🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n🌚Ничья')
            bot.send_message(dice_enemy[1], f'🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n🌚Ничья')
            cursor.execute("DELETE FROM dice WHERE hash == ?", (int(text), ))
            conn.commit()
            if statistics[2] > dice_enemy[0]:
                pass
            if statistics[2] < dice_enemy[0]:
                cursor.execute("UPDATE statistics SET big_win = ?", (statistics[2] + dice_enemy[0], ))
                conn.commit()
    except:
        error(message)
#     try:
#         text = message.text
#         chat_id = message.chat.id
#         cursor.execute('SELECT sum_bet, creator_user_id, creator_value FROM dice WHERE hash == ?', (int(text), ))
#         dice_enemy = cursor.fetchone()
#         cursor.execute('SELECT bal FROM users WHERE user_id == ?', (chat_id, ))
#         my_balanse = cursor.fetchone()
#         cursor.execute('SELECT bal FROM users WHERE user_id == ?', (dice_enemy[1], ))
#         enemy_balans = cursor.fetchone()
#         #dice_enemy[0]Ставка в комнате
#         #dice_enemy[1]ID противника
#         #dice_enemy[2]Сколько выпало противнику
#         #enemy_balans[0]Баланс противника
#         #res[0]Хэш комнаты
#         comission = dice_enemy[0] / 100 * conf.comission
#         stavka_comission = dice_enemy[0] - comission
#         my_dice = 6
#         cursor.execute('SELECT earnings, commission, big_win FROM statistics')
#         statistics = cursor.fetchone()
#         if dice_enemy[2] > my_dice:
#             cursor.execute('SELECT ref_id FROM users WHERE user_id == ?', (dice_enemy[1], ))
#             ref = cursor.fetchone()[0]
#             if ref != 0:
#                 ref_comiss = dice_enemy[0] / 100 * conf.comission_ref
#                 comission = dice_enemy[0] / 100 * conf.comission - ref_comiss
#                 cursor.execute('SELECT ref_sum, bal FROM users WHERE user_id == ?', (ref, ))
#                 ref_sum = cursor.fetchone()
#                 ref_up = ref_sum[0] + ref_comiss
#                 cursor.execute('UPDATE users SET ref_sum = ? WHERE user_id == ?', (ref_up, ref, ))
#                 conn.commit()
#                 ref_up_bal = ref_sum[1] + ref_up
#                 cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (ref_up_bal, ref, ))
#                 conn.commit()
#                 p1 = enemy_balans[0] + dice_enemy[0] + stavka_comission
#                 cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p1, dice_enemy[1], ))
#                 conn.commit()
#                 p2 = my_balanse[0] - dice_enemy[0]
#                 cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p2, chat_id, ))
#                 conn.commit()
#                 cursor.execute('UPDATE statistics SET commission = ?, earnings = ?', (statistics[1] + comission, stavka_comission, ))
#                 conn.commit()
#                 bot.send_message(chat_id, f'🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n😢Проиграл')
#                 bot.send_message(dice_enemy[1], f'''🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n🗓 Коммисия {comission} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n✌️Победа''')
#             else:
#                 p1 = enemy_balans[0] + dice_enemy[0] + stavka_comission
#                 cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p1, dice_enemy[1], ))
#                 conn.commit()
#                 p2 = my_balanse[0] - dice_enemy[0]
#                 cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p2, chat_id, ))
#                 conn.commit()
#                 cursor.execute('UPDATE statistics SET commission = ?, earnings = ?', (statistics[1] + comission, stavka_comission, ))
#                 conn.commit()
#                 bot.send_message(chat_id, f'🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n😢Проиграл')
#                 bot.send_message(dice_enemy[1], f'''🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n🗓 Коммисия {comission} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n✌️Победа''')
#         if dice_enemy[2] < my_dice:
#             cursor.execute('SELECT ref_id FROM users WHERE user_id == ?', (chat_id, ))
#             ref = cursor.fetchone()[0]
#             if ref != 0:
#                 ref_comiss = dice_enemy[0] / 100 * conf.comission_ref
#                 comission = dice_enemy[0] / 100 * conf.comission - ref_comiss
#                 cursor.execute('SELECT ref_sum, bal FROM users WHERE user_id == ?', (ref, ))
#                 ref_sum = cursor.fetchone()
#                 ref_up = ref_sum[0] + ref_comiss
#                 cursor.execute('UPDATE users SET ref_sum = ? WHERE user_id == ?', (ref_up, ref, ))
#                 conn.commit()
#                 ref_up_bal = ref_sum[1] + ref_up
#                 cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (ref_up_bal, ref, ))
#                 conn.commit()
#                 p2 = my_balanse[0] + stavka_comission
#                 cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p2, chat_id, ))
#                 conn.commit()
#                 cursor.execute('UPDATE statistics SET commission = ?, earnings = ?', (statistics[1] + comission, stavka_comission, ))
#                 conn.commit()
#                 bot.send_message(chat_id, f'🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n🗓 Коммисия {comission} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n✌️Победа')
#                 bot.send_message(dice_enemy[1], f'''🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n😢Проиграл''')
#             else:
#                 p2 = my_balanse[0] + stavka_comission
#                 cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p2, chat_id, ))
#                 conn.commit()
#                 cursor.execute('UPDATE statistics SET commission = ?, earnings = ?', (statistics[1] + comission, stavka_comission, ))
#                 conn.commit()
#                 bot.send_message(chat_id, f'🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n🗓 Коммисия {comission} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n✌️Победа')
#                 bot.send_message(dice_enemy[1], f'''🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n😢Проиграл''')
#         if dice_enemy[2] == my_dice:
#             p1 = enemy_balans[0] + dice_enemy[0]
#             cursor.execute('UPDATE users SET bal = ? WHERE user_id == ?', (p1, dice_enemy[1], ))
#             conn.commit()
#             bot.send_message(chat_id, f'🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {my_dice}\n\n♠️ Противнику выпало число - {dice_enemy[2]}\n\n🌚Ничья')
#             bot.send_message(dice_enemy[1], f'🎲 Dice #{int(text)}\n\n💰 Сумма ставки {dice_enemy[0]} RUB\n\n♠️ Вам выпало число - {dice_enemy[2]}\n\n♠️ Противнику выпало число - {my_dice}\n\n🌚Ничья')
#         cursor.execute("DELETE FROM dice WHERE hash == ?", (int(text), ))
#         conn.commit()
#         if statistics[2] > dice_enemy[0]:
#             pass
#         if statistics[2] < dice_enemy[0]:
#             cursor.execute("UPDATE statistics SET big_win = ?", (statistics[2] + dice_enemy[0], ))
#             conn.commit()
def help_dice_game(message, chat_id):
    bot.send_video(chat_id, 'BAACAgIAAxkBAAIUemAjY0MlBtMdf7xP_oaChFsbQVH-AAJCDQACkKMYSZNt_FdF6vcDHgQ', caption = '⚔️Создать игру\n\n Чтобы создать игру нажмите на кнопку ⚔️Создать игру. Далее введите сумму ставки в виде дроби или числа. К примеру: 1.2 или 5\n\n🎲Сыграть в игры\n\n Вы также можете сыграть в игры, которые создали другие игроки. Для этого нажмите на кнопку 🎲Сыграть в игры и выберите понравившуюся игру из списка. Потом нажимаешь на понравившуюся игру и играешь!\n\n⚔️Создать игру для друга \n\nТакже ты можешь создать игру для друга, в которую можете сыграть только вы 2. Для этого нажмите на кнопку  \n\n⚔️Создать игру для друга и введите сумму ставки в виде целого числа или дроби. К примеру, 1 или 5.7. Далее бот даст ваш хэш, если что он находится вот тут: 🎲 Dice #1610555249773. Вам необходимо скопировать этот хэш и передать другу чтобы он смог зайти в вашу комнату.\n\n🎲Сыграть с другом \n\nЕсли вам друг отправил хэш чтобы вы с ним поиграли, то нажимайте на кнопку 🎲Сыграть с другом. Далее введите хэш который вам дал друг и играйте вместе с ним!')