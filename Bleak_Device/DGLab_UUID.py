
from typing import Union

from dataclasses import dataclass
from bleak import BleakGATTCharacteristic


@dataclass(frozen=True)
class UUID_V3:
    Write_Service:                          str = "0000180c-0000-1000-8000-00805f9b34fb"
    Notify_Service:                         str = "0000180c-0000-1000-8000-00805f9b34fb"
    Read_Service:                           str = "0000180a-0000-1000-8000-00805f9b34fb"


    #Read Only
    Battery_Characteristic:                 str = "00001500-0000-1000-8000-00805f9b34fb"
    #Write
    Write_Characteristic:                   str = "0000150a-0000-1000-8000-00805f9b34fb"
    #Notify
    Notify_Characteristic:                  str = "0000150b-0000-1000-8000-00805f9b34fb"


#暂未支持
@dataclass(frozen=True)
class UUID_V2:
    NULL:                                str = "NULL"











