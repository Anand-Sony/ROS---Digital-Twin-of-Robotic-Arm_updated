#!/usr/bin/env python3
import serial
import rclpy
import math
from rclpy.node import Node
from sensor_msgs.msg import JointState
import re

class ServoSerialReader(Node):
    def __init__(self):
        super().__init__('servo_serial_reader')
        self.joint_positions = [0.0] * 5  # joint_1 to joint_5
        self.serial_ok = False

        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)
        port = self.get_parameter('port').value
        baud = self.get_parameter('baudrate').value

        self.pub = self.create_publisher(JointState, '/joint_states', 10)

        try:
            self.arduino = serial.Serial(port, baud, timeout=0.1)
            self.arduino.flush()
            self.serial_ok = True
            self.get_logger().info(f'Serial connected to {port} @ {baud}')
        except Exception as e:
            self.get_logger().warn(f'Serial connect failed: {e}')

        self.timer = self.create_timer(0.05, self.timer_callback)  # 20Hz

    def deg_to_rad(self, deg):
        return (deg - 90.0) * math.pi / 180.0

    def parse_arduino_line(self, line):
        # Match "S1: 90 | S2: 90 | S3: 90 | S4: 90"
        match = re.match(r'S1:\s*([\d.]+)\s*\|\s*S2:\s*([\d.]+)\s*\|\s*S3:\s*([\d.]+)\s*\|\s*S4:\s*([\d.]+)', line)
        if match:
            s1, s2, s3, s4 = map(float, match.groups())
            self.get_logger().info(f"Angles - S1:{s1:.1f} S2:{s2:.1f} S3:{s3:.1f} S4:{s4:.1f}")
            # Map servo to joints: s1->joint_3 (adj grip), s2->joint_1 (base), s3->joint_2 (adj base), s4->joint_4 (gripper)
            self.joint_positions[0] = self.deg_to_rad(s2)  # joint_1 = s2 base
            self.joint_positions[1] = self.deg_to_rad(s3)  # joint_2 = s3 adj base
            self.joint_positions[2] = self.deg_to_rad(s1)  # joint_3 = s1 adj gripper
            self.joint_positions[3] = self.deg_to_rad(s4)  # joint_4 = s4 gripper
            self.joint_positions[4] = -self.joint_positions[3]  # joint_5 mimic
            return True
        return False

    def timer_callback(self):
        if self.serial_ok and self.arduino:
            try:
                line = self.arduino.readline().decode('utf-8').strip()
                if line and self.parse_arduino_line(line):
                    # Publish
                    msg = JointState()
                    msg.header.stamp = self.get_clock().now().to_msg()
                    msg.name = ['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5']
                    msg.position = self.joint_positions
                    self.pub.publish(msg)
            except Exception as e:
                self.get_logger().debug(f'Serial read err: {e}')

def main():
    rclpy.init()
    node = ServoSerialReader()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

