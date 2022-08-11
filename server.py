import asyncio
import datetime
from asyncio import subprocess

import aiofiles
from aiohttp import web

INTERVAL_SECS = 1


async def uptime_handler(request):
    response = web.StreamResponse()

    # Большинство браузеров не отрисовывают частично загруженный контент, только если это не HTML.
    # Поэтому отправляем клиенту именно HTML, указываем это в Content-Type.
    response.headers['Content-Type'] = 'text/html'

    # Отправляет клиенту HTTP заголовки
    await response.prepare(request)

    while True:
        formatted_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f'{formatted_date}<br>'  # <br> — HTML тег переноса строки

        # Отправляет клиенту очередную порцию ответа
        await response.write(message.encode('utf-8'))

        await asyncio.sleep(INTERVAL_SECS)


async def archive(request):
    response = web.StreamResponse()
    response.headers['Content-Disposition'] = 'attachment; filename="photos.zip"'
    program = 'zip'
    args = ['-', 'test_photos', '-r']
    bytes_portion = 100000
    archive_hash = request.match_info.get('archive_hash', 'unknown')

    await response.prepare(request)

    content = b''
    process = await asyncio.create_subprocess_exec(program, *args, stdout=subprocess.PIPE)

    while not process.stdout.at_eof():
        content = await process.stdout.read(n=bytes_portion)
        await response.write(content)

    return response


async def handle_index_page(request):
    async with aiofiles.open('index.html', mode='r') as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([
        web.get('/', handle_index_page),
        web.get('/archive/{archive_hash}/', archive),
    ])
    web.run_app(app)
