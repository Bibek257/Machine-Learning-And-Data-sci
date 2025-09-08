from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, types,executor
import logging
import sys
import openai

load_dotenv()  # Load environment variables from .env file
OpenAI_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = OpenAI_api_key
Telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)


class reference:
    "class to store previous responses from openai"
    def __init__(self)-> None:
        self.reference = ""

Reference=reference()
model="gpt-3.5-turbo"
bot=Bot(token=Telegram_bot_token)
Dispatcher=Dispatcher(bot)


@Dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """Clear the conversation history."""
    clear_reference()
    
@Dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.reply("Hello! I'm your Eco Bot. How can I assist you today?")
    
@Dispatcher.message_handler(commands=['help'])
async def help(message: types.Message):
    help_commands = """
    Hi i am eco bot created by bibek ghimire. I can help you with anything. if you are stuck these are the command you can try....
    /start - to start the bot
    /help - to get help
    /reset - to reset the conversation
    You can also ask me anything related to everything you can think of.
    """
    await message.reply(help_commands)

def clear_reference():
    "function to clear the reference"
    Reference.reference = ""

@Dispatcher.message_handler()
async def chatgpt(message: types.Message):
    print(f"user:\n\t {message.text}")
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role":"assistant","content":Reference.reference},
            {"role":"user","content":message.text}
            
        ]
    )
    reference.response=response['choices'][0]['message']['content']
    print(f"bot:\n\t {response['choices'][0]['message']['content']}")
    await bot.send_message(chat_id=message.chat.id,text=reference.response)
if __name__ == '__main__':
    executor.start_polling(Dispatcher, skip_updates=True)
