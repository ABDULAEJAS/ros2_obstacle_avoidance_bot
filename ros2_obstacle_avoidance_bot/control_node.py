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

from typing import List, Optional

from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class ControlNode(Node):
    """ROS 2 Node for proactive obstacle avoidance and autonomous vacuum navigation."""

    def __init__(self) -> None:
        """Initialize ControlNode, subscribers, publisher, and control timer."""
        super().__init__('control_node')

        self.front_dist: float = float('inf')
        self.left_dist: float = float('inf')
        self.right_dist: float = float('inf')

        self.create_subscription(Float32, '/obstacle_distance', self.front_cb, 10)
        self.create_subscription(Float32, '/obstacle_distance_left', self.left_cb, 10)
        self.create_subscription(Float32, '/obstacle_distance_right', self.right_cb, 10)

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.05, self.control_loop)

        # 0.50m safety threshold (0.20m robot radius + 0.30m safe buffer)
        self.safe_threshold: float = 0.50
        self.get_logger().info('Proactive Obstacle Avoidance Controller Started.')

    def front_cb(self, msg: Float32) -> None:
        """Update front sector distance."""
        self.front_dist = msg.data

    def left_cb(self, msg: Float32) -> None:
        """Update left sector distance."""
        self.left_dist = msg.data

    def right_cb(self, msg: Float32) -> None:
        """Update right sector distance."""
        self.right_dist = msg.data

    def control_loop(self) -> None:
        """Periodic 20Hz control loop evaluating sector distances and publishing Twist."""
        twist = Twist()

        if self.front_dist <= self.safe_threshold:
            twist.linear.x = 0.0

            if self.left_dist >= self.right_dist:
                self.get_logger().warn(
                    f'Obstacle ahead ({self.front_dist:.2f}m)! Turning LEFT.'
                )
                twist.angular.z = 1.0
            else:
                self.get_logger().warn(
                    f'Obstacle ahead ({self.front_dist:.2f}m)! Turning RIGHT.'
                )
                twist.angular.z = -1.0
        else:
            twist.linear.x = 0.22
            twist.angular.z = 0.0

        self.cmd_pub.publish(twist)


def main(args: Optional[List[str]] = None) -> None:
    """Run the main entrypoint spinning ControlNode."""
    rclpy.init(args=args)
    node = ControlNode()
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
