import asyncio
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.future import select
from datetime import datetime
from handlers import bot_msg, user_msg, dairy, timer
from callback import pagination
from config import config
from extensions import dbcreate
from images import send_images


# Создаем глобальный планировщик
scheduler = AsyncIOScheduler()


# Функция для проверки задач каждую минуту
async def check_tasks():
    async with dbcreate.async_session() as session:
        result = await session.execute(
            select(dbcreate.Task).where(dbcreate.Task.timer <= datetime.now())
        )
        tasks = result.scalars().all()
        
        if tasks:
            for task in tasks:
                try:
                    print(f"Напоминание о задаче: {task.inner_text}")
                    
                    # Удаляем задачу из базы данных
                    await session.delete(task)
                    
                except Exception as e:
                    print(f"Ошибка при обработке задачи {task.inner_text}: {e}")

            # Сохраняем изменения в базе данных
            await session.commit()



# Еженедельное напоминание
async def weekly_reminder(bot: Bot):
    async with dbcreate.async_session() as session:
        # Получаем всех пользователей из базы данных
        result = await session.execute(select(dbcreate.User))
        users = result.scalars().all()

        # Отправляем напоминание каждому пользователю
        for user in users:
            await send_images.send_random_image_and_text(bot, user.chat_id)
            print(f"Еженедельное напоминание для {user.id}")


# Функция для активации задач в планировщике для конкретного пользователя
async def activate_user_scheduler(chat_id):
    # Получаем задачи пользователя
    async with dbcreate.async_session() as session:
        result = await session.execute(
            select(dbcreate.Task).where(dbcreate.Task.user_id == chat_id)
        )
        tasks = result.scalars().all()
        
        for task in tasks:
            if task.timer > datetime.now():
                # Добавляем в планировщик
                scheduler.add_job(
                    check_tasks, 
                    trigger=IntervalTrigger(seconds=60),
                    id=f'task_reminder_{task.id}',
                    args=(chat_id, task.inner_text)
                )
            else:
                print(f"Задача с таймером {task.timer} не будет добавлена, так как она уже прошла.")

                

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
    scheduler.add_job(check_tasks, trigger=IntervalTrigger(seconds=60), id='check_tasks')
    # Запуск еженедельного напоминания
    scheduler.add_job(weekly_reminder, trigger='interval', weeks=1, id='weekly_reminder', args=(bot,))

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
