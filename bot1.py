import config
import logging
from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter
import schedule
import time
from threading import Thread
from sqlighter import SQLighter


def remind():
    print("time is working")
    db = SQLighter('db.db')

    def timer():
        db.new_day()

    schedule.every().day.at("23:59:59").do(timer)
    while True:
        schedule.run_pending()
        time.sleep(1)


th = Thread(target=remind, args=())
th.start()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)
db = SQLighter('db.db')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    first_name = message.from_user.first_name
    await message.answer((f"Hi {first_name}, nice to meet you! "))


@dp.message_handler(commands=['pencil'])
async def pencil(message: types.Message):
    hours = int(time.strftime('%H'))
    minutes = int(time.strftime('%M'))
    ohours = 23
    ominutes = 60
    h = ohours - hours
    m = ominutes - minutes
    first_name = message.from_user.username
    if (not db.subscriber_exists(message.from_user.id, message.chat.id)):
        import random
        ran = random.randint(1, 10)
        day2 = 2
        ran1 = str(ran)

        user_name = message.from_user.first_name
        chat1 = message.chat.id
        db.add_subscriber(
        message.from_user.id,
        first_name=user_name, 
        status=ran, 
        chat_id=chat1
        )
        db.update_day(message.chat.id, message.from_user.id, day_id=day2)
        await message.reply(
            f"@{first_name}, приветствую в игре.\nТвой pencil увеличился на " + ran1 
            + " см.\nСейчас твой pencil " + ran1 + " см.\n" + f"Сыграй через {h} ч. и {m} мин.")
    else:
        import random
        day = str(db.day(message.chat.id, message.from_user.id))
        day1 = int((day)[2:-3])
        if day1 == 1:
            sm1 = str(db.get_subscriptions(message.from_user.id, message.chat.id))
            sm = (sm1)[2:-3]
            day2 = 2
            if int(sm) <= 0:
                ran = random.randint(1, 10)
                ran1 = str(ran)
                sm2 = int(sm) + int(ran)
                sm3 = str(sm2)
                db.update_day(message.chat.id, message.from_user.id, day_id=day2)
                db.update_subscription(message.from_user.id, message.chat.id, status=ran)
                await message.reply(
                    f"@{first_name}, твой pencil увеличился на " + ran1 
                    + " см.\nСейчас твой pencil " + sm3 + " см.\n" + f"Сыграй через {h} ч. и {m} мин.")
            else:
                ran = random.randint(-10, 10)
                ran1 = str(ran)
                sm2 = int(sm) + int(ran)
                sm3 = str(sm2)
                db.update_day(message.chat.id, message.from_user.id, day_id=day2)
                if sm2 <= 0:
                    ran = 0
                    db.update_subscription(message.from_user.id, message.chat.id, status=ran)
                    await message.reply(
                        f"@{first_name}, твой pencil уменьшился на " + ran1 
                        + " см.\nСейчас у тебя нет pencil...\n" + f"Сыграй через {h} ч. и {m} мин.")
                else:
                    sm1 = str(db.get_subscriptions(message.from_user.id, message.chat.id))
                    sm = (sm1)[2:-3]
                    db.update_subscription(message.from_user.id, message.chat.id, status=sm3)

                    if ran > 0:
                        await message.reply(
                            f"@{first_name}, твой pencil увеличился на " + ran1
                            + " см.\nСейчас твой pencil " + sm3 + " см.\n" + f"Сыграй через {h} ч. и {m} мин.")
                    if ran < 0:
                        ran1 = (ran1)[1:]
                        await message.reply(
                            f"@{first_name}, твой pencil уменьшился на " + ran1 
                            + " см.\nСейчас твой pencil " + sm3 + " см.\n" + f"Сыграй через {h} ч. и {m} мин.")
                    if ran == 0:
                        await message.reply(
                            f"@{first_name}, твой pencil не изменился. " + "\nСейчас твой pencil " 
                            + sm3 + " см.\n" + f"Сыграй через {h} ч. и {m} мин.")
        if day1 == 2:
            await message.reply(f"@{first_name}, ты уже играл...\n" + f"Сыграй через {h} ч. и {m} мин.")


@dp.message_handler(commands=['all'])
async def all(message: types.Message):
    all = db.get_all(message.chat.id)
    al = '\n' + "\n"
    is1 = 0
    for i in list(all):
        is1 = is1 + 1
        al = al + str(is1) + '. ' + str(i).replace('(', '').replace(')', '').replace("'", '').replace("'", '') + ' sm;' '\n'
    await message.reply('All pencils: ' + al)


@dp.message_handler(commands=['top10'])
async def top10(message: types.Message):
    all1 = db.get_top(message.chat.id)
    al1 = '\n' + "\n"
    iss = 0
    for i1 in list(all1[0:10]):
        iss = iss + 1
        al1 = al1 + str(iss) + '. ' + str(i1).replace('(', '').replace(')', '').replace("'", '').replace("'", '') + ' sm;' '\n'
    await message.reply('Tоп 10 pencils: ' + al1)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
