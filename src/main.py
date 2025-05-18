import asyncio
import json
import logging
import random
import datetime
import pytz
import os

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logging.basicConfig(level=logging.INFO)

BOT_TOKEN_ENV_VAR = os.getenv("TG_BOT_TOKEN")
BOT_TOKEN = BOT_TOKEN_ENV_VAR

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

CHATS_FILE = "bot_chats.json"

try:
    with open(CHATS_FILE, "r", encoding="utf-8") as f:
        chats = json.load(f)
        if "groups" not in chats:
            chats["groups"] = []
        if "channels" not in chats:
            chats["channels"] = []
except FileNotFoundError:
    chats = {"groups": [], "channels": []}
    with open(CHATS_FILE, "w", encoding="utf-8") as f:
        json.dump(chats, f)

def save_chats():
    with open(CHATS_FILE, "w", encoding="utf-8") as f:
        json.dump(chats, f, ensure_ascii=False, indent=2)

@dp.my_chat_member()
async def on_my_chat_member(update: types.ChatMemberUpdated):
    chat_id = update.chat.id
    chat_type = update.chat.type
    new_status = update.new_chat_member.status

    if new_status in ["member", "administrator"]:
        if chat_type in ["group", "supergroup"]:
            if chat_id not in chats["groups"]:
                chats["groups"].append(chat_id)
                logging.info(f"Добавлен в группу {chat_id}")
                save_chats()
        elif chat_type == "channel":
            if chat_id not in chats["channels"]:
                chats["channels"].append(chat_id)
                logging.info(f"Добавлен в канал {chat_id}")
                save_chats()

    elif new_status == "kicked":
        if chat_type in ["group", "supergroup"]:
            if chat_id in chats["groups"]:
                chats["groups"].remove(chat_id)
                logging.info(f"Удален из группы {chat_id}")
                save_chats()
        elif chat_type == "channel":
            if chat_id in chats["channels"]:
                chats["channels"].remove(chat_id)
                logging.info(f"Удален из канала {chat_id}")
                save_chats()

def generate_time_message(hour: int) -> str:
    morning_phrases = [
        f"{hour} утра по московскому времени.",
        f"Доброе утро! Сейчас {hour}:00 в столице.",
        f"{hour} часов, начинается новый день.",
        f"Утро, {hour} часов. Хорошего дня!",
        f"{hour}:00, утро в самом разгаре."
    ]

    day_phrases = [
        f"И вот уже на часах {hour}:00 часов дня!",
        f"{hour} часов дня.",
        f"Уже {hour} часов, как день?",
        f"{hour}:00 часов в сто-о-лице!",
        f"{hour} часов, дневное время."
    ]

    evening_phrases = [
        f"Cейчас {hour} часов.",
        f"{hour}:00 часов вечера",
        f"Вечер, {hour} часов.",
        f"На часах {hour}:00, вечернее время.",
        f"{hour} часов вечера."
    ]

    night_phrases = [
        f"Ночное время, {hour} часов.",
        f"{hour} часов ночи, Москва не спит.",
        f"Сейчас {hour}:00, тихая ночь.",
        f"{hour} часов, глубокая ночь.",
        f"В Москве {hour}:00, ночное время."
    ]

    if 5 <= hour <= 11:
        return random.choice(morning_phrases)
    elif 12 <= hour <= 17:
        return random.choice(day_phrases)
    elif 18 <= hour <= 22:
        return random.choice(evening_phrases)
    else:
        return random.choice(night_phrases)

async def send_hourly_message():
    moscow_tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(moscow_tz)
    current_hour = now.hour

    message = generate_time_message(current_hour)
    logging.info(f"Отправка сообщения: {message}")

    for chat_id in chats["groups"]:
        try:
            await bot.send_message(chat_id=chat_id, text=message)
            logging.info(f"Сообщение отправлено в группу {chat_id}")
        except Exception as e:
            logging.error(f"Ошибка при отправке в группу {chat_id}: {e}")

    for chat_id in chats["channels"]:
        try:
            await bot.send_message(chat_id=chat_id, text=message)
            logging.info(f"Сообщение отправлено в канал {chat_id}")
        except Exception as e:
            logging.error(f"Ошибка при отправке в канал {chat_id}: {e}")

async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_hourly_message, 'cron', minute=0)
    scheduler.start()

    logging.info("Бот запущен и планировщик активен.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
