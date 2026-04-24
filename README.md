<div align="center">
  <img src="asset/ONSITE-blue-logo-cn_name.svg" alt="OnSite" width="760">

# Onsite 实车赛虚实融合注入机背景车二次开发
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

## 项目概述
基于 Redis 消息订阅/发布的仿真车辆控制程序。仓库通过 `main.py` 监听仿真平台下发的控制消息、车辆定位消息和场景切换消息，再按场景编号选择对应控制器，为指定车辆持续输出控制指令。

当前项目的核心特点如下：

- 使用 `Redis Pub/Sub` 与外部仿真平台交互
- 从 `map/TJ-map.json` 中提取道路或车道中心线生成全局路径
- 根据场景编号切换不同控制器与路径配置
- 控制器内部采用样条参考线 + lattice planner 生成下一时刻目标点
- 支持基础路径跟踪、变道型路径拼接、局部点偏移等场景配置能力

## 目录

- [1 环境配置](#jump1)
- [2 项目结构](#jump2)
- [3 运行机制说明](#jump3)
- [4 控制器说明](#jump4)
- [5 运行方式](#jump5)
- [6 消息格式与联调说明](#jump6)
- [7 输出与调试建议](#jump7)
- [8 变更日志](#jump8)

## <span id="jump1">1 环境配置

### 1.1 安装依赖

建议使用 Python 3.10 及以上版本，并通过 conda 创建环境后安装依赖：

```bash
conda create -n onsite python=3.10
conda activate onsite
pip install -r requirements.txt
```

### 1.2 Redis 连接配置

Redis 连接信息位于 [config.py](./config.py) 的 `SIM_CONTROLLER_CONFIG["redis"]` 中，包括：

- `host`
- `port`
- `password`

如需切换到其他环境，请先修改该配置，再启动程序。

## <span id="jump2">2 项目结构

当前仓库的实际目录结构如下：

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
├─ map/
│  └─ TJ-map.json
├─ config.py
├─ main.py
├─ requirements.txt
├─ test.py
└─ README.md
```

### 2.1 关键文件说明

| 文件 | 说明 |
| --- | --- |
| [main.py](./main.py) | 主程序入口，负责订阅 Redis 消息、切换场景、创建控制器并发布控制指令 |
| [config.py](./config.py) | 统一维护场景定义、控制器映射、道路元素列表、Redis 配置等 |
| [controllers/BaseController.py](./controllers/BaseController.py) | 控制器抽象基类，定义 `set_route_points` 和 `get_next_action` 接口 |
| `controllers/alg1/` | 第一套控制策略，包含减速区与转弯速度调整逻辑 |
| `controllers/alg2/` | 第二套控制策略，执行基础 lattice 路径跟踪 |
| `controllers/alg3/` | 第三套控制策略，当前实现与 `alg2` 基本一致，可作为后续扩展入口 |
| `map/TJ-map.json` | 路网数据文件，程序通过道路和车道信息生成全局路径 |
| [test.py](./test.py) | 一个本地联调脚本，通过 HTTP 向 `127.0.0.1:7778` 发送仿真启动请求 |

## <span id="jump3">3 运行机制说明

### 3.1 主流程

[main.py](./main.py) 中的 `SimVehController` 是整个系统的主控对象。程序启动后会：

1. 读取 [config.py](./config.py) 中的全局配置
2. 加载 `map/TJ-map.json` 路网文件
3. 根据默认场景生成一条全局参考路径
4. 订阅总入口通道 `algorithm`
5. 根据收到的消息类型，执行心跳上报、开始控制或切换场景

### 3.2 场景配置生成路径

每个场景在 `SCENARIO_DEFINITIONS` 中定义，主要包括：

- `id`：场景编号
- `controller`：该场景使用的控制器类
- `control_enabled`：该场景是否启用算法控制
- `is_default`：是否为默认场景
- `config`：路径构造参数

其中 `config` 会控制以下行为：

- `element_ids`：按顺序拼接的道路 ID 列表
- `lane_numbers`：每条道路对应使用的车道编号
- `use_lane_switching`：是否在两条相邻车道中心线之间交替取点，生成变道型路径
- `apply_offset`：是否对指定道路前若干个点施加横向偏移
- `offset_roads` / `offset_count` / `y_offset`：偏移细节

程序通过 `_get_route_points_from_elements()` 将这些配置转换为 `Point` 列表，再交给控制器生成参考样条。

### 3.3 控制消息处理逻辑

主程序会处理三类消息：

- `type == 1`：启动心跳线程，周期性向状态通道发送设备状态
- `type == 2`：开始控制，记录哪些车辆由当前算法接管，并启动定位订阅线程
- `type == 3`：切换场景，重新应用场景配置、重建路径并清空旧控制器实例

收到车辆定位消息后，程序会：

1. 收集所有车辆的位置和速度，组织为障碍物数组
2. 过滤出需要由算法控制的车辆
3. 按当前场景编号选择控制器类
4. 为新车辆创建控制器，并注入当前全局路径
5. 调用 `get_next_action(...)` 生成控制输出
6. 将多个车辆的控制结果打包后发布到控制通道

## <span id="jump4">4 控制器说明

### 4.1 控制器统一接口

所有控制器都继承自 [controllers/BaseController.py](./controllers/BaseController.py)，需要实现两个核心接口：

- `set_route_points(route_points)`：接收全局路径点并建立内部参考线
- `get_next_action(current_x, current_y, speed, accel, angle, obstacles=None)`：基于当前状态返回下一步 `Action`

`Action` 模型中当前主要使用的是：

- `type=1`：位置控制
- `lon` / `lat`：下一目标点坐标
- `remove=True`：表示车辆已到达终点，可从控制列表中移除

### 4.2 Controller1

[controllers/alg1/Controller1.py](./controllers/alg1/Controller1.py) 在基础 lattice 路径跟踪之外，额外加入了速度调节逻辑：

- 使用 `slow_roads` 标记需要重点处理的道路段
- 通过 `_update_road_status()` 粗略判断车辆当前所在路径段
- 在指定道路连接处设置减速区
- 在转弯阶段使用更低目标速度

默认速度参数如下：

- `normal_speed = 12.0 / 3.6`
- `transition_speed = 8.0 / 3.6`
- `slow_speed = 4.5 / 3.6`

当前 `config.py` 中场景 `id=3` 使用该控制器。

### 4.3 Controller2

[controllers/alg2/Controller2.py](./controllers/alg2/Controller2.py) 是一套更直接的参考线跟踪实现，流程为：

1. 清理重复路径点
2. 基于路径点生成样条参考线
3. 通过 `_find_s()` 找到车辆在参考线上的最近弧长位置
4. 通过 `_calc_l()` 估计横向偏移
5. 调用 `lattice_planner_for_Cruising(...)` 生成局部轨迹
6. 逐点输出局部轨迹中的下一个目标点

实现中已经预留了 `obstacles` 参数，但当前版本将 `C.obs` 固定置为空数组，没有实际启用障碍物避让。

当前 `config.py` 中场景 `id=9` 使用该控制器。

### 4.4 Controller3

[controllers/alg3/Controller3.py](./controllers/alg3/Controller3.py) 的当前实现与 `Controller2` 基本一致，主要特点如下：

- 同样基于参考样条和 lattice planner 输出下一目标位置
- 同样会在到达终点 1 米范围内返回 `remove=True`
- 同样预留了 `obstacles` 输入，但当前实现中未真正加载障碍物
- 适合作为第三套算法的实验入口，在不影响 `alg1`、`alg2` 的前提下继续演化

需要注意的是：`Controller3` 已经在仓库中实现，但尚未在 [config.py](./config.py) 的 `SCENARIO_DEFINITIONS` 中注册，因此默认运行流程不会自动使用它。如果需要启用，需要新增一个场景配置并将 `controller` 指向 `Controller3`。

## <span id="jump5">5 运行方式

### 5.1 启动主控制程序

```bash
python main.py
```

程序启动后会：

- 连接 Redis
- 加载地图
- 应用默认场景配置
- 持续监听 `algorithm` 通道消息

### 5.2 修改默认场景或控制器映射

如需变更默认行为，请编辑 [config.py](./config.py) 中的 `SCENARIO_DEFINITIONS`。当前内置场景为：

| 场景 ID | 控制器 | 默认启用 | 路径特征 |
| --- | --- | --- | --- |
| `3` | `Controller1` | 是 | 固定车道路径，且对部分道路前几个点施加 `y` 方向偏移 |
| `9` | `Controller2` | 否 | 启用车道交替取点，形成变道型路径 |

如果要启用 `Controller3`，可按现有格式追加一个新场景，例如：

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

### 5.3 使用联调脚本

[test.py](./test.py) 可用于向本机服务发送一个示例仿真启动请求：

```bash
python test.py
```

该脚本默认请求地址为：

```text
http://127.0.0.1:7778/jd/startTessng
```

它更适合做联调示例或接口调通，不参与 `main.py` 的主控制逻辑。

## <span id="jump6">6 消息格式与联调说明

### 6.1 订阅入口

程序默认订阅通道由 [config.py](./config.py) 中的以下配置决定：

```python
"channels": {"subscribe": "algorithm"}
```

### 6.2 开始控制消息

当收到 `type == 2` 的消息时，程序会重点读取以下字段：

- `locationChannel`
- `controlChannel`
- `vehPointsMapping`

其中 `vehPointsMapping` 的 key 会被解析为需要由算法接管的车辆 ID 集合，只有这些车辆才会创建控制器实例。

### 6.3 定位消息

定位消息会被解析为 `msg_data["value"]["value"]` 列表，每个车辆对象至少需要包含：

- `originId`
- `number`
- `x`
- `y`
- `speed`
- `acceleration`
- `courseAngle`
- `driveType`
- `controlType`

过滤规则如下：

- `driveType == 1` 的车辆不参与控制
- `controlType == 0` 的车辆不参与控制
- 不在 `vehPointsMapping` 指定范围内的车辆不参与控制

### 6.4 控制输出

控制结果会组装为如下结构后发布：

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

## <span id="jump7">7 致谢

衷心感谢国家自然科学基金委员会工程与材料科学部和中国汽车工程学会的支持以及[TOPS课题组](https://tops.tongji.edu.cn/index.htm)的集体努力与卓越贡献。

## <span id="jump8">8 变更日志

### [2026-04-20]

- 代码首次上传
- 补充项目说明、环境配置和数据组织方式
