import logging
import asyncio

import command_manager
import channel_manager

from config import dp, bot

logging.basicConfig(level=logging.INFO)


# Запуск бота
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling(bot))
    loop.run_forever()