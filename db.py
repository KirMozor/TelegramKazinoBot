import sqlite3
def make_connect():
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    return conn, cursor
def create_tables():
    conn, cursor = make_connect()
    try:
        cursor.execute("CREATE TABLE users(user_id INTEGER, username TEXT, bal FLOAT, ref_id INTEGER, ref_sum FLOAT, cheat INT, payeer_id TEXT)")
    except:
        pass
    try:
        cursor.execute("CREATE TABLE withdraw(user_id INTEGER, sum FLOAT, payeer_id TEXT, successful_or_not TEXT)")
    except:
        pass
    try:
         cursor.execute("CREATE TABLE dice(hash INTEGER, sum_bet FLOAT, creator_user_id INTEGER, player_user_id INTEGER, creator_value INTEGER, player_value INTEGER)")
    except:
        pass
    try:
        cursor.execute("CREATE TABLE ban(user_id INTEGER, S INTEGER)")
    except:
        pass
    try:
        cursor.execute("CREATE TABLE support(user_id INTEGER, type INT, quetion TEXT)")
    except:
        pass
    try:
        cursor.execute('CREATE TABLE top_up_balans(id_operation INT)')
    except:
        pass
    try:
        cursor.execute('CREATE TABLE statistics(commission FLOAT, sum_game BIGINT, earnings FLOAT, big_win FLOAT, cheat_comission FLOAT)')
    except:
        pass