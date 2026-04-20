from typing import List
from math import sqrt, sin, cos, pi
import numpy as np

from controllers.BaseController import BaseController, Point, Action
from .lattice_planner import get_reference_line, lattice_planner_for_Cruising, C


class Controller2(BaseController):
    def __init__(self):
        super().__init__()
        self.ref_spline = None
        self.current_lattice_path = None
        self.lattice_path_index = 0

        self.end_point = None

    def reset(self):
        self.ref_spline = None
        self.current_lattice_path = None
        self.lattice_path_index = 0

    def set_route_points(self, line: List[Point]) -> None:
        cleaned_points = []
        for p in line:
            if not cleaned_points or sqrt((p.x - cleaned_points[-1].x) ** 2 + (p.y - cleaned_points[-1].y) ** 2) > 1e-6:
                cleaned_points.append(p)
        if len(cleaned_points) < 2:
            raise ValueError("Not enough unique points to create spline")
        wx = [p.x for p in cleaned_points]
        wy = [p.y for p in cleaned_points]
        self.ref_spline = get_reference_line(wx, wy)[4]
        self.end_point = Point(x=line[-1].x, y=line[-1].y)

    def get_next_action(self, current_x: float, current_y: float, speed: float, accel: float, angle: float, obstacles: np.ndarray = None) -> Action:
        # 判断是否到达终点
        dist = ((current_x - self.end_point.x)**2 + (current_y - self.end_point.y)**2)**0.5
        if dist < 1:
            return Action(type=1, lon=current_x, lat=current_y, remove=True)

        # 接入lattice规划
        if self.current_lattice_path is None or self.lattice_path_index >= len(self.current_lattice_path.x) - 1:
            s0 = self._find_s(current_x, current_y)
            l0 = self._calc_l(current_x, current_y, s0)
            s0_v = speed
            s0_a = accel
            l0_v = 0.0
            l0_a = 0.0
            # 检查输入参数
            if not (-C.ROAD_WIDTH <= l0 <= C.ROAD_WIDTH):
                print(f"Warning: Invalid l0={l0}, resetting to 0")
                l0 = 0.0
            if s0 < 0 or s0 > self.ref_spline.s[-1]:
                print(f"Warning: Invalid s0={s0}, resetting to 0")
                s0 = 0.0
            # 设置障碍物为空
            # 设置障碍物：使用传入的障碍物信息
            # if obstacles is not None and len(obstacles) > 0:
            #     C.obs = obstacles
            #     print(f"设置 {len(obstacles)} 个障碍物")
            # else:
            #     C.obs = np.array([])
            #     print("没有障碍物")
            C.obs = np.array([])

            # 调用lattice规划
            self.current_lattice_path = lattice_planner_for_Cruising(l0, l0_v, l0_a, s0, s0_v, s0_a, self.ref_spline)
            if not self.current_lattice_path:
                print("Error: Lattice path not found")
                return Action(type=1, lon=current_x, lat=current_y)
            self.lattice_path_index = 1  # 从下一个点开始

        # 获取下一个xy坐标
        next_x = self.current_lattice_path.x[self.lattice_path_index]
        next_y = self.current_lattice_path.y[self.lattice_path_index]
        self.lattice_path_index += 1  # 步进到下一个点

        return Action(type=1, lon=next_x, lat=next_y)

    def _find_s(self, x, y):
        """在参考路径上找到最近的s"""
        if not self.ref_spline:
            return 0.0
        max_s = self.ref_spline.s[-1] - 1e-10
        s_values = np.linspace(0, max_s, num=1000, endpoint=True)
        dists = []
        for s in s_values:
            px, py = self.ref_spline.calc_position(s)
            if px is None or py is None:
                dists.append(float('inf'))
                continue
            dists.append(sqrt((px - x)**2 + (py - y)**2))
        min_index = np.argmin(dists)
        s = s_values[min_index]
        # 细化搜索
        ds = self.ref_spline.s[-1] / 1000
        for _ in range(10):
            s_low = max(0, s - ds)
            s_high = min(max_s, s + ds)
            pos_low = self.ref_spline.calc_position(s_low)
            if pos_low[0] is None:
                dist_low = float('inf')
            else:
                dist_low = sqrt((pos_low[0] - x)**2 + (pos_low[1] - y)**2)
            pos_high = self.ref_spline.calc_position(s_high)
            if pos_high[0] is None:
                dist_high = float('inf')
            else:
                dist_high = sqrt((pos_high[0] - x)**2 + (pos_high[1] - y)**2)
            pos_s = self.ref_spline.calc_position(s)
            if pos_s[0] is None:
                dist_s = float('inf')
            else:
                dist_s = sqrt((pos_s[0] - x)**2 + (pos_s[1] - y)**2)
            if dist_low < dist_s:
                s = s_low
            elif dist_high < dist_s:
                s = s_high
            ds /= 2
        return s

    def _calc_l(self, x, y, s):
        """计算横向偏移l"""
        if not self.ref_spline:
            return 0.0
        s = np.clip(s, 0, self.ref_spline.s[-1] - 1e-10)
        ref_x, ref_y = self.ref_spline.calc_position(s)
        if ref_x is None or ref_y is None:
            return 0.0
        yaw = self.ref_spline.calc_yaw(s)
        dx = x - ref_x
        dy = y - ref_y
        l = dx * cos(yaw + pi / 2) + dy * sin(yaw + pi / 2)
        return l
