import time
import json
from typing import Dict, List, Tuple, Type
from threading import Thread
from redis import StrictRedis
import numpy as np
from controllers.BaseController import Point, BaseController
from config import SIM_CONTROLLER_CONFIG


class SimVehController:
    # 设备ID
    DEVICE_ID: int = SIM_CONTROLLER_CONFIG["device_id"]
    # 仅在以下场景下执行控制逻辑
    CONTROL_SCENARIOS = set(SIM_CONTROLLER_CONFIG["control_scenarios"])
    # Redis 配置
    REDIS_HOST: str = SIM_CONTROLLER_CONFIG["redis"]["host"]
    REDIS_PORT: int = SIM_CONTROLLER_CONFIG["redis"]["port"]
    REDIS_PASSWORD: str = SIM_CONTROLLER_CONFIG["redis"]["password"]
    # 订阅输入数据的通道
    SUB_CHANNEL: str = SIM_CONTROLLER_CONFIG["channels"]["subscribe"]

    # 各场景对应的控制器：键为场景序号，值为控制器类
    CONTROLLER_CLASS_MAPPING: Dict[int, Type[BaseController]] = SIM_CONTROLLER_CONFIG["controller_class_mapping"]

    def __init__(self):
        # 当前测试序号
        self.test_number: int = 1
        # 当前场景序号
        self.scenario_number: int = SIM_CONTROLLER_CONFIG["default_scenario"]

        # 统一的场景配置（路径 + 特殊行为）
        self.scenario_configs = SIM_CONTROLLER_CONFIG["scenario_configs"]

        # 需要被本算法控制的车辆ID集合（由data_type==2消息指定）
        self.controlled_vehicle_ids: set[int] = set()

        # 当前配置相关成员变量（由_apply_config统一设置）
        if self.scenario_number not in self.scenario_configs:
            self.scenario_number = next(iter(self.scenario_configs.keys()))
        self.current_config = self.scenario_configs[self.scenario_number].copy()
        self.use_lane_switching = False
        self.apply_offset = False
        self.offset_roads = []
        self.offset_count = 0
        self.y_offset = 0.0
        self.route_element_ids = []
        self.route_lane_numbers = []
        self.current_route_points: List[Point] = []

        # 控制器实例映射
        self.controller_mapping: Dict[Tuple[int, int], BaseController] = {}

        # Redis客户端
        self.redis_client = StrictRedis(host=self.REDIS_HOST, port=self.REDIS_PORT, password=self.REDIS_PASSWORD)

        # 加载路网
        self.road_network = self._load_road_network(SIM_CONTROLLER_CONFIG["road_network_file"])

        # 初始化时立即应用场景1配置（生成current_route_points等）
        self._apply_config()

    def _load_road_network(self, json_file_path: str) -> Dict:
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[ERROR] JSON file {json_file_path} not found!")
            return {}
        except json.JSONDecodeError:
            print(f"[ERROR] Invalid JSON format in {json_file_path}!")
            return {}
        except Exception as e:
            print(f"[ERROR] Failed to load road network: {e}")
            return {}

    def _find_road_by_id(self, road_id: int) -> Dict:
        for road in self.road_network.get("road", []):
            if road.get("id") == road_id:
                return road
        return {}

    def _get_points_from_road(self, road: Dict, lane_number: int) -> List[Point]:
        points = []
        lanes = road.get("lanes", [])
        target_lane = None
        for lane in lanes:
            if lane.get("number") == lane_number:
                target_lane = lane
                break
        if target_lane:
            center_points_tess = target_lane.get("centerPointsTess", [])
            for point in center_points_tess:
                if len(point) >= 2:
                    points.append(Point(x=point[0], y=point[1]))
        else:
            points_tess = road.get("pointsTess", [])
            for point in points_tess:
                if len(point) >= 2:
                    points.append(Point(x=point[0], y=point[1]))
        return points

    def _get_points_from_lane_switching(self, road: Dict, base_lane_number: int, switch_lane_number: int) -> List[Point]:
        points = []
        base_lane_points = self._get_points_from_road(road, base_lane_number)
        switch_lane_points = self._get_points_from_road(road, switch_lane_number)
        if not base_lane_points or not switch_lane_points:
            print(f"[WARNING] Cannot get points from both lanes {base_lane_number} and {switch_lane_number}")
            return base_lane_points or switch_lane_points

        min_length = min(len(base_lane_points), len(switch_lane_points))
        base_lane_points = base_lane_points[:min_length]
        switch_lane_points = switch_lane_points[:min_length]

        for i in range(min_length):
            if (i // 2) % 2 == 0:
                points.append(base_lane_points[i])
            else:
                points.append(switch_lane_points[i])
        print(f"[INFO] Generated {len(points)} points with lane switching between lane {base_lane_number} and {switch_lane_number}")
        return points

    def _offset_points_for_specific_roads(self, road_id: int, points: List[Point], offset_count: int, y_offset: float) -> List[Point]:
        if offset_count <= 0 or road_id not in self.offset_roads:   # ← 这里改成用配置的offset_roads
            return points
        offset_points = []
        for i, point in enumerate(points):
            if i < offset_count:
                offset_points.append(Point(x=point.x, y=point.y + y_offset))
            else:
                offset_points.append(point)
        print(f"[INFO] Applied y-offset of {y_offset} to first {offset_count} points of road {road_id}")
        return offset_points

    def _get_route_points_from_elements(self) -> List[Point]:
        route_points = []
        if len(self.route_element_ids) != len(self.route_lane_numbers):
            print(f"[ERROR] Element IDs count and Lane numbers count must be equal!")
            return route_points

        for i, element_id in enumerate(self.route_element_ids):
            lane_number = self.route_lane_numbers[i]
            road = self._find_road_by_id(element_id)
            if not road:
                continue

            if self.use_lane_switching:
                switch_lane = 1 if lane_number == 0 else 0
                points = self._get_points_from_lane_switching(road, lane_number, switch_lane)
            else:
                points = self._get_points_from_road(road, lane_number)

            if self.apply_offset:
                points = self._offset_points_for_specific_roads(element_id, points, self.offset_count, self.y_offset)

            route_points.extend(points)
            print(f"[INFO] Added {len(points)} points from road {element_id} (lane {lane_number})")

        print(f"[INFO] Generated route with {len(route_points)} points from {len(self.route_element_ids)} elements")
        return route_points

    def _apply_config(self):
        cfg = self.current_config
        self.use_lane_switching = cfg["use_lane_switching"]
        self.apply_offset = cfg["apply_offset"]
        self.offset_roads = cfg["offset_roads"]
        self.offset_count = cfg["offset_count"]
        self.y_offset = cfg["y_offset"]
        self.route_element_ids = cfg["element_ids"]
        self.route_lane_numbers = cfg["lane_numbers"]
        # 立即生成最新的全局路径点
        self.current_route_points = self._get_route_points_from_elements()
        print(f"[INFO] Config applied, generated {len(self.current_route_points)} route points")

    def _is_control_enabled(self) -> bool:
        return self.scenario_number in self.CONTROL_SCENARIOS

    def start(self) -> None:
        print("[INFO] Start SimVehController!")
        while True:
            pub_sub = self.redis_client.pubsub()
            pub_sub.subscribe(self.SUB_CHANNEL)
            for message in pub_sub.listen():
                if not message or message.get("type") != "message":
                    continue
                try:
                    data: dict = json.loads(message["data"].decode("utf-8"))
                except:
                    continue

                data_type: int = data.get("type", 0)

                if data_type == 1:  # 心跳
                    status_channel = data["statusChannel"]
                    Thread(target=self._send_heartbeat_data, args=(status_channel,), daemon=True).start()
                    print(f"[INFO] Start heartbeat thread -> {status_channel}")

                elif data_type == 2:  # 开始控制（指定哪些车由本算法控制）
                    if not self._is_control_enabled():
                        self.controlled_vehicle_ids.clear()
                        print(f"[INFO] Scenario {self.scenario_number} 不需要控制，忽略控制请求")
                        continue
                    location_channel = data["locationChannel"]
                    control_channel = data["controlChannel"]

                    # 记录需要控制的车辆ID（只有这些车会创建控制器）
                    self.controlled_vehicle_ids = {int(veh_id) for veh_id in data["vehPointsMapping"].keys()}

                    print(f"[INFO] Start control thread, controlling vehicles {sorted(self.controlled_vehicle_ids)}, "
                          f"current route points: {len(self.current_route_points)}")

                    Thread(target=self._receive_location_and_send_control_data,
                           args=(location_channel, control_channel), daemon=True).start()

                elif data_type == 3:  # 切换场景
                    self.scenario_number = data["scenarioNumber"]
                    if self.scenario_number not in self.scenario_configs:
                        print(f"[WARN] Scenario {self.scenario_number} not exist, fallback to default")
                        self.scenario_number = SIM_CONTROLLER_CONFIG["default_scenario"]

                    self.current_config = self.scenario_configs[self.scenario_number].copy()
                    self._apply_config()  # ← 这里会重新生成 self.current_route_points（新路径）

                    # 清空旧控制器，下一次位置消息到来时会用新的scenario_number（新算法）和新的current_route_points重新创建
                    old_count = len(self.controller_mapping)
                    self.controller_mapping.clear()
                    if not self._is_control_enabled():
                        self.controlled_vehicle_ids.clear()

                    print(f"[INFO] Scenario switched to {self.scenario_number}, "
                          f"route points: {len(self.current_route_points)}, "
                          f"lane_switching={self.use_lane_switching}, offset={self.apply_offset}, "
                          f"cleared {old_count} old controllers")

            time.sleep(1)

    def _send_heartbeat_data(self, status_channel: str) -> None:
        while True:
            heartbeat_data_1 = {
                "timestamp": int(time.time() * 1000),
                "deviceId": self.DEVICE_ID,
                "type": 0,
                "state": 1
            }
            self.redis_client.publish(status_channel, json.dumps(heartbeat_data_1))

            heartbeat_data_2 = {
                "timestamp": int(time.time() * 1000),
                "deviceId": self.DEVICE_ID,
                "type": 1,
                "state": 1
            }
            self.redis_client.publish(status_channel, json.dumps(heartbeat_data_2))
            time.sleep(1)

    def _receive_location_and_send_control_data(self, location_channel: str, control_channel: str) -> None:
        while True:
            pub_sub = self.redis_client.pubsub()
            pub_sub.subscribe(location_channel)

            for message in pub_sub.listen():
                if not message or message["type"] != "message":
                    continue
                try:
                    msg_data: dict = json.loads(message["data"].decode("utf-8"))
                    vehicle_data_list = msg_data["value"]["value"]
                except:
                    continue

                # 收集所有车辆作为障碍物
                obstacles = []
                for vehicle_data in vehicle_data_list:
                    vehicle_id = vehicle_data["originId"]
                    current_x = vehicle_data["x"]
                    current_y = vehicle_data["y"]
                    current_speed = vehicle_data["speed"] / 3.6
                    current_angle = vehicle_data["courseAngle"]
                    angle_rad = current_angle * np.pi / 180
                    vx = current_speed * np.cos(angle_rad)
                    vy = current_speed * np.sin(angle_rad)
                    obstacles.append([current_x, current_y, vx, vy])
                obstacles_array = np.array(obstacles) if obstacles else np.array([])

                action_list: List[dict] = []
                if not self._is_control_enabled():
                    self.controller_mapping.clear()
                    self.controlled_vehicle_ids.clear()
                    continue
                for vehicle_data in vehicle_data_list:
                    vehicle_id: int = vehicle_data["originId"]
                    vehicle_number: int = vehicle_data["number"]
                    drive_type: int = vehicle_data["driveType"]
                    control_type: int = vehicle_data["controlType"]

                    if drive_type == 1 or control_type == 0:
                        continue

                    # 只有被指定的车辆才创建/使用控制器
                    if vehicle_id not in self.controlled_vehicle_ids:
                        continue

                    key = (vehicle_id, vehicle_number)

                    if key not in self.controller_mapping:
                        controller_class = self.CONTROLLER_CLASS_MAPPING.get(self.scenario_number)
                        if controller_class is None:
                            continue

                        if len(self.current_route_points) == 0:
                            print(f"[WARNING] No route points for vehicle {vehicle_id}")
                            continue

                        controller = controller_class()
                        controller.set_route_points(self.current_route_points)  # ← 永远使用最新的全局路径
                        self.controller_mapping[key] = controller
                        print(f"[INFO] Created {controller_class.__name__} for vehicle {vehicle_id}-{vehicle_number}, "
                              f"route points: {len(self.current_route_points)}")

                    controller = self.controller_mapping[key]

                    current_x = vehicle_data["x"]
                    current_y = vehicle_data["y"]
                    current_speed = vehicle_data["speed"] / 3.6
                    current_accel = vehicle_data["acceleration"]
                    current_angle = vehicle_data["courseAngle"]

                    action = controller.get_next_action(
                        current_x, current_y, current_speed, current_accel,
                        current_angle, obstacles=obstacles_array
                    )

                    action_data = {
                        "id": vehicle_id,
                        "number": vehicle_number,
                        **action.model_dump()
                    }
                    action_list.append(action_data)

                if action_list:
                    control_data = {"params": action_list}
                    self.redis_client.publish(control_channel, json.dumps(control_data))

            time.sleep(1)


if __name__ == "__main__":
    sim_veh_controller = SimVehController()
    sim_veh_controller.start()