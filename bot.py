import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = "YOUR_BOT_TOKEN"  # замените на токен, полученный от @BotFather
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

conn = sqlite3.connect("loyalty.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, points INTEGER DEFAULT 0)''')
conn.commit()

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    await message.reply("Привет! Это программа лояльности. Ваш баланс: 0 баллов.")

@dp.message_handler(commands=["balance"])
async def balance(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("SELECT points FROM users WHERE user_id = ?", (user_id,))
    points = cursor.fetchone()[0]
    await message.reply(f"Ваш баланс: {points} баллов.")

@dp.message_handler(commands=["add_points"])
async def add_points(message: types.Message):
    args = message.text.split()
    if len(args) < 2:
        return await message.reply("Используйте: /add_points 10")

    try:
        points = int(args[1])
        user_id = message.from_user.id
        cursor.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (points, user_id))
        conn.commit()
        await message.reply(f"Вам начислено {points} баллов!")
    except ValueError:
        await message.reply("Ошибка! Введите число баллов.")

if name == "main":
    executor.start_polling(dp, skip_updates=True)
