#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

class ArmController(Node):
    def __init__(self):
        super().__init__('arm_controller')

        self.joint_pub = self.create_publisher(JointState, 'joint_states', 10)
        self.sub = self.create_subscription(JointState, 'joint_commands', self.callback, 10)
        self.get_logger().info('Bridge joint_commands → joint_states ready')

    def callback(self, msg):
        js = JointState()
        js.header = msg.header
        js.name = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5']
        js.position = msg.position + [0.0]  # joint5 gripper fixed
        js.velocity = []
        self.joint_pub.publish(js)
        self.get_logger().debug(f'Published {js.position[:4]}')

def main():
    rclpy.init()
    node = ArmController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
