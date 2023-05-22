from asyncio import run
from multiprocessing import Process


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
    async def work(dp, bot):
        await dp.start_polling(bot)

    def start_schedule(self, dp, bot):
        # while True:
        run(self.work(dp, bot))
            # time.sleep(20)
