import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Ваши API-ключи
TELEGRAM_TOKEN = '7937440891:AAGXWZtmbz_lT0dIAbTUWke7bDENZB9rvAY'
OPENWEATHERMAP_API_KEY = '08a6b6c3c821e8252575926f0b9782b1'

def get_weather() -> str:
    """Получает данные о погоде в Саратове с OpenWeatherMap и возвращает их в виде строки."""
    city = 'Saratov'
    url = (f'http://api.openweathermap.org/data/2.5/weather?q={city}'
           f'&appid={OPENWEATHERMAP_API_KEY}&units=metric&lang=ru')
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        description = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        weather_report = (
            f"Погода в Саратове:\n"
            f"{description.capitalize()}\n"
            f"Температура: {temp}°C\n"
            f"Влажность: {humidity}%\n"
            f"Скорость ветра: {wind_speed} м/с"
        )
        return weather_report
    except Exception as e:
        logger.error(f"Ошибка при получении погоды: {e}")
        return "Не удалось получить данные о погоде. Попробуйте позже."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start."""
    await update.message.reply_text('Привет! Отправь команду /weather, чтобы узнать погоду в Саратове.')

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /weather."""
    weather_info = get_weather()
    await update.message.reply_text(weather_info)

def main() -> None:
    """Запуск бота с использованием нового API."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("weather", weather))

    application.run_polling()

if __name__ == '__main__':
    main()
