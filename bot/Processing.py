from multiprocessing import Process
from asyncio import run
import time
from bot.admin_panel import app


class App:
    def __init__(self) -> None:
        self.p0 = Process()

    def start_process(self, func, arg=None):
        if arg is not None:
            self.p0 = Process(target=func, args=(arg,))
        else:
            self.p0 = Process(target=func)
        self.p0.start()

    def stop_process(self):
        self.p0.terminate()

    @staticmethod
    async def work():
        app.run()

    def start_schedule(self):
        while True:
            run(self.work())
            time.sleep(20)
