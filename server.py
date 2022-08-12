import asyncio
import logging
from asyncio import subprocess
from pathlib import PurePath

from aiohttp import web, ClientConnectionError

from handlers import handle_index_page, handle_cwd_name, handle_cwd_exists
from settings import RESPONSE_DELAY, ENABLE_LOGGING, PHOTOS_DIR


async def archive(request):
    program = 'zip'
    bytes_portion = 100000
    archive_name = 'photos.zip'
    archive_hash = request.match_info.get('archive_hash')

    cwd = PurePath(PHOTOS_DIR, archive_hash)
    args = ['-r', '-', '.', '-i', '*', ]

    await handle_cwd_name(request, archive_hash)
    await handle_cwd_exists(request, cwd=cwd)

    response = web.StreamResponse()
    response.headers['Content-Disposition'] = f'attachment; filename="{archive_name}"'

    await response.prepare(request)
    process = await asyncio.create_subprocess_exec(program, *args, stdout=subprocess.PIPE, cwd=cwd)

    try:
        while not process.stdout.at_eof():
            logging.info('Sending archive chunk ...')
            content = await process.stdout.read(n=bytes_portion)
            await response.write(content)
            await asyncio.sleep(RESPONSE_DELAY)
    except (web.HTTPRequestTimeout, ClientConnectionError) as exc:
        logging.error('Download was interrupted: ', exc.text)
        raise exc
    finally:
        await process.communicate()

    return response


def main():
    if ENABLE_LOGGING:
        logging.basicConfig(
            format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO,
        )
    app = web.Application()
    app.add_routes([
        web.get('/', handle_index_page),
        web.get('/archive/{archive_hash}/', archive),
    ])
    web.run_app(app)


if __name__ == '__main__':
    main()
