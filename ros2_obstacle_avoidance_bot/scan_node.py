# Copyright 2026 Amin Ahmed G
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math
from typing import List, Optional

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32


class ScanNode(Node):
    """ROS 2 Node for processing 360-degree LiDAR scans into sector distances."""

    def __init__(self) -> None:
        """Initialize ScanNode, subscribers, and publishers."""
        super().__init__('scan_node')
        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )
        self.front_dist_pub = self.create_publisher(Float32, '/obstacle_distance', 10)
        self.left_dist_pub = self.create_publisher(Float32, '/obstacle_distance_left', 10)
        self.right_dist_pub = self.create_publisher(Float32, '/obstacle_distance_right', 10)
        self.get_logger().info('Accurate 360 LiDAR Scan Node Started.')

    def scan_callback(self, msg: LaserScan) -> None:
        """Process incoming LaserScan and calculate minimum distance in 3 sectors."""
        if not msg.ranges:
            return

        angles = [
            msg.angle_min + i * msg.angle_increment for i in range(len(msg.ranges))
        ]

        front_ranges: List[float] = []
        left_ranges: List[float] = []
        right_ranges: List[float] = []

        for r, angle in zip(msg.ranges, angles):
            if r < msg.range_min or r > msg.range_max or math.isnan(r) or math.isinf(r):
                continue

            # Front Sector: -30 deg to +30 deg (-0.52 rad to +0.52 rad)
            if -0.52 <= angle <= 0.52:
                front_ranges.append(r)
            # Left Sector: +30 deg to +90 deg (+0.52 rad to +1.57 rad)
            elif 0.52 < angle <= 1.57:
                left_ranges.append(r)
            # Right Sector: -90 deg to -30 deg (-1.57 rad to -0.52 rad)
            elif -1.57 <= angle < -0.52:
                right_ranges.append(r)

        min_front = min(front_ranges) if front_ranges else float('inf')
        min_left = min(left_ranges) if left_ranges else float('inf')
        min_right = min(right_ranges) if right_ranges else float('inf')

        self.front_dist_pub.publish(Float32(data=float(min_front)))
        self.left_dist_pub.publish(Float32(data=float(min_left)))
        self.right_dist_pub.publish(Float32(data=float(min_right)))


def main(args: Optional[List[str]] = None) -> None:
    """Run the main entrypoint spinning ScanNode."""
    rclpy.init(args=args)
    node = ScanNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
