#包
import logging
import sys
from audioop import error
from pkgutil import get_data

import orjson
import asyncio
import aiohttp

#import cchardet
import async_timeout


from GobalVar import JSON_FIELDS_INDICATORS, REQUIRED_JSON_FIELDS_INDICATORS, data_queue, Data_Storage_Instance as DSI
#保留data_queue，保持一部分未来的拓展性。但是data_queue在实际上已弃用

class DataStorage:
    def __init__(self):
        self.__data = None
        self.__data_json = None

    async def data_update(self):
        while True:
            try:
                self.__data = await get_result()
                await asyncio.sleep(0.01)
            except asyncio.CancelledError:
                print("数据更新服务已被关闭！")
            except Exception as e:
                print(f"data_update发生错误：{e}")


    async def json_update(self):
        while True:
            try:
                self.__data_json = await json_capture()
                await asyncio.sleep(0.01)
            except asyncio.CancelledError:
                print("Json更新服务已被关闭！")
            except Exception as e:
                print(f"json_update发生错误：{e}")

    def get_data(self):
        return self.__data

    def get_json(self):
        return self.__data_json



async def json_capture():
    try:
        res = None
        for data in await DSI.get_data():
            if data[1] is not None:
                res = json_parser(data[1])
        return res
    except Exception as e:
        print(f"在获取data时发生了意料之外的错误：{e}")
        logging.error(f"在获取data时发生了意料之外的错误：{e}")




#获取response信息，提取数据
async def fetch(url):
    #进行url内容请求，因为请求是本地，正常使用不会报错。故不使用try catch以免浪费性能（虽然3.11有无损耗try catch）。
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            str_ = f"这是来自 {url} 的结果：" #+ await response.text()

            if response.headers.get('Content-Type') == 'application/json':
                results = [str_, await response.json()]
            else:
                results = [str_, None]

            return results


#def img_captor(url):

#从fetch中获取指定url提供的数据
async def get_result():
    #战争雷霆本地主机8111端口数据（全部，以供后续开发）
    urls = [
        #'http://localhost:8111',
        'http://localhost:8111/gamechat',
        'http://localhost:8111/hudmsg',
        'http://localhost:8111/indicators',
        'http://localhost:8111/map_info.json',
        'http://localhost:8111/map_obj.json',
        'http://localhost:8111/mission.json',
        'http://localhost:8111/state'
    ]
    tasks = [fetch(url) for url in urls]
    return await asyncio.gather(*tasks)

#在控制台进行内容输出
async def data_printer(data_storage):
    while True:
        try:
            print(f"输出内容：{data_storage.get_data()}")
            print(f"输出内容：{data_storage.get_json()}")
            #让出操控权
            await asyncio.sleep(0.005)
        except asyncio.CancelledError:
            print("数据输出任务已被关闭！")


#Json解析
def json_parser(json):
    try:
        results = []
        missing_critical = []
        for FIELD in JSON_FIELDS_INDICATORS:
            value = json.get(FIELD)
            if value is None:
                if FIELD in REQUIRED_JSON_FIELDS_INDICATORS:
                    missing_critical.append(FIELD)
                value = "N/A" if FIELD in REQUIRED_JSON_FIELDS_INDICATORS else None
            results.append([FIELD, value])

        if missing_critical:
            return f"解析时出现错误，发现缺失的重要信息！以下是缺失的部件信息：{missing_critical}！"

        return results

    except Exception as e:
        return f"解析错误{str(e)}"





#数据清理
def progress_clear(data_queue_):
    print(f"{data_queue_}已被清理完毕！")
    data_queue_ = 0

























