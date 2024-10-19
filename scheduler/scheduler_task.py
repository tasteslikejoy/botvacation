from aiogram import Bot
from sqlalchemy.future import select
from datetime import datetime
from images import send_images
from extensions import dbcreate


# Функ ция отвечает за отправку сообщений
async def send_message(chat_id, text, bot: Bot):
    await bot.send_message(chat_id, text)


async def check_tasks(bot: Bot):
    # Асинхронный контекстный менеджер для создания сессии с базой данных
    async with dbcreate.async_session() as session:
        # Выбирает задачи из базы данных, у которых время меньше или равно текущему времени
        result = await session.execute(
            select(dbcreate.Task).where(dbcreate.Task.timer <= datetime.now())
        )
        tasks = result.scalars().all()

        if tasks:
            for task in tasks:
                try:
                    print(f'Напоминание о задаче: {task.inner_text}')

                    # Здесь выполняется запрос для нахождения пользователя по ID, связанному с задачей
                    # Если пользователь найден, он сохраняется в переменной user
                    user = await session.execute(
                        select(dbcreate.User).where(dbcreate.User.id == task.user_id)
                    )
                    user = user.scalar_one_or_none()

                    if user:
                        await send_message(user.chat_id, f'Напоминание о задаче: {task.inner_text}', bot)
                    else:
                        print(f'Пользователь с id {task.user_id} не найден')

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


async def activate_user_scheduler(scheduler, bot: Bot):
     # Используя контекстный менеджер, мы создаем асинхронную сессию для работы с базой данных через dbcreate
    async with dbcreate.async_session() as session:
        # Здесь мы выполняем SQL запрос для получения всех объектов Task из базы данных
        # scalars() используется для извлечения значений, а all() собирает их в список
        result = await session.execute(select(dbcreate.Task))
        tasks = result.scalars().all()

        for task in tasks:
            if task.timer > datetime.now():
                # Добавляем в планировщик
                scheduler.add_job(
                    check_tasks,
                    trigger='interval',
                    seconds=60,
                    args=[bot],
                    id=f'task_reminder_{task.id}'  # Уникальный ID для задачи
                )
            else:
                print(f'Задача с таймером {task.timer} не будет добавлена, так как она уже прошла.')
