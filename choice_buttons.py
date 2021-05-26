from main import cnx
from Doctor import Doctor

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
cursor = cnx.cursor()

##firstState
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ["Make an appointment"]
keyboard.add(*buttons)
buttons2=["View appointments","Cancel"]
keyboard.add(*buttons2)

##secondState
keyboard2 = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard2.add(*["Therapy"],*["Surgery"],*["Dentistry"], *["Cancel"])

##GetAllDoctors
def getAllDoctors():
    sql = "select * from doctor"
    cursor.execute(sql)
    doctors = cursor.fetchall()
    return doctors

keyboard3 = ReplyKeyboardMarkup(resize_keyboard=True)
doctors = getAllDoctors()
for doctor in doctors:
    print(doctor)
    keyboard3.add(*[str(doctor[0]) +". " + doctor[1] +" " +doctor[2]])

keyboard3.add(*["Cancel"])

