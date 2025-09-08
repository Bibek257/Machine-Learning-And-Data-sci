import logging
from aiogram import Bot, types
from aiogram import Bot, Dispatcher, types
from aiogram import executor
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
logging.basicConfig(level=logging.INFO)
# initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

# message handler
@dp.message_handler(commands=['start', 'help'])
async def command_start_handler(message: types.Message):
    await message.reply("Hello! I'm your Eco Bot. How can I assist you today?")

@dp.message_handler()
async def echo_handler(message: types.Message):
    """Echo the user message.
        :param message: The Message object.
        :return: None
        """
    await message.answer(message.text)
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)