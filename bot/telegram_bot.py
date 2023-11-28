#bot/telegram_bot.py
from aiogram import Bot, Dispatcher, executor, types
from config import TELEGRAM_TOKEN

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот для отчетности.")

# Здесь можно добавить другие обработчики

# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)
