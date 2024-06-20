import asyncio
import time
from aiogram import BaseMiddleware, types
from aiogram.dispatcher.event.handler import HandlerObject


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, default_rate: int = 0.5) -> None:
        self.limiters = {}
        self.default_rate = default_rate
        self.count_throttled = 1
        self.last_throttled = 0

    async def __call__(self, handler, event: types.Update, data):
        real_handler: HandlerObject = data["handler"]
        skip_pass = True
        if real_handler.flags.get("skip_pass") is not None:
            skip_pass = real_handler.flags.get("skip_pass")
        if skip_pass:
            if int(time.time()) - self.last_throttled >= self.default_rate:
                self.last_throttled = int(time.time())
                self.default_rate = 0.5
                self.count_throttled = 0
                return await handler(event, data)
            else:
                if self.count_throttled >= 2:
                    self.default_rate = 3
                else:
                    self.count_throttled += 1
                    try:
                        rem = await event.message.answer("<b>Too many requests!</b>")
                        await asyncio.sleep(3)
                        await rem.delete()
                    except AttributeError:
                        pass
                        # print(error)

            self.last_throttled = int(time.time())
        else:
            return await handler(event, data)
