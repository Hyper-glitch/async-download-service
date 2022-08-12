"""Module for handlers."""
import os

import aiofiles
from aiohttp import web


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
