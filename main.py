import asyncio
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import config
from handlers import bot_msg, user_msg, dairy, timer
from callback import pagination
from scheduler.scheduler_task import check_tasks, weekly_reminder
from images import send_images


# Создаем глобальный планировщик
scheduler = AsyncIOScheduler()


# Основная асинхронная функция, в которой будет создаваться и настраиваться бот
async def main():
    bot = Bot(config.api_token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(
        send_images.router,
        timer.router,
        dairy.router,
        user_msg.router,
        pagination.router,
        bot_msg.router
    )

    # Запуск глобального планировщика
    scheduler.start()

    # Запускаем задачу проверки таймеров для пользователя каждую минуту
    scheduler.add_job(check_tasks, trigger='interval', seconds=60, id='check_tasks')
    # Запуск еженедельного напоминания
    scheduler.add_job(weekly_reminder, trigger='interval', weeks=1, id='weekly_reminder', args=(bot,))

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
