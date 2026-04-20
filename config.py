from controllers.alg1.Controller1 import Controller1
from controllers.alg2.Controller2 import Controller2


SCENARIO_DEFINITIONS = [
    {
        "id": 3,
        "controller": Controller1,
        "control_enabled": True,
        "is_default": True,
        "config": {
            "element_ids": [1036, 739, 1027, 122, 708, 713],
            "lane_numbers": [0, 0, 0, 2, 1, 1],
            "use_lane_switching": False,
            "apply_offset": True,
            "offset_roads": [739, 1027],
            "offset_count": 5,
            "y_offset": 2.0,
        },
    },
    {
        "id": 9,
        "controller": Controller2,
        "control_enabled": True,
        "is_default": False,
        "config": {
            "element_ids": [727, 730],
            "lane_numbers": [0, 0],
            "use_lane_switching": True,
            "apply_offset": False,
            "offset_roads": [],
            "offset_count": 0,
            "y_offset": 0.0,
        },
    },
]


def _get_default_scenario_id() -> int:
    for scenario in SCENARIO_DEFINITIONS:
        if scenario.get("is_default"):
            return scenario["id"]
    return SCENARIO_DEFINITIONS[0]["id"]


SCENARIO_CONFIGS = {item["id"]: item["config"] for item in SCENARIO_DEFINITIONS}
CONTROLLER_CLASS_MAPPING = {
    item["id"]: item["controller"]
    for item in SCENARIO_DEFINITIONS
    if item.get("controller") is not None
}
CONTROL_SCENARIOS = {
    item["id"] for item in SCENARIO_DEFINITIONS if item.get("control_enabled", False)
}


SIM_CONTROLLER_CONFIG = {
    "device_id": 12032,
    "redis": {
        "host": "100.84.159.241",
        "port": 6379,
        "password": "Wanji@300552!",
    },
    "channels": {"subscribe": "algorithm"},
    "road_network_file": "map/YYT_TJST_unlimited.json",
    "control_scenarios": list(CONTROL_SCENARIOS),
    "default_scenario": _get_default_scenario_id(),
    "controller_class_mapping": CONTROLLER_CLASS_MAPPING,
    "scenario_configs": SCENARIO_CONFIGS,
}