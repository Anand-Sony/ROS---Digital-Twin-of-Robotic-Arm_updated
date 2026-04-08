#!/usr/bin/env python3
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
import os

def generate_launch_description():
    serial_port_arg = DeclareLaunchArgument(
        'serial_port',
        default_value='/dev/ttyUSB0',
        description='Serial port for ESP32'
    )
    
    baudrate_arg = DeclareLaunchArgument(
        'baudrate',
        default_value='115200',
        description='Serial baudrate'
    )

    twin_description_dir = get_package_share_directory("twin_description")

    robot_description_content = ParameterValue(Command([
        'xacro', ' ',
        os.path.join(twin_description_dir, 'urdf', 'twin.urdf.xacro'),
    ]))

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_content,
                     'use_sim_time': False}]
    )

    serial_reader_node = Node(
        package='twin_firmware',  
        executable='serial_reader.py',
        name='pot_serial_reader',
        output='screen',
        parameters=[{
            'port': LaunchConfiguration('serial_port'),
            'baudrate': LaunchConfiguration('baudrate'),
        }]
    )

    return LaunchDescription([
        serial_port_arg,
        baudrate_arg,
        robot_state_publisher_node,
        serial_reader_node
    ])
