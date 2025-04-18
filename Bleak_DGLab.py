from dataclasses import dataclass

import Bleak_Device

import logging

from Bleak_Device.Bleak_Device import BleakDevice

logging.basicConfig(
    level=logging.INFO,
    format = '%(asctime)s - [%(levelname)s]:%(message)s',
    filename='../logs/Bleak_DGLab.log'
)



"""
OOP
"""

#只是个小工具没必要用太复杂的设计模式，所以就连单例也不想用，直接用最原始的方法（偷懒）好了。

#存放热数据
@dataclass
class Channel_A:
    Strength: int = 0,
    WaveFrequency: list[int] = [0,0,0,0],
    WaveStrength: list[int] = [0,0,0,0],
    Limit : int = 0

#存放热数据
@dataclass
class Channel_B:
    Strength: int = 0,
    WaveFrequency: list[int] = [0,0,0,0],
    WaveStrength: list[int] = [0,0,0,0],
    Limit : int = 0



#郊狼3控制器，请在外部传入BleakDevice类。
class Bleak_DGLab_V3_Controller:
    def __init__(self, instance):
        #操作对象
        if not isinstance(instance, BleakDevice):
            logging.warning(f"传入的设备实例非法，请传入 BleakDevice 蓝牙实例。 库：Bleak_Device。")
            self.shutdown()

        self.operator = instance
        self.Channel_A = Channel_A
        self.Channel_B = Channel_B



    async def setup_strength(self, strength_a : int, strength_b : int):

        if not isinstance(strength_a, int) or not isinstance(strength_b, int):
            logging.warning(f"A通道强度或B通道强度传入的类型非法，请传入int类型的参数（禁止除正整数外的类型传入）。")
            logging.warning(f"传入A通道参数类型： {type(strength_a)} 传入的B通道参数类型： {type(strength_b)} ")
            return

        if not (0 <= strength_a <= 200) or not (0 <= strength_b <= 200):
            logging.warning(f"A通道或B通道传入的强度值非法，请确保数值在[0-200]内。传入的强度值A：{strength_a}，传入的强度值B：{strength_b}。")
            return

        #设置段
        self.Channel_A.Strength = strength_a
        self.Channel_B.Strength = strength_b
        return


    async def setup_wave_frequency(self, wave_a : list[int], wave_b : list[int]):




        return


    async def setup_wave_strength(self, wave_a : list[int], wave_b : list[int]):




        return

    async def setup_limit(self, limit_a : int, limit_b : int):




        return

    async def hot_save(self):




        return


    #清理自己的残留并且关闭蓝牙连接
    async def shutdown(self):
        self.Channel_A = None
        self.Channel_B = None
        await self.operator.shutdown()


        logging.info(f"{self.operator.get_device_name()}清理完毕！")
        logging.info(f"{self.__class__.__name__}清理完毕！")
        print(f"{self.__class__.__name__}清理完毕！")
        print(f"已关机！")
        return

    #只清理自己的残留，并不对现有的蓝牙连接产生反应
    async def __clean__(self):
        self.Channel_A = None
        self.Channel_B = None

        logging.info(f"{self.__class__.__name__}清理完毕！")
        print(f"{self.__class__.__name__}清理完毕！")
        return












