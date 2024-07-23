import asyncio
from env import TOKEN, MyGnewsKey
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import json
import random
import urllib.request
from googletrans import Translator

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()  # Создание экземпляра класса Translator для перевода текста


def get_news(tema):
    text = translator.translate(tema.strip().split()[0], dest='en').text

    url = f"https://gnews.io/api/v4/top-headlines?q={text}&lang=ru&country=RU&max=10&apikey={MyGnewsKey}"
    print(f"{url}")
    with (urllib.request.urlopen(url) as response):
        data = json.loads(response.read().decode("utf-8"))
        articles = data["articles"]
        k = random.randint(0, len(articles) - 1)
        if k == 0:
            return None

        title = articles[k]['title']
        content = articles[k]['content']
        source1 = articles[k]['source']['name']
        source2 = articles[k]['url']
    return title, content, source1, source2


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}\n"
                         f"Я могу найти для тебя свежую новость в интернете.\n"
                         f"Напиши мне тему для поиска одним словом.")


@dp.message()
async def send_news(message: Message):
    news = get_news(message.text)
    if news is None:
        await message.answer("Ничего не нашлось. Попробуйте еще раз.")
    else:
        title, content, source1, source2 = news
        await message.answer(f"Источник информации: {source1}\n\"{title}\"\n{source2}\n{content}")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
