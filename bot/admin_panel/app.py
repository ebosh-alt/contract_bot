import os

from aiogram import Bot
from aiogram.types import FSInputFile
from aiohttp import web
from flask import Flask, request, redirect, flash, url_for
from werkzeug.utils import secure_filename
from bot.admin_panel.GetTemplate import get_tmp
from bot.config import api_key
from bot.db import users
from bot.utils.is_number_float import is_number_float

# app = Flask(__name__, static_folder="src/css")
app = web.Application()


def setup_routes(app):
    app.router.add_get("/admin", hello)


UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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


# @app.router("/")
def helwlo():
    return "HELLO"


# @app.router("/login")
def login():
    return "login"


# @app.router("/admin", methods=['GET', 'POST'])
async def hello():
    user_id = request.args.get("user_id")
    user_id_amount = request.args.get("balance")
    # photo = request.args.get("file")
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

    if request.method == 'POST':
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
            # with open(f"D:/telegram_bot/contract_bot/bot/admin_panel/photo/{filename}", "rb") as f:
            #     photo = f.read()
            # photo = InputFile(f"D:/telegram_bot/contract_bot/bot/admin_panel/photo/{filename}")
            photo = FSInputFile(f"D:/telegram_bot/contract_bot/bot/admin_panel/photo/{filename}")

            for id in users:

                if id == 686171972:
                    await bot.send_photo(chat_id=id,
                                         caption=message,
                                         photo=photo)
        elif message:
            for id in users:
                if id == 686171972:
                    await bot.send_message(chat_id=id,
                                           text=message)
        return redirect(request.path)

    content = get_users()
    return get_tmp("admin_panel.html", content)


if __name__ == "__main__":
    get_users()
