import asyncio
from aiogram import Router
from sqlalchemy.future import select
from datetime import datetime
from extensions import dbcreate
from images import send_images


async def check_tasks():
    async with dbcreate.async_session() as session:
        result = await session.execute(
            select(dbcreate.Task).where(dbcreate.Task.timer <= datetime.now())
        )
        tasks = result.scalars().all()

        if tasks:
            for task in tasks:
                try:
                    print(f'Напоминание о задаче: {task.inner_text}')

                    # Удаляем задачу из базы данных
                    await session.delete(task)

                except Exception as e:
                    print(f'Ошибка при обработке задачи {task.inner_text}: {e}')

            # Сохраняем изменения в базе данных
            await session.commit()


async def weekly_reminder(bot):
    async with dbcreate.async_session() as session:
        # Получаем всех пользователей из базы данных
        result = await session.execute(select(dbcreate.User))
        users = result.scalars().all()

        # Отправляем напоминание каждому пользователю
        for user in users:
            await send_images.send_random_image_and_text(bot, user.chat_id)
            print(f'Еженедельное напоминание для {user.id}')


async def activate_user_scheduler(scheduler, chat_id):
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
                    trigger='interval',
                    seconds=60,
                    id=f'task_reminder_{task.id}',
                    args=(chat_id, task.inner_text)
                )
            else:
                print(f'Задача с таймером {task.timer} не будет добавлена, так как она уже прошла.')
