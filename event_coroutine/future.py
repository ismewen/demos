import aiohttp


class Future(object):

    def __init__(self, loop):
        self.loop = loop
        self.done = False
        self.coroutine = None

    def set_coroutine(self, coroutine):
        self.coroutine = coroutine

    def set_done(self):
        self.done = True

    def result(self):
        pass

    # 如果没有完成任务，让出cpu
    def __await__(self):
        if not self.done:
            yield self
        return


import asyncio


async def test():
    async with aiohttp.ClientSession() as session:
        await session.get("http://www.baidu.com")
t = asyncio.create_task(test())