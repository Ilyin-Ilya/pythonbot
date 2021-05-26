from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
import datetime
import time
from main import cnx
from States import Test
from choice_buttons import keyboard2, keyboard, keyboard3
from main import bot, dp
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove


@dp.message_handler(Command("start"), state=None)
async def echo(message: Message):
    await message.answer(text="Hello. Available actions: ", reply_markup=keyboard)
    await Test.action_state.set()


@dp.message_handler(state=Test.action_state)
async def answer_q1(message: Message, state: FSMContext):
    act = message.text
    if act == "Cancel":
        await message.answer("Спасибо, до свидания", reply_markup=ReplyKeyboardRemove())
        await state.finish()
    else:
        await state.update_data(action_made=act)

        await message.answer("Отлично! Выберите специализацию врача:", reply_markup=keyboard2)

        await Test.specialization_state.set()


@dp.message_handler(state=Test.specialization_state)
async def answer_q2(message: Message, state: FSMContext):
    # Достаем переменные
    specialization_ = message.text

    await state.update_data(specialization_selected=specialization_)
    if specialization_ == "Cancel":
        await message.answer("Спасибо, до свидания", reply_markup=ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.answer("Пора выбрать ФИО врача: ", reply_markup=keyboard3)
        await Test.doctor_select_state.set()


@dp.message_handler(state=Test.doctor_select_state)
async def answer_q3(message: Message, state: FSMContext):
    # Достаем переменные
    text = message.text
    if text == "Cancel":
        await message.answer("Спасибо, до свидания", reply_markup=ReplyKeyboardRemove())
        await state.finish()

    doctor_id = int(text.split(".")[0])

    await state.update_data(doctor_id=doctor_id)
    data = await state.get_data()
    cursor = cnx.cursor()


    if data.get("action_made") == "View appointments":
        sql = "SELECT doctor.doctor_name, doctor_surname, client_name, client_surname, date \
              FROM doctor inner join appointment \
              where doctor.type_id = doctor_id and \
              doctor_id = %s"
        val = (doctor_id,)
        cursor.execute(sql, val)
        ress = cursor.fetchall()
        for res in ress:
            await message.reply("Doctor " + res[0]+ " "+ res[1]+ "\nClient " + res[2] + " "
                                 + res[3] + "\nTime: "+ res[4].strftime("%Y-%m-%d %H:%M:%S"),reply_markup=ReplyKeyboardRemove())

        await state.finish()

    elif data.get("action_made") == "Make an appointment":
        sql = "insert into appointment(`doctor_id`,`client_name`,`client_surname`,`date`)\
        values( %s, %s, %s, CURRENT_TIMESTAMP())"
        val = (doctor_id,message.from_user.first_name,message.from_user.last_name,)
        cursor.execute(sql, val)
        cnx.commit()
        await message.reply("Получилось! Увидимся на приеме!",reply_markup=ReplyKeyboardRemove())
        await state.finish()