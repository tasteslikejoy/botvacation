import os
import random
from aiogram import Bot
from aiogram import Router


# Папка с изображениями
IMAGE_FOLDER = os.path.abspath('images/images_to_send/image.txt')
# Путь к текстовому файлу
TEXT_FILE = os.path.abspath('images/text/text.txt')


# Читает файл с изображениями, заполняет список ссылками и возвращает случайную ссылку
def get_random_image():
    try:
        with open(IMAGE_FOLDER, 'r', encoding='utf-8') as file:
            urls = file.readlines()
        if not urls:
            raise ValueError('Файл с изображениями пуст.')
        return random.choice(urls).strip()
    except Exception as e:
        print(f'Ошибка при получении случайного изображения: {e}')
        return None

# Аналогична функции для изображений, но работает с текстовым файлом
def get_random_text():
    try:
        with open(TEXT_FILE, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        if not lines:
            raise ValueError('Текстовый файл пуст.')
        return random.choice(lines).strip()
    except Exception as e:
        print(f'Ошибка при получении случайного текста: {e}')
        return None

# Эта функция принимает объект бота bot и идентификатор пользователя user
# Получает случайное изображение и текст
# Если всё успешно, отправляет сообщение с изображением и текстом пользователю
async def send_random_image_and_text(bot: Bot, user: int):
    image_path = get_random_image()
    random_text = get_random_text()

    if image_path is None:
        return 'Извините, не удалось найти изображение.'

    if random_text is None:
        return 'Извините, не удалось получить текст.'

    try:
        await bot.send_photo(user, photo=image_path, caption=random_text)
    except Exception as e:
        return f'Ошибка при отправке сообщения: {e}'