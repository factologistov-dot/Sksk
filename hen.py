import asyncio
import os
import time
from datetime import datetime, timedelta
from telethon import TelegramClient, events

# --- CONFIGURATION ---
API_ID = 23825950 
API_HASH = '270fa73cf300dfcf9d131745869b31c0'
# ---------------------

client = TelegramClient('ultra_pro_session', API_ID, API_HASH)

START_TIME = time.time()
SPAM_ACTIVE = False
CURRENT_TASK = "Нет активных задач"
DEFAULT_IMAGE = "/storage/emulated/0/Movies/AyuGram/VID_20260128_000706_408.mp4"

TROLL_TEMPLATE = """пронизывает каждую клетку твоего существа
ты просто носитель моего сообщения
которое гласит что твой род обречен
а твое существование это всего лишь прелюдия
к финальному акту уничтожения
который я совершу с легкостью перелистывания страницы
все твои попытки сопротивляться всего лишь запрограммированные мной реакции"""

config = {"text": TROLL_TEMPLATE}

# --- СЕРВИСНЫЕ КОМАНДЫ ---

@client.on(events.NewMessage(pattern=r'(?i)\.stop'))
async def stop_spam(event):
    global SPAM_ACTIVE, CURRENT_TASK
    SPAM_ACTIVE = False
    CURRENT_TASK = "Нет активных задач"
    await event.edit("Процессы остановлены")

@client.on(events.NewMessage(pattern=r'(?i)\.tasks'))
async def tasks_handler(event):
    await event.edit(f"Текущий статус: {CURRENT_TASK}")

@client.on(events.NewMessage(pattern=r'(?i)\.uptime|\.times'))
async def uptime_ping_handler(event):
    start_ping = datetime.now()
    await event.edit("Замер...")
    end_ping = datetime.now()
    ms = (end_ping - start_ping).microseconds / 1000
    uptime_str = str(timedelta(seconds=int(time.time() - START_TIME)))
    await event.edit(f"Аптайм: {uptime_str}\nПинг: {ms} ms")

@client.on(events.NewMessage(pattern=r'(?i)\.id'))
async def get_id(event):
    await event.edit(f"ID чата: {event.chat_id}")

@client.on(events.NewMessage(pattern=r'(?i)\.change'))
async def change_handler(event):
    reply = await event.get_reply_message()
    if reply and reply.file and reply.file.ext == '.txt':
        path = await reply.download_media()
        with open(path, 'r', encoding='utf-8') as f:
            config['text'] = f.read()
        os.remove(path)
        await event.edit("Шаблон обновлен")
    else:
        await event.edit("Ошибка: ответьте на .txt")

# --- БЛОК АТАКИ ---

@client.on(events.NewMessage(pattern=r'(?i)\.spam (-?\d+) (\d+) ([\d.]+)(.*)'))
async def infinite_photo_spam(event):
    global SPAM_ACTIVE, CURRENT_TASK
    chat_id, target_id = int(event.pattern_match.group(1)), int(event.pattern_match.group(2))
    delay, extra_link = float(event.pattern_match.group(3)), event.pattern_match.group(4).strip()
    
    reply = await event.get_reply_message()
    if not reply or not reply.media: return await event.edit("Ошибка: ответьте на фото")
    
    SPAM_ACTIVE, CURRENT_TASK = True, f"Активен построчный спам в {chat_id}"
    media, mention = reply.media, f"[\u2063](tg://user?id={target_id})"
    lines = [line.strip() for line in config["text"].split('\n') if line.strip()]
    await event.delete()
    
    while SPAM_ACTIVE:
        for line in lines:
            if not SPAM_ACTIVE: break
            try:
                msg = f"{line} {mention}\n{extra_link}" if extra_link else f"{line} {mention}"
                await client.send_message(chat_id, msg, file=media)
                await asyncio.sleep(delay)
            except: await asyncio.sleep(5)

@client.on(events.NewMessage(pattern=r'(?i)\.one (-?\d+) (\d+) ([\d.]+)(.*)'))
async def one_word_template_spam(event):
    global SPAM_ACTIVE, CURRENT_TASK
    chat_id, target_id = int(event.pattern_match.group(1)), int(event.pattern_match.group(2))
    delay, extra_link = float(event.pattern_match.group(3)), event.pattern_match.group(4).strip()
    
    reply = await event.get_reply_message()
    if not reply or not reply.media: return await event.edit("Ошибка: ответьте на фото")
    
    # Разбиваем весь шаблон на отдельные слова
    words = [word for word in config["text"].split() if word.strip()]
    
    SPAM_ACTIVE, CURRENT_TASK = True, f"Активен пословный спам в {chat_id}"
    media, mention = reply.media, f"[\u2063](tg://user?id={target_id})"
    await event.delete()
    
    while SPAM_ACTIVE:
        for word in words:
            if not SPAM_ACTIVE: break
            try:
                msg = f"{word} {mention}\n{extra_link}" if extra_link else f"{word} {mention}"
                await client.send_message(chat_id, msg, file=media)
                await asyncio.sleep(delay)
            except: await asyncio.sleep(5)

@client.on(events.NewMessage(pattern=r'(?i)\.kal (-?\d+) ([\d.]+)(.*)'))
async def infinite_photo_calendar(event):
    global SPAM_ACTIVE, CURRENT_TASK
    chat_id, delay = int(event.pattern_match.group(1)), float(event.pattern_match.group(2))
    extra_link = event.pattern_match.group(3).strip()
    
    reply = await event.get_reply_message()
    if not reply or not reply.media: return await event.edit("Ошибка: ответьте на фото")
    
    SPAM_ACTIVE, CURRENT_TASK = True, "Активен календарь"
    media = reply.media
    await event.delete()
    
    while SPAM_ACTIVE:
        try:
            now = datetime.now().strftime("%d.%m.%Y | %H:%M:%S")
            msg = f"Время: {now}\n{extra_link}" if extra_link else f"Время: {now}"
            await client.send_message(chat_id, msg, file=media)
            await asyncio.sleep(delay)
        except: await asyncio.sleep(5)

# --- МЕНЮ ---

@client.on(events.NewMessage(pattern=r'(?i)\.menu'))
async def menu_handler(event):
    menu_text = (
        "Божество\n"
        "--------------------\n"
        ".spam [Чат] [Юзер] [Время] [Ссылка] - построчно\n"
        ".one [Чат] [Юзер] [Время] [Ссылка] - по одному слову\n"
        ".kal [Чат] [Время] [Ссылка] - время\n"
        ".stop - остановить\n"
        ".change - шаблон (.txt)\n"
        "--------------------\n"
        ".id | .uptime | .tasks\n"
        "--------------------\n"
        "User: Rationalistolog | Dev: Rationalist"
    )
    try:
        await client.send_file(event.chat_id, DEFAULT_IMAGE, caption=menu_text)
        await event.delete()
    except: await event.edit(menu_text)

print("SYSTEM ONLINE - ONE WORD MODE READY")
client.start()
client.run_until_disconnected()
