import magic
import aiohttp
import logging
import concurrent.futures
from wand.image import Image
import asyncio
import settings
import re

logger = logging.getLogger('main')


class FileConvert:
    def __init__(self):
        self.magic = magic.Magic(mime=True)
        self.session = aiohttp.ClientSession()

    # TODO need add some abstractions to downloads

    async def check_media(self, event, bot):
        iter_file = bot.iter_download(event.message.media.photo,
                                      chunk_size=128, request_size=128)
        bytes_file = bytes(await iter_file.__anext__())
        print(bytes_file)
        mime_file = self.magic.from_buffer(bytes_file)
        if "image" in mime_file:
            bytes_file = b""
            async for chunk in iter_file:
                # print(len(bytes(chunk)), bytes(chunk))
                bytes_file += bytes(chunk)
            await iter_file.close()
            iter_file = None
            return bytes_file
        else:
            return None

    def convert_image(self, byte_file: bytes):
        try:
            with Image(blob=byte_file) as img:
                if (img.width, img.height) != (256, 256):
                    img.resize(256, 256)
                    img.filename = "image_to_test"
                    img.format = "png"
                    return img.make_blob()
                else:
                    img.filename = "image_to_test"
                    img.format = "png"
                    return img.make_blob()
        except Exception as e:
            return None


file_convert = FileConvert()


def convert_image(bytes_file):
    """some python Magic?"""
    return file_convert.convert_image(bytes_file)


class CheckContent:
    def __init__(self, bot):
        self.bot = bot
        pass

    async def check_events(self, event):
        bytes_file = await file_convert.check_media(event, self.bot)
        if not bytes_file:
            return
        loop = asyncio.get_event_loop()
        with concurrent.futures.ProcessPoolExecutor(max_workers=1) as pool:
            async with aiohttp.ClientSession(
                    headers={"token": settings.server_token}) as session:
                image256 = await loop.run_in_executor(pool,
                                                      convert_image,
                                                      bytes_file)
                if not image256:
                    return
                async with session.post(f"{settings.server_url}/check_file",
                                        data={"file": image256}) as response:
                    result = await response.json()

        if not result.get("file_hash"):
            return
        if result["unsafe"] > settings.coefficient_unsafe:
            logger.info(f"Remove image hash: {result}")
            sender = await event.message.get_sender()
            await event.message.respond(
                f"@{sender.username} your message can contain 18+ content.")
            await event.message.delete()
