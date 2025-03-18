from Cython.Utility.Dataclasses import Field
import asyncio
from DGLab_WT_Lib import DataStorage

READ_CHUNK_SIZE = 4096      #已弃用

DATA_SIZE_QUEUE = 128       #已弃用


#数据队列
data_queue = asyncio.Queue(maxsize=DATA_SIZE_QUEUE)
#保留data_queue，保持一部分未来的拓展性。但是data_queue在实际上已弃用


#获取JSON信息字段
JSON_FIELDS_INDICATORS = [
    "army",  # 载具类型
    "crew_total",  # 车组人员总数
    "crew_current",  # 当前在位的车组人员数
    "driver_state",  # 驾驶员状态
    "gunner_state",  # 炮手状态
    "gunner_time_to_take_place",  # 炮手就位所需时间
    "driver_time_to_take_place",  # 驾驶员就位所需时间
    "rpm",  # 发动机每分钟转数
    "speed",  # 当前行驶速度
    "has_speed_warning",  # 是否有超速警告（导弹车辆超速无法发射）
    "lws",  # 镭射告警状态
    "ircm",  # 红外对抗措施状态
    "engine_broken",  # 发动机是否损坏
    "engine_dead",  # 发动机是否完全失效
    "v_drive_broken",  # 高低机装置是否损坏
    "h_drive_broken",  # 方向机是否损坏
    "transmission_broken",  # 传动是否受损
    "track_broken",  # 履带是否断裂
    "barrel_dead",  # 炮管是否损坏
    "breech_damaged",  # 炮闩是否损坏
    "breach_dead",  # 炮闩是否完全失效
    "is_repairing_auto",  # 是否正在自动修复
    "repair_time",  # 修复所需的时间
    "is_repairing",  # 是否正在进行修复操作
    "first_stage_ammo",  # 待发弹药架
    "stabilizer"  # 火炮稳定器状态
]

#不可缺少的字段
REQUIRED_JSON_FIELDS_INDICATORS  = ["army", "crew_total", "crew_current"]


"""        results = [
            json.get("army"),   #载具种类
            json.get("crew_total"),  # 成员总数
            json.get("crew_current"),  # 当前成员数
            json.get("driver_state"),  # 驾驶员状态
            json.get("gunner_state"),  # 炮手状态
            json.get("gunner_time_to_take_place"),  # 炮手等待替换时间
            json.get("driver_time_to_take_place"),  # 驾驶员等待替换时间
            json.get("rpm"),  # 发动机转速
            json.get("speed"),  # 速度
            json.get("has_speed_warning"),  # 超速警告
            json.get("lws"),  # 激光告警系统状态
            json.get("ircm"),  # 红外对抗状态
            json.get("engine_broken"),  # 引擎是否受损
            json.get("engine_dead"),  # 引擎是否损坏
            json.get("v_drive_broken"),  # 水平驱动是否损坏
            json.get("h_drive_broken"),  # 垂直驱动是否损坏
            json.get("transmission_broken"),  # 传动是否损坏
            json.get("track_broken"),  # 履带是否损坏
            json.get("barrel_dead"),  # 炮管是否损坏
            json.get("breech_damaged"),  # 炮闩是否受损
            json.get("breach_dead"),  # 炮闩是否损坏
            json.get("is_repairing_auto"),  # 是否正在自动修复
            json.get("repair_time"),  # 自动修复时间
            json.get("is_repairing"),   #是否正在修理
            json.get("first_stage_ammo"),  # 代发弹药架
            json.get("stabilizer")  #稳定器
        ]
"""





#郊狼映射强度上限
MAX_STRENGTH = 0



#创建储存类实例
Data_Storage_Instance = DataStorage()









