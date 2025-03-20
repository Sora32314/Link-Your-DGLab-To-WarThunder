#额外包
import sys
from functools import wraps

import orjson
import asyncio
import aiohttp

import time

#import cchardet
import async_timeout

from DGLab_WT_Lib import data_printer, progress_clear, json_parser, json_capture
#自定义包
from GobalVar import DATA_SIZE_QUEUE, data_queue
from DGLab_WT_Lib import Data_Storage_Instance as DSI

import DGLab_WT_Lib
import Bleak_DGLab



#对于初次使用python并且阅读到此处的用户：在Python中，多线程拥有全局解释器锁（GIL），因此并不能并行运行，只能够并发运行，因此对于IO密集型任务，\
#我们可以用协程来模拟多线程运行，协程的速度在Python的IO密集型任务中与多线程效率大致相当。


if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

"""
#时间基准测试
def async_timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[{func.__name__}]耗时：{elapsed:.6f} 秒。")
        return result
    return wrapper
"""




#主函数
async def main_():

    tasks = [
        asyncio.create_task(DSI.data_update()),
        asyncio.create_task(DSI.json_update()),
        asyncio.create_task(data_printer(DSI))
    ]

    await asyncio.sleep(3)

    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)









#入口函数
if __name__ == "__main__":
    asyncio.run(main_())
    #asyncio.run(init_())



