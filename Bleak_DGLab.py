
"""import asyncio
from platform import system

import pydglab
import logging
from pydglab import model_v3
from pydglab import model_v2
import importlib

from DGLab_WT_Lib import json_parser
from GobalVar import data_queue


logging.basicConfig(
    level=logging.INFO,
    format = '%(asctime)s - [%(levelname)s]:%(message)s',
    filename='./logs/App.log'
)


#连接到郊狼
async def bleak_dglab(instance_):
    max_retries = 15
    retry_delay = 1.5
    retry_count = 0

    while True:
        try:
            logging.info("连接中......")
            await instance_.create()
            logging.info(f"成功连接至实例。")
            return True
        except Exception as e:
            retry_count += 1
            logging.warning(f"连接失败，自动重连中!    次数：{retry_count}")
            await asyncio.sleep(retry_delay)
            if retry_count >= max_retries:
                logging.error(f"自动连接{retry_count}次数后仍然连接失败，请检查蓝牙设备是否正常工作！")
                logging.error(f"错误信息：{e}")
                return False


#设置强度
async def set_strength(data):



    return



async def init_():
    instance_ = pydglab.dglab_v3()

    if await bleak_dglab(instance_):
        logging.info(f"已连接至设备ID：{instance_.address}")
    else:
        logging.error(f"未能创建郊狼实例，请检查连接是否有效。设备ID：{instance_.address}")
        return


    try:
        await instance_.set_wave_sync(
            1, 9, 20, 5, 35, 20
        )



        logging.info(f"波形参数设置完成：{1, 9, 20, 5, 35, 20}")
    except Exception as e:
        logging.error(f"设置波形时出错，错误信息：{e}")
        return"""

















"""if __name__ == "__main__":
    asyncio.run(init_())"""
















