from typing import List
from abc import ABC, abstractmethod
from pydantic import BaseModel


class Point(BaseModel):
	x: float
	y: float


class Action(BaseModel):
	type: int  # 1：位置；2：绝对加速度；3：相对加速度；4：速度
	lon: float = 0.0
	lat: float = 0.0
	xAcce: float = 0.0
	yAcce: float = 0.0
	zAcce: float = 0.0
	xAcceForVehi: float = 0.0
	yAcceForVehi: float = 0.0
	zAcceForVehi: float = 0.0
	xSpeed: float = 0.0
	ySpeed: float = 0.0
	zSpeed: float = 0.0
	remove: bool = False


class BaseController(ABC):
	def __init__(self):
		self.current_x = None
		self.current_y = None
		self.current_speed = None
		self.current_accel = None
		self.current_angle = None
		self.next_x = None
		self.next_y = None
		self.next_speed = None
		self.next_accel = None
		self.next_angle = None

	@abstractmethod
	def set_route_points(self, route_points: List[Point]) -> None:
		pass

	@abstractmethod
	def get_next_action(self, current_x: float, current_y: float, current_speed: float, current_accel: float, current_angle: float) -> Action:
		pass
