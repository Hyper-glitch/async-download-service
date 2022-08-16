"""The main module for run the server."""
import argparse
import asyncio
import logging
from pathlib import PurePath

from aiohttp import web, ClientConnectionError
from aiohttp.abc import StreamResponse, Request

from handlers import handle_index_page, handle_cwd_name, handle_cwd_exists
from settings import RESPONSE_DELAY, ENABLE_LOGGING, PHOTOS_DIR


async def archive(request: Request) -> StreamResponse:
    """Archive files in stream and send it to the client side.

    Args:
        request: request from client that trigger this endpoint.
    Raises:
        HTTPRequestTimeout: if request timed out.
        ClientConnectionError: if client connection lost.
        HTTPNotFound: if archive_hash does not exist in url scheme.
    Returns:
        response: response with content from a server.
    """
    program = 'zip'
    bytes_portion = 100000
    archive_name = 'photos.zip'
    archive_hash = request.match_info['archive_hash']

    cwd = PurePath(PHOTOS_DIR, archive_hash)
    args = ['-r', '-', '.', '-i', '*', ]

    await handle_cwd_name(request, archive_hash=archive_hash)
    await handle_cwd_exists(request, cwd=cwd)

    response = web.StreamResponse()
    response.headers['Content-Disposition'] = f'attachment; filename="{archive_name}"'

    await response.prepare(request)
    process = await asyncio.create_subprocess_exec(program, *args, stdout=asyncio.subprocess.PIPE, cwd=cwd)

    try:
        while not process.stdout.at_eof():
            logging.info('Sending archive chunk ...')
            content = await process.stdout.read(n=bytes_portion)
            await response.write(content)

            if RESPONSE_DELAY:
                await asyncio.sleep(RESPONSE_DELAY)

    except (web.HTTPRequestTimeout, ClientConnectionError, asyncio.CancelledError) as exc:
        logging.error('Download was interrupted: ', exc.text)
        raise exc
    finally:
        if process.returncode is None:
            process.kill()
            await process.communicate()

    return response


def create_parser() -> argparse.Namespace:
    """Create arg parser and add arguments.

    Returns:
        namespace: values or arguments, that parsed.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-H', '--hostname', help='TCP/IP hostname to serve on (default: %(default)r)', default='localhost',
    )
    parser.add_argument(
        '-P', '--port', help='TCP/IP port to serve on (default: %(default)r)', type=int, default='8080',
    )
    return parser.parse_args()


def main() -> None:
    """Main function that set up logging, add arg parser and create and run the server.

    Returns:
        None
    """
    if ENABLE_LOGGING:
        logging.basicConfig(
            format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO,
        )
    args = create_parser()
    app = web.Application()
    app.add_routes([
        web.get('/', handle_index_page),
        web.get('/archive/{archive_hash}/', archive),
    ])
    web.run_app(app=app, host=args.hostname, port=args.port)


if __name__ == '__main__':
    main()
