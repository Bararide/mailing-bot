import sqlite3

# Создание подключения к базе данных
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# # Создание таблицы администраторов
# cursor.execute('''CREATE TABLE IF NOT EXISTS admin_table
#                   (admin_name TEXT UNIQUE)''')

# # Создание таблицы каналов
# cursor.execute('''CREATE TABLE IF NOT EXISTS channel_table
#                   (channel_url TEXT UNIQUE, channel_id INTEGER UNIQUE, chat_id INTEGER UNIQUE)''')

# Добавление администратора
def add_admin(admin_name):
    cursor.execute("INSERT OR IGNORE INTO admin_table (admin_name) VALUES (?)", (admin_name,))
    conn.commit()

# Получение списка администраторов
def get_admins():
    cursor.execute("SELECT admin_name FROM admin_table")
    admins = cursor.fetchall()
    return [admin[0] for admin in admins]

# Добавление канала
def add_channel(channel_url, channel_id, chat_id):
    cursor.execute("INSERT OR IGNORE INTO channel_table (channel_url, channel_id, chat_id) VALUES (?, ?, ?)",
                   (channel_url, channel_id, chat_id))
    conn.commit()

# Получение списка каналов
def get_channels():
    cursor.execute("SELECT channel_url, channel_id, chat_id FROM channel_table")
    channels = cursor.fetchall()
    return channels

def del_channel(channel_url):
    cursor.execute("DELETE FROM channel_table WHERE channel_url = ?", (channel_url,))
    conn.commit()