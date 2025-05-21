import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from openai import OpenAI

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация
TELEGRAM_BOT_TOKEN = "7555374568:AAGXG4EV_KGiTD56o2a5IoQ-5BZIZHc16Kc"
OPENROUTER_API_KEY = "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"
MODEL = "mistralai/mistral-7b-instruct"  # Хорошо работает с русским

# Инициализация
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# Системный промт для точных ответов
SYSTEM_PROMPT = """Ты профессиональный бизнес-консультант по юридическим вопросам. 
Давай четкие, конкретные и краткие ответы на русском языке. 
Отвечай только по существу, без лишних слов."""

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "🟢 Юридический бизнес-ассистент\n\n"
        "Задайте вопрос о регистрации бизнеса, налогах, договорах или других юридических аспектах.\n"
        "Примеры вопросов:\n"
        "• Как зарегистрировать ИП?\n"
        "• Какие налоги у ООО?\n"
        "• Нужен ли договор с фрилансером?"
    )

@dp.message()
async def handle_message(message: Message):
    try:
        # Показываем статус "печатает"
        await bot.send_chat_action(message.chat.id, "typing")
        
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://t.me/",
                "X-Title": "Legal Business Assistant",
            },
            model=MODEL,
            temperature=0.3,  # Для более предсказуемых ответов
            max_tokens=500,   # Ограничение длины ответа
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text}
            ]
        )
        
        # Чистка и форматирование ответа
        response = completion.choices[0].message.content
        response = response.strip()  # Удаляем лишние пробелы
        response = response.split('\n')[0]  # Берем первый абзац если ответ длинный
        
        await message.answer(response)
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await message.answer("🔴 Ошибка обработки. Повторите вопрос короче.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())