#包
import sys
from audioop import error

import orjson
import asyncio
import aiohttp

#import cchardet
import async_timeout

from GobalVar import JSON_FIELDS_INDICATORS, REQUIRED_JSON_FIELDS_INDICATORS


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

#内容捕获并将其存储至data_queue
async def data_capture(data_queue):
    try:
        while True:
            await data_queue.put(await get_result())
            await asyncio.sleep(0.015)
    except asyncio.CancelledError:
        print("数据捕获任务已被关闭！")

#在控制台进行内容输出
async def data_printer(data_queue):
    try:
        while True:
            for data in await data_queue.get():
                print(orjson.dumps(data).decode())
                if data[1] is not None:
                    res = json_parser(data[1])
                    print(f"解析出的数据：{res}")
            #让出操控权
            await asyncio.sleep(0.005)
    except asyncio.CancelledError:
        print("数据输出任务已被关闭！")


#数据解析
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
def progress_clear(data_queue):
    print(f"{data_queue}已被清理完毕！")
    data_queue = 0

























