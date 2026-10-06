<div align="center">
  <img src="asset/ONSITE-blue-logo-cn_name.svg" alt="OnSite" width="760">

# Background Vehicle Customization for the Onsite Real-Vehicle Competition's Virtual–Physical Fusion Injection System

<p>
  <strong>English</strong> · <a href="README_zh.md">中文</a>
</p>
</div>

<div align="center">
<a href="https://onsite.com.cn/"><img src="https://img.shields.io/badge/OnSite-3.0-blue"></a>
&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://tops.tongji.edu.cn/"><img src="https://img.shields.io/badge/TCU-TOPS-purple"></a>
&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://arxiv.org/abs/2512.07507"><img src="https://img.shields.io/badge/Paper-arxiv-red"></a>
&nbsp;&nbsp;&nbsp;&nbsp;
<a href="./LICENSE"><img src="https://img.shields.io/badge/LICENSE-Apache License 2.0-lightgray"></a>
</div>

## Project Overview

A simulated vehicle control program based on Redis publish/subscribe messaging. Through `main.py`, the repository listens for control messages, vehicle location messages, and scenario change messages from the simulation platform. It then selects the appropriate controller based on the scenario ID and continuously outputs control commands for the specified vehicles.

The project's current core features are:

- Interaction with an external simulation platform through `Redis`
- Global path generation by extracting road or lane centerlines from `map/TJ-map.json`
- Selection of different controllers and path configurations based on the scenario ID
- Generation of the next target point using a spline reference line and a lattice planner within each controller
- Support for scenario configurations such as basic path tracking, path stitching for lane changes, and local point offsets

## Table of Contents

- [1 Environment Setup](#jump1)
- [2 Project Structure](#jump2)
- [3 How It Works](#jump3)
- [4 Controllers](#jump4)
- [5 Running the Program](#jump5)
- [6 Message Formats and Integration Testing](#jump6)
- [7 Acknowledgments](#jump7)
- [8 Changelog](#jump8)

<a id="jump1"></a>

## 1 Environment Setup

### 1.1 Installing Dependencies

Python 3.10 or later is recommended. Create an environment with conda, then install the dependencies:

```bash
conda create -n onsite python=3.10
conda activate onsite
pip install -r requirements.txt
```

### 1.2 Redis Connection Configuration

The Redis connection settings are located in `SIM_CONTROLLER_CONFIG["redis"]` in [config.py](./config.py) and include:

- `host`
- `port`
- `password`

To switch to a different environment, update these settings before starting the program.

<a id="jump2"></a>

## 2 Project Structure

The repository's current directory structure is as follows:

```text
VP-AutoTest-BV-Controller/
├─ controllers/
│  ├─ BaseController.py
│  ├─ alg1/
│  │  ├─ Controller1.py
│  │  ├─ cubic_spline.py
│  │  ├─ lattice_planner.py
│  │  ├─ quartic_polynomial.py
│  │  └─ quintic_polynomial.py
│  ├─ alg2/
│  │  ├─ Controller2.py
│  │  ├─ cubic_spline.py
│  │  ├─ lattice_planner.py
│  │  ├─ quartic_polynomial.py
│  │  └─ quintic_polynomial.py
│  └─ alg3/
│     ├─ Controller3.py
│     ├─ cubic_spline.py
│     ├─ lattice_planner.py
│     ├─ quartic_polynomial.py
│     └─ quintic_polynomial.py
├─ doc/
│  └─ 场景注入机使用和配置教程.pdf
├─ map/
│  └─ TJ-map.json
├─ config.py
├─ main.py
├─ requirements.txt
├─ test.py
├─ README.md
└─ README_zh.md
```

### 2.1 Key Files

| File | Description |
| --- | --- |
| [main.py](./main.py) | Main entry point, responsible for subscribing to Redis messages, switching scenarios, creating controllers, and publishing control commands |
| [config.py](./config.py) | Central configuration for scenario definitions, controller mappings, lists of road elements, Redis settings, and more |
| [controllers/BaseController.py](./controllers/BaseController.py) | Abstract controller base class defining the `set_route_points` and `get_next_action` interfaces |
| `controllers/alg1/` | First control strategy, including slowdown zones and speed adjustment logic for turns |
| `controllers/alg2/` | Second control strategy, performing basic lattice path tracking |
| `controllers/alg3/` | Third control strategy, currently largely identical to `alg2`, providing a starting point for future extensions |
| `doc/` | Project documentation directory, currently containing `场景注入机使用和配置教程.pdf` (Scenario Injection System Usage and Configuration Tutorial) as a reference for configuration and use |
| `map/TJ-map.json` | Road network data file; the program generates global paths from its road and lane information |
| [test.py](./test.py) | A local integration testing script that sends an HTTP simulation start request to `127.0.0.1:7778` |

<a id="jump3"></a>

## 3 How It Works

### 3.1 Main Workflow

`SimVehController` in [main.py](./main.py) is the main control object for the entire system. When the program starts, it:

1. Reads the global configuration from [config.py](./config.py)
2. Loads the `map/TJ-map.json` road network file
3. Generates a global reference path based on the default scenario
4. Subscribes to the main entry channel, `algorithm`
5. Reports heartbeats, starts control, or switches scenarios according to the type of message received

### 3.2 Generating Paths from Scenario Configurations

Each scenario is defined in `SCENARIO_DEFINITIONS`, primarily with the following fields:

- `id`: Scenario ID
- `controller`: Controller class used by the scenario
- `control_enabled`: Whether algorithm control is enabled for the scenario
- `is_default`: Whether this is the default scenario
- `config`: Path construction parameters

The `config` field controls the following behavior:

- `element_ids`: List of road IDs to connect in sequence
- `lane_numbers`: Lane number to use for each road
- `use_lane_switching`: Whether to alternate points between two adjacent lane centerlines to generate a lane change path
- `apply_offset`: Whether to apply a lateral offset to the first few points of specified roads
- `offset_roads` / `offset_count` / `y_offset`: Offset details

The program uses `_get_route_points_from_elements()` to convert these settings into a list of `Point` objects, which is then passed to the controller to generate a reference spline.

### 3.3 Control Message Processing

The main program handles three types of messages:

- `type == 1`: Starts a heartbeat thread that periodically sends device status to the status channel
- `type == 2`: Starts control, records which vehicles are taken over by the current algorithm, and starts a location subscription thread
- `type == 3`: Switches scenarios, reapplies the scenario configuration, rebuilds the path, and clears existing controller instances

Upon receiving a vehicle location message, the program:

1. Collects the positions and speeds of all vehicles and organizes them into an obstacle array
2. Filters for vehicles that need to be controlled by the algorithm
3. Selects the controller class based on the current scenario ID
4. Creates a controller for each new vehicle and supplies the current global path
5. Calls `get_next_action(...)` to generate control output
6. Packages the control results for multiple vehicles and publishes them to the control channel

<a id="jump4"></a>

## 4 Controllers

### 4.1 Common Controller Interface

All controllers inherit from [controllers/BaseController.py](./controllers/BaseController.py) and must implement two core interfaces:

- `set_route_points(route_points)`: Receives global path points and builds an internal reference line
- `get_next_action(current_x, current_y, speed, accel, angle, obstacles=None)`: Returns the next `Action` based on the current state

The main fields currently used in the `Action` model are:

- `type=1`: Position control
- `lon` / `lat`: Coordinates of the next target point
- `remove=True`: Indicates that the vehicle has reached the endpoint and can be removed from the control list

### 4.2 Controller1

[controllers/alg1/Controller1.py](./controllers/alg1/Controller1.py) adds speed adjustment logic to basic lattice path tracking:

- Uses `slow_roads` to mark road segments that require special handling
- Uses `_update_road_status()` to roughly determine the vehicle's current path segment
- Sets slowdown zones at specified road connections
- Uses a lower target speed during turns

The default speed parameters are:

- `normal_speed = 12.0 / 3.6`
- `transition_speed = 8.0 / 3.6`
- `slow_speed = 4.5 / 3.6`

Scenario `id=3` in the current `config.py` uses this controller.

### 4.3 Controller2

[controllers/alg2/Controller2.py](./controllers/alg2/Controller2.py) is a more straightforward reference line tracking implementation with the following workflow:

1. Removes duplicate path points
2. Generates a spline reference line from the path points
3. Uses `_find_s()` to find the nearest arc-length position on the reference line for the vehicle
4. Uses `_calc_l()` to estimate the lateral offset
5. Calls `lattice_planner_for_Cruising(...)` to generate a local trajectory
6. Outputs the next target point from the local trajectory, one point at a time

The implementation already includes an `obstacles` parameter, but the current version fixes `C.obs` to an empty array, so obstacle avoidance is not actually enabled.

Scenario `id=9` in the current `config.py` uses this controller.

### 4.4 Controller3

The current implementation of [controllers/alg3/Controller3.py](./controllers/alg3/Controller3.py) is largely identical to `Controller2`, with the following main characteristics:

- Also outputs the next target position using a reference spline and lattice planner
- Also returns `remove=True` when the vehicle is within 1 meter of the endpoint
- Also provides an `obstacles` input, but does not actually load obstacles in the current implementation
- Provides a starting point for experiments with a third algorithm, allowing further development without affecting `alg1` or `alg2`

Note that `Controller3` is implemented in the repository but has not yet been registered in `SCENARIO_DEFINITIONS` in [config.py](./config.py), so the default workflow will not use it automatically. To enable it, add a new scenario configuration and set `controller` to `Controller3`.

<a id="jump5"></a>

## 5 Running the Program

### 5.1 Starting the Main Control Program

```bash
python main.py
```

When the program starts, it:

- Connects to Redis
- Loads the map
- Applies the default scenario configuration
- Continuously listens for messages on the `algorithm` channel

### 5.2 Changing the Default Scenario or Controller Mapping

To change the default behavior, edit `SCENARIO_DEFINITIONS` in [config.py](./config.py). The currently included scenarios are:

| Scenario ID | Controller | Enabled by Default | Path Characteristics |
| --- | --- | --- | --- |
| `3` | `Controller1` | Yes | Fixed-lane path, with a `y`-direction offset applied to the first few points of some roads |
| `9` | `Controller2` | No | Alternates points between lanes to form a lane change path |

To enable `Controller3`, append a new scenario using the existing format, for example:

```python
from controllers.alg3.Controller3 import Controller3

{
    "id": 10,
    "controller": Controller3,
    "control_enabled": True,
    "is_default": False,
    "config": {
        "element_ids": [...],
        "lane_numbers": [...],
        "use_lane_switching": False,
        "apply_offset": False,
        "offset_roads": [],
        "offset_count": 0,
        "y_offset": 0.0,
    },
}
```

### 5.3 Using the Integration Testing Script

[test.py](./test.py) can send a sample simulation start request to a local service:

```bash
python test.py
```

The script's default request URL is:

```text
http://127.0.0.1:7778/jd/startTessng
```

It is best suited to integration testing examples or verifying API connectivity, and is not part of the main control logic in `main.py`.

<a id="jump6"></a>

## 6 Message Formats and Integration Testing

### 6.1 Subscription Entry Point

The channel to which the program subscribes by default is determined by the following setting in [config.py](./config.py):

```python
"channels": {"subscribe": "algorithm"}
```

### 6.2 Start Control Message

When a message with `type == 2` is received, the program primarily reads the following fields:

- `locationChannel`
- `controlChannel`
- `vehPointsMapping`

The keys in `vehPointsMapping` are parsed into the set of vehicle IDs to be taken over by the algorithm. Controller instances are created only for these vehicles.

### 6.3 Location Messages

Location messages are parsed as the `msg_data["value"]["value"]` list. Each vehicle object must contain at least the following fields:

- `originId`
- `number`
- `x`
- `y`
- `speed`
- `acceleration`
- `courseAngle`
- `driveType`
- `controlType`

The filtering rules are:

- Vehicles with `driveType == 1` are excluded from control
- Vehicles with `controlType == 0` are excluded from control
- Vehicles outside the set specified by `vehPointsMapping` are excluded from control

### 6.4 Control Output

Control results are assembled into the following structure and then published:

```json
{
  "params": [
    {
      "id": 101,
      "number": 1,
      "type": 1,
      "lon": 123.45,
      "lat": 67.89,
      "remove": false
    }
  ]
}
```

<a id="jump7"></a>

## 7 Acknowledgments

We sincerely thank the Department of Engineering and Materials Sciences of the National Natural Science Foundation of China and the China Society of Automotive Engineers for their support, and the [TOPS research group](https://tops.tongji.edu.cn/index.htm) for its collective efforts and outstanding contributions.

<a id="jump8"></a>

## 8 Changelog

### [2026-04-24]

- Added a description of the `doc/` documentation directory
- Added the `场景注入机使用和配置教程.pdf` entry to the project structure

### [2026-04-20]

- Initial code upload
- Added the project description, environment setup, and data organization details
