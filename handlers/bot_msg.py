import random
from aiogram import Router
from aiogram.types import Message
from keyboards import reply, fabrics
from data.subloader import get_json


router = Router()


# Декоратор указывает, что данная функция будет обрабатывать входящие сообщения
@router.message()
# Это асинхронная функция, которая принимает объект message типа Message, представляющий сообщение, полученное ботом
async def msg(message: Message):
    msg = message.text.lower() # Получаем текст сообщения и приводим его к нижнему регистру для упрощения обработки
    bags = await get_json('bags.json') # Здесь вызывается асинхронная функция get_json() для загрузки различных файлов JSON
    cloth = await get_json('cloth.json')
    cosmetics = await get_json('cosmetics.json')
    electronic_equipment = await get_json('electronic_equipment.json')
    medicines = await get_json('medicines.json')
    random_fact = await get_json('random.json')

    # Проверяем, совпадает ли текст сообщения с ключевым словом "отпуск"
    if msg == 'отпуск':
        # Если условие выполняется, бот отправляет пользователю сообщение с текстом и прикрепляет к нему клавиатуру
        await message.answer('Отлично! Давайте скорее соберем вещи!', reply_markup=reply.vacation_kb)
    elif msg == 'ежедневник':
        await message.answer('Ничего не забудьте!', reply_markup=reply.dairy_kb)
    elif msg == 'назад':
        await message.answer('Главное меню', reply_markup=reply.main_kb)
    elif msg == 'предупредить начальство':
        await message.answer('Давай создадим задачу и я о ней напомню!', reply_markup=reply.call_timer_kb)
    elif msg == 'начать отсчет':
        await message.answer(f'Как здорово, {message.from_user.username}! '
                             f'Когда планируем отдыхать?', reply_markup=reply.call_vacation_kb)
    elif msg == 'собрать вещи':
        await message.answer('Отлично! Давай приступим!', reply_markup=reply.bags_kb)
    elif msg == 'документы':
        await message.answer(f'{bags[0][0]} {bags[0][1]}', reply_markup=fabrics.pag_bags(0))
        if bags:
            await message.answer('Подсказка: '
                                 'Некоторые документы можно отсканировать!', reply_markup=reply.bags_kb)
    elif msg == 'одежда':
        await message.answer(f'{cloth[0][0]} {cloth[0][1]}', reply_markup=fabrics.pag_cloth(0))
        if cloth:
            await message.answer('Подсказка: '
                                 'Головной убор очень важен!\n'
                                 'Для холодных стиран не забудьте термобелье!', reply_markup=reply.bags_kb)
    elif msg == 'косметика':
        await message.answer(f'{cosmetics[0][0]} {cosmetics[0][1]}', reply_markup=fabrics.pag_cosmetics(0))
        if cosmetics:
            await message.answer('Подсказка: '
                                 'Убедитесь, что такие объемы жидкости можно провозить!', reply_markup=reply.bags_kb)
    elif msg == 'лекарства':
        await message.answer(f'{medicines[0][0]} {medicines[0][1]}', reply_markup=fabrics.pag_medicine(0))
        if medicines:
            await message.answer('Подсказка: '
                                 'Не забывайте заботиться о своем пищеварении!', reply_markup=reply.bags_kb)
    elif msg == 'техника':
        await message.answer(f'{electronic_equipment[0][0]} {electronic_equipment[0][1]}', reply_markup=fabrics.pag_electronic(0))
        if electronic_equipment:
            await message.answer('Подсказка: '
                                 'Проверь наличие всех проводов для зарядки своих устройств. '
                                 'Их может не хватить!', reply_markup=reply.bags_kb)
    elif msg == 'интересный факт':
        fact = random.choice(random_fact)
        await message.answer(f'{fact}', reply_markup=reply.main_kb)


