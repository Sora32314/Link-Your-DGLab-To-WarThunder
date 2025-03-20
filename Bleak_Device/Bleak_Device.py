import asyncio
import logging
from time import sleep
from tkinter.font import names

from aioamqp import connect
from async_timeout import timeout
from bleak import BleakClient, BleakScanner

"""
设置log格式与目录。
"""
logging.basicConfig(
    level=logging.INFO,
    format = '%(asctime)s - [%(levelname)s]:%(message)s',
    filename='../logs/Bleak.log'
)


class BleakDevice:
    def __init__(self):
        #获取到的数据
        self.data = None
        #获取到所有的设备表
        self.deviceList = None
        #设备信息
        self.device = None
        #连接实例
        self.client = None
        #监听UUID
        self.uuid = None


    #扫描设备
    async def scan_device(self):
        logging.info(f"正在扫描Bleak设备。")
        self.deviceList = await BleakScanner.discover(return_adv=True)

        for device, adv_address in self.deviceList.values():
            logging.info(f"已发现如下设备：{device.name}，地址：{device.address}，RSSI（信号强度）：{adv_address.rssi}。")


    #扫描存在的设备后，通过名称进行配对
    async def connect_to_device(self, name):
        for device, adv_address in self.deviceList.values():
            if device.name == name:
                self.device = device
                break

        logging.info(f"正在连接到设备：{self.device.name}！")

        #设置蓝牙连接的等待超时时间为25s
        self.client = BleakClient(self.device, timeout=25)
        try:
            if not self.client.is_connected:
                await self.client.connect()
            logging.info(f"设备：{self.device.name}已连接成功！")
            return True
        except Exception as e:
            await self.client.disconnect()
            logging.error(f"在运行时出现了错误：{e}")

        logging.warning(f"未在蓝牙范围内找到所提供的设备名称：{name}。请检查设备是否存在并开机，或设备蓝牙功能是否故障。")
        return False

    #监听蓝牙程序发送的信息
    async def listening(self):
        try:
            if not self.client.is_connected and self.uuid is None:
                logging.error(f"不能在未连接的情况下进行监听！")
                return False

            print(f"开始监听特征值：{self.uuid}。")
            while True:
                await asyncio.sleep(0.015)

        except asyncio.CancelledError:
            logging.info(f"设备{self.device.name}已退出监听！")

            logging.info(f"清理中......")
            await self.disconnected()



    async def disconnected(self):
        try:
            if self.client and self.client.is_connected:
                logging.info(f"正在执行退出程序，请手动关闭{self.device.name}的蓝牙连接。")
                print(f"正在执行退出程序，请手动关闭{self.device.name}的蓝牙连接。")
                await asyncio.wait_for(self.client.disconnect(), timeout=120)
                logging.info(f"已安全断开{self.device.name}！")
                self.client = None
                self.device = None
            else:
                logging.warning(f"你不能在未连接时进行断开连接！")
        except asyncio.TimeoutError:
            logging.warning(f"断开操作超时，正在强制执行清理！")
            self.client = None
            self.device = None
            logging.info(f"强制清理操作执行完毕！请手动断开设备与蓝牙的连接。")
        finally:
            logging.info(f"设备已退出！")


def callback_handler(self, data):
    print(f"收到数据：{data}")
    try:
        decoded_data = data.decode("utf-8")
        print(f"解码后数据：{decoded_data}")
    except UnicodeDecodeError:
        print("无法解析字符串！")


async def run():
    instance = BleakDevice()

    await instance.scan_device()

    await asyncio.create_task(instance.connect_to_device("47L121000"))

    await instance.listening()




if __name__ == "__main__":
    asyncio.run(run())



