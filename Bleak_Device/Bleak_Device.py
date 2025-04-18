import asyncio
import logging
from contextlib import nullcontext
from dataclasses import dataclass
from time import sleep
from tkinter.font import names

from aioamqp import connect
from async_timeout import timeout
from bleak import BleakClient, BleakScanner, BleakError
from DGLab_UUID import UUID_V3

"""
日期格式：YYYY/MM/DD
"""

"""
设置log格式与目录。
"""
logging.basicConfig(
    level=logging.INFO,
    format = '%(asctime)s - [%(levelname)s]:%(message)s',
    filename='../logs/Bleak.log'
)

@dataclass(frozen=True)
class CCCD_UUID:
    CCCD_UUID: str = "00002902-0000-1000-8000-00805f9b34fb"


class BleakDevice:
    def __init__(self):
        #获取到的数据
        self.data = None
        #获取到所有的设备表
        self.deviceList = None
        self.device = None
        #连接实例
        self.client = None
        #监听UUID
        self.uuid = []
        #服务
        self.service = None
        #连接状态
        self.__connection__ = False


    #扫描设备
    async def __scan_device__(self):
        logging.info(f"正在扫描Bleak设备。")
        self.deviceList = await BleakScanner.discover(return_adv=True)

        for device, adv_address in self.deviceList.values():
            logging.info(f"已发现如下设备：{device.name}，地址：{device.address}，RSSI（信号强度）：{adv_address.rssi}。")


    #扫描存在的设备后，通过名称进行配对
    async def create_connection(self, name, _timeout: float = 25):
        await self.__scan_device__()

        for device, device_adv in self.deviceList.values():
            if device.name == name:
                self.device = device
                break

        if not self.device:
            raise BleakError(f"未找到所提供的蓝牙设备：{name}！")

        logging.info(f"正在连接到设备：{self.device.name}！")
        """
        自动管理蓝牙资源，用以替换曾进行手动管理的断开连接失败尝试。
        因为对蓝牙协议的了解不足，只能使用with进行自动管理。
        
        2025/4/1 更新：是的，无法正常断开连接的原因是当Windows系统配对蓝牙设备之后，系统会认为系统需要长时间与蓝牙设备保持连接/
        而程序的权限不足以绕开Windows的管理，所以根本无法在配对的情况下断开连接，于是换回手动连接。
        """
        self.client = BleakClient(self.device, timeout = _timeout, winrt=dict(use_cached_services=False))
        await self.client.connect()
        #设置连接信息
        self.__connection__ = True

        try:
            logging.info(f"设备：{self.device.name}已连接成功！")
            logging.info(f"设备地址：{self.device.address}")



            #保持连接，每循环占用50ms
            while True:
                await asyncio.sleep(0.5)
                if not self.__connection__:
                    break

        except BleakError as e:
            logging.warning(f"{e}")
        except asyncio.CancelledError:
            logging.info(f"建立的连接已成功收到取消命令！")
        except Exception as e:
            logging.error(f"未知错误：{e}")
        finally:
            logging.info(f"正在清理中......")
            await self.__clean__()
            logging.info(f"清理完毕！")
            logging.info(f"已安全退出！")
            await self.client.disconnect()
            return True

    #拼写控制命令
    @staticmethod
    def make_command_hex(cmd):
        command = None

        try:
            command = bytes.fromhex(
                cmd
            )
            return command
        except asyncio.CancelledError:
            return command

        except Exception as e:
            logging.warning(f"拼写控制命令出错： “{e}” 命令： {cmd} 无法被转换为HEX或其他错误。")
            return command

    #对UUID写入消息
    async def writing(self, uuid, message, _timeout: float = 25):
        try:
            if self.client is None or self.client.is_connected is None:
                if await asyncio.wait_for(self.__check_connection__(), _timeout) is False:
                    logging.warning(f"对{uuid}的写入尝试超时，不可以在未进行连接时就对UUID执行写入！")
                    return False

            print(f"正在对 {uuid} 写入数据：{message}")

            await self.client.write_gatt_char(uuid, message)
            return
        except asyncio.CancelledError:
            return


    #监听蓝牙程序发送的信息
    async def listening(self, uuid, _timeout: float = 25):
        try:
            if self.client is None or self.client.is_connected is None:
                if await asyncio.wait_for(self.__check_connection__(), _timeout) is False:
                    logging.warning(f"对{uuid}的监听尝试超时，不可以在未进行连接时就监听UUID！")
                    return False

            print(f"开始监听特征值：{uuid}")

            await self.client.start_notify(uuid, callback_handler)

            self.uuid.append(uuid)
            return
        except asyncio.CancelledError:
            return
        except Exception as e:
            print(e)
            return

    #获取服务并打印
    async def print_service(self):
        if self is not None:
            services = self.client.services
            for service in services:
                print(f"服务UUID：{service.uuid}，描述：{service.description}")
                for char in service.characteristics:
                    read = "read" in char.properties
                    write = "write" in char.properties
                    notify = "notify" in char.properties
                    print(f"  特征值 UUID: {char.uuid} (可读: {read}, 可写: {write}， 通知：{notify})， 描述：{char.description}")
        return

    #获取存在的服务
    async def get_service(self, uuid: str):
        if self is not None:
            for service in self.client.services:
                if service.uuid == uuid:
                    return service

    #获取存在的特征值
    async def get_characteristic(self, uuid: str):
        if self is not None:
            for service in self.client.services:
                for char in service.characteristics:
                    if char.uuid == uuid:
                        return char

    #获取设备名称
    async def get_device_name(self):
        return self.device.name

    #关机
    async def shutdown(self):
        self.__connection__ = False
        return

    #清理
    async def __clean__(self):
        if self is not None and len(self.uuid) > 0 and self.client is not None:
            print("清理中......")
            self.__connection__ = False

            for item in self.uuid:
                print(f"清理：{item}")
                await self.client.stop_notify(item)
            print("清理完毕！")
        return

    #检查连接
    async def __check_connection__(self):
        while not self.__connection__:
            await asyncio.sleep(0.5)
        return True




def callback_handler(sender, data):
    #用于测试
    print(f"发送者：{sender}，收到数据：{data}")
    try:
        decoded_data = data.decode("gb2312")
        print(f"解码前数据：{data}，解码后数据：{decoded_data}")
    except UnicodeDecodeError:
        print("无法解析字符串！")

    except Exception as e:
        print(f"发现未知错误：{e}")




async def run():

    instance = BleakDevice()

    task = asyncio.create_task(instance.create_connection("47L121000"))

    await instance.listening(UUID_V3.Notify_Characteristic)

    command_str = instance.make_command_hex("B0000505")

    await instance.writing(UUID_V3.Write_Characteristic, command_str)

    await asyncio.sleep(25)

    task.cancel()

    await asyncio.gather(task, return_exceptions=True)

    return










if __name__ == "__main__":
    asyncio.run(run())



