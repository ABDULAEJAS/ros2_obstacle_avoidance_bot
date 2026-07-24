# ROS 2 Obstacle Avoidance Bot (`ros2_obstacle_avoidance_bot`)

An autonomous differential-drive robot simulation built for **ROS 2 (Jazzy / Humble)** and **Gazebo Sim**. Features 360-degree GPU LiDAR perception, 3-sector distance processing, and proactive obstacle avoidance motion control.

---

## Technical Overview

```
                        +----------------------------+
                        |  Gazebo GPU LiDAR (/scan)  |
                        +--------------+-------------+
                                       |
                                       v
                        +--------------+-------------+
                        |   ScanNode (360 LiDAR)     |
                        |  - Front Sector (-30°..+30°)|
                        |  - Left Sector  (+30°..+90°)|
                        |  - Right Sector (-90°..-30°)|
                        +--------------+-------------+
                                       |
               +-----------------------+-----------------------+
               |                       |                       |
               v                       v                       v
      /obstacle_distance    /obstacle_distance_left  /obstacle_distance_right
               |                       |                       |
               +-----------------------+-----------------------+
                                       |
                                       v
                        +--------------+-------------+
                        | ControlNode (Avoidance)    |
                        | - Safe Threshold: 0.50m    |
                        | - Proactive Steer Decision |
                        +--------------+-------------+
                                       |
                                       v
                             /cmd_vel (Twist)
                                       |
                                       v
                        +--------------+-------------+
                        |   ros_gz_bridge & Gazebo    |
                        +----------------------------+
```

### System Architecture

1. **`ScanNode` (`ros2_obstacle_avoidance_bot/scan_node.py`)**:
   - Subscribes to 360-degree LiDAR scans (`/scan`).
   - Filters out invalid/NaN/Inf ray readings.
   - Evaluates minimum obstacle clearance across three distinct sectors:
     - **Front Sector**: $[-0.52\,\text{rad}, +0.52\,\text{rad}]$ ($-30^\circ$ to $+30^\circ$)
     - **Left Sector**: $[+0.52\,\text{rad}, +1.57\,\text{rad}]$ ($+30^\circ$ to $+90^\circ$)
     - **Right Sector**: $[-1.57\,\text{rad}, -0.52\,\text{rad}]$ ($-90^\circ$ to $-30^\circ$)
   - Publishes sector clearance distances on `/obstacle_distance`, `/obstacle_distance_left`, and `/obstacle_distance_right`.

2. **`ControlNode` (`ros2_obstacle_avoidance_bot/control_node.py`)**:
   - Runs a 20Hz closed-loop reactive navigation controller.
   - Evaluates a **0.50m safety threshold** ($0.20\text{m robot radius} + 0.30\text{m buffer}$).
   - Automatically steers toward the sector with maximum open space when an obstacle is detected ahead.

3. **Cybertruck Vehicle Model (`urdf/`)**:
   - Metallic stainless steel chassis (`#C0C5C8`), front cyan LED headlight strip, rear red LED taillight, and matte black wheels.
   - Gazebo Sim differential drive plugin publishing odometry on `/odom` and TF transforms on `/tf`.

---

## Prerequisites

- **ROS 2**: Jazzy Jalisco or Humble Hawksbill
- **Gazebo Sim**: Harmonic / Fortress
- **Python**: 3.10+
- **ROS 2 Packages**: `ros_gz_bridge`, `ros_gz_sim`, `xacro`, `robot_state_publisher`

---

## Installation & Build

```zsh
source /opt/ros/jazzy/setup.zsh
mkdir -p ~/obstacle_bot_ws/src
cd ~/obstacle_bot_ws/src
git clone https://github.com/Amin-Ahmed-G/ros2_obstacle_avoidance_bot.git

cd ~/obstacle_bot_ws
colcon build --symlink-install
source install/setup.zsh
```

---

## Running the Simulation

To launch Gazebo Sim, the Cybertruck spawn, parameter bridge, LiDAR scan node, and obstacle avoidance control node:

```zsh
source /opt/ros/jazzy/setup.zsh
cd ~/obstacle_bot_ws
source install/setup.zsh

ros2 launch ros2_obstacle_avoidance_bot gazebo.launch.py
```

---

## Verification & Testing

To run the unit test and linter suite:

```zsh
cd ~/obstacle_bot_ws
colcon test --packages-select ros2_obstacle_avoidance_bot
colcon test-result --all --verbose
```

---

## Author & Maintainer

- **Amin Ahmed G**
- GitHub: [github.com/Amin-Ahmed-G](https://github.com/Amin-Ahmed-G)
- Email: aminahmedg2005@gmail.com
