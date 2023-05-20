import os
import datetime

from aiogram import Bot
from aiogram.types import FSInputFile
from aiohttp import web
from flask import Flask, request, redirect, flash, url_for
from werkzeug.utils import secure_filename
from bot.admin_panel.GetTemplate import get_tmp
from bot.config import api_key
from bot.db import users, promocodes, Promocode
from bot.utils.is_number_float import is_number_float

app = Flask(__name__, static_folder="src/css")

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def get_users():
    content = {'title': 'Пользователи', 'users': []}
    for id in users:
        user = users.get(id)
        content['users'].append({'id': user.id,
                                 'username': user.username,
                                 'balance': user.balance,
                                 "referral_link": user.referral_link,
                                 "bonus_account": user.bonus_account,
                                 "status": user.status == 1})
    content['enumerate'] = enumerate

    return content


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/admin", methods=['GET', 'POST'])
async def hello():
    user_id = request.args.get("user_id")
    user_id_amount = request.args.get("balance")
    name_promocode = request.args.get("name_promocode")
    count_using = request.args.get("count_using")
    count_day = request.args.get("count_day")
    amount = request.args.get("amount")
    if user_id:
        user = users.get(int(user_id))
        if user:
            user.status = not user.status
            users.update_info(user)
        return redirect(request.path)

    elif user_id_amount:
        user_id, amount = user_id_amount.split(" ")
        user = users.get(int(user_id))
        if user:
            amount = is_number_float(amount)
            user.balance += amount
            users.update_info(user)
        return redirect(request.path)

    elif request.method == 'POST':
        message = request.values.get("message")
        if 'file' not in request.files and message is None:
            return redirect(request.path)

        file = request.files['file']
        if file.filename == '' and message is None:
            return redirect(request.path)
        bot = Bot(api_key, parse_mode="Markdown")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file.save(f"D:/telegram_bot/contract_bot/bot/admin_panel/photo/{filename}")
            file.close()
            photo = FSInputFile(f"D:/telegram_bot/contract_bot/bot/admin_panel/photo/{filename}")

            for id in users:
                await bot.send_photo(chat_id=id,
                                     caption=message,
                                     photo=photo)
        elif message:
            for id in users:
                # if id == 686171972:
                await bot.send_message(chat_id=id,
                                       text=message)
        return redirect(request.path)
    elif name_promocode and amount and count_using or name_promocode and amount and count_day:
        expiration_date = (datetime.datetime.now() + datetime.timedelta(days=int(count_day))).strftime("%d/%m/%Y")
        if count_using is None:
            count_using = 1000000
        elif count_day is None:
            count_day = 1000
        promocodes.add(Promocode(
            id=len(promocodes)+1,
            name=name_promocode,
            amount=float(amount),
            count_using=int(count_using),
            count_day=int(count_day),
            expiration_date=expiration_date
        ))

    content = get_users()
    return get_tmp("admin_panel.html", content)


if __name__ == "__main__":
    get_users()
