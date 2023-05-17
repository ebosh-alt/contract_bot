import cgi
import os
import uuid

import aiofiles
import aiohttp
from aiohttp import web

from bot.admin_panel.GetTemplate import get_tmp
from bot.db import users
import aiohttp_jinja2
import jinja2
from aiofile import async_open

from bot.utils.is_number_float import is_number_float

app = web.Application()

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


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


async def save_file(request: aiohttp.web.Request) -> web.Response:
    # _, params = cgi.parse_header(request.headers['CONTENT-DISPOSITION'])
    # file_name = params['filename']
    file_path = f"D:/telegram_bot/contract_bot/bot/admin_panel/photo/file_name.png"

    async with async_open(file_path, 'bw') as afp:
        # https://docs.aiohttp.org/en/stable/streams.html#asynchronous-iteration-support
        # Выполняет итерацию по блокам данных в порядке их ввода в поток
        async for data in request.content.iter_any():
            await afp.write(data)

    # return web.Response(status=201, reason='OK', text="GOOD")


aiohttp_jinja2.setup(app,
                     loader=jinja2.FileSystemLoader("D:/telegram_bot/contract_bot/bot/admin_panel/src/templates"))


async def redirect_handler(path):
    return web.Response(status=302, headers={'location': path})


def get_attr(request):
    try:
        print(request.message.url)
        data = str(request.message.url).split("?")[1].split("=")
        return {
            data[0]: data[1]
        }
    except:
        return {}


routes = web.RouteTableDef()


# @aiohttp_jinja2.template('admin_panel.html')
@routes.post('/admin')
async def hello1(request: aiohttp.web.Request):
    content = get_users()
    print(request.content)
    await save_file(request)
    return web.Response(text=get_tmp("admin_panel.html", content),
                        content_type='text/html')


@routes.get('/admin')
async def hello(request: aiohttp.web.Request):
    data = get_attr(request)
    user_id = data.get("user_id")
    user_id_amount = data.get("balance")
    method = request.method

    if method == "GET":
        if user_id:
            user = users.get(int(user_id))
            if user:
                user.status = not user.status
                users.update_info(user)
            raise web.HTTPFound(request.path)
        elif user_id_amount:
            user_id, amount = user_id_amount.split("+")
            user = users.get(int(user_id))
            if user:
                amount = is_number_float(amount)
                user.balance += amount
                users.update_info(user)
            raise web.HTTPFound(request.path)

        else:
            print(100)
            await save_file(request)
            # f = await aiofiles.open('file.img', mode='wb+')
            # await f.write(await request.read())
            # await f.close()
    # if request.method == 'POST':
    # print(request.message)
    # raise web.HTTPFound(request.path)

    #     message = request.values.get("message")
    #     if 'file' not in request.files and message is None:
    #         return redirect(request.path)
    #
    #     file = request.files['file']
    #     if file.filename == '' and message is None:
    #         return redirect(request.path)
    #     bot = Bot(api_key, parse_mode="Markdown")
    #
    #     if file and allowed_file(file.filename):
    #         filename = secure_filename(file.filename)
    #
    #         file.save(f"D:/telegram_bot/contract_bot/bot/admin_panel/photo/{filename}")
    #         file.close()
    #         # with open(f"D:/telegram_bot/contract_bot/bot/admin_panel/photo/{filename}", "rb") as f:
    #         #     photo = f.read()
    #         # photo = InputFile(f"D:/telegram_bot/contract_bot/bot/admin_panel/photo/{filename}")
    #         photo = FSInputFile(f"D:/telegram_bot/contract_bot/bot/admin_panel/photo/{filename}")
    #
    #         for id in users:
    #
    #             if id == 686171972:
    #                 await bot.send_photo(chat_id=id,
    #                                      caption=message,
    #                                      photo=photo)
    #     elif message:
    #         for id in users:
    #             if id == 686171972:
    #                 await bot.send_message(chat_id=id,
    #                                        text=message)
    #     return redirect(request.path)
    #
    # content = get_users()
    # return get_tmp("admin_panel.html", content)
    content = get_users()
    return web.Response(text=get_tmp("admin_panel.html", content),
                        content_type='text/html')


# app.router.add_get("/admin", hello)
app.router.add_routes(routes)

if __name__ == "__main__":
    get_users()
