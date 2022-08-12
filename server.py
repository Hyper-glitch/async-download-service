import asyncio
import os
from asyncio import subprocess

import aiofiles
from aiohttp import web

INTERVAL_SECS = 1


async def archive(request):
    program = 'zip'
    bytes_portion = 100000
    archive_name = 'photos.zip'
    archive_hash = request.match_info.get('archive_hash')
    cwd = f'test_photos/{archive_hash}'
    args = ['-r', '-', '.', '-i', '*', ]

    await handler_cwd_name(request, archive_hash)
    await handler_cwd_exists(request, cwd=cwd)

    response = web.StreamResponse()
    response.headers['Content-Disposition'] = f'attachment; filename="{archive_name}"'

    await response.prepare(request)
    process = await asyncio.create_subprocess_exec(program, *args, stdout=subprocess.PIPE, cwd=cwd)

    while not process.stdout.at_eof():
        content = await process.stdout.read(n=bytes_portion)
        await response.write(content)

    return response


async def handle_cwd_exists(request, cwd):
    if not os.path.exists(cwd):
        raise web.HTTPNotFound(text='Архив не существует или был удален.')


async def handle_cwd_name(request, archive_hash):
    if archive_hash == '.' or archive_hash == '..':
        raise web.HTTPNotImplemented(text='Архив с катологом "." или ".." не может быть создан.')


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
