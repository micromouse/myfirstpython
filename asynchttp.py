# 异步http
import asyncio

import aiohttp


async def fetch(url: str):
    """
    异步获取Url内容
    :param url: Url
    :return: Url内容
    """
    async with aiohttp.ClientSession() as session:
        print(f"5秒钟后获取[{url}]内容")
        await asyncio.sleep(5)
        print(f"开始获取[{url}]内容")
        async with session.get(url) as response:
            return await response.text()


async def main():
    context = await fetch("https://www.baidu.com")
    print(f"已获取到[https://www.baidu.com]内容：\n{context}")


asyncio.run(main())
