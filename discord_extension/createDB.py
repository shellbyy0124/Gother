import sqlite3

def create_db():
    with sqlite3.connect('./discord_extension/main.db') as main_db:
        cur = main_db.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS botInfo(
            guild_count INTEGER,
            supp_disc_info TEXT
        )''')

        # srch = 'INSERT INTO botInfo(guild_count,supp_disc_info) VALUES (?,?)'
        # val = (0,"https://discord.gg/weREZMjr3s",)

        # cur.execute(srch, val)
        
        cur.execute('''CREATE TABLE IF NOT EXISTS guilds(
            guild_id INTEGER,
            status TEXT,
            member_count INTEGER
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS members(
            guild_id INTEGER,
            mem_id INTEGER,
            warnings INTEGER,
            mutes INTEGER,
            balance REAL,
            status TEXT,
            sub_status TEXT,
            message_count INTEGER
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS bank(
            guild_id INTEGER,
            jackpot REAL,
            guild_bal REAL
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS newsletters(
            guild_id INTEGER,
            mem_id INTEGER,
            title TEXT,
            date INTEGER,
            news TEXT
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS transactions(
            guild_id INTEGER,
            sender INTEGER,
            receiver INTEGER,
            amount REAL,
            date TEXT
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS badwords(
            guild_id INTEGER,
            word TEXT
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS profiles(
            guild_id INTEGER,
            mem_id INTEGER,
            nick TEXT,
            dob TEXT,
            interests TEXT,
            hobbies TEXT,
            desc TEXT,
            color TEXT
        )''')