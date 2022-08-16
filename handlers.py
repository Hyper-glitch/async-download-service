"""Module for microservice handlers."""
import os
from pathlib import PurePath

import aiofiles
from aiohttp import web
from aiohttp.abc import Request, StreamResponse


async def handle_cwd_exists(request: Request, cwd: PurePath) -> None:
    """Check that archive exists or not.

    Args:
        request: request from client that trigger this endpoint.
        cwd: current work directory.
    Raises:
        HTTPNotFound: if the archive does not exist or has been deleted.
    """
    if not os.path.exists(cwd):
        raise web.HTTPNotFound(text='The archive does not exist or has been deleted.')


async def handle_cwd_name(request: Request, archive_hash: str) -> None:
    """Check the name of dir, that will be archived.

    Args:
        request: request from client that trigger this endpoint.
        archive_hash: name of archive hash.
    Raises:
        HTTPNotImplemented: because can't archive directory with name '.' or '..'
    """
    if archive_hash == '.' or archive_hash == '..':
        raise web.HTTPNotImplemented(text='Архив с катологом "." или ".." не может быть создан.')


async def handle_index_page(request: Request) -> StreamResponse:
    """Open and return response with html content.

    Args:
        request: request from client that trigger this endpoint.
    Returns:
        response: response with content from a server.
    """
    async with aiofiles.open('index.html', mode='r') as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')
