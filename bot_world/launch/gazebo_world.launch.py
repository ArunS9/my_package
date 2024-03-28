#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Get the path to the Gazebo world file
    world_file_path = os.path.join(get_package_share_directory('bot_world'), 'worlds', 'my_world.world')

    return LaunchDescription([
        # Launch Gazebo with the specified world file
        Node(
            package='gazebo_ros',
            executable='gazebo',
            name='gazebo',
            output='screen',
            arguments=['-s', 'libgazebo_ros_factory.so', world_file_path]
        ),
        # Spawn the robot model using Xacro
        Node(
            package='xacro',
            executable='xacro',
            name='xacro',
            output='screen',
            arguments=[os.path.join(get_package_share_directory('bot_world'), 'description', 'robot.urdf.xacro')],
            remappings=[
                ('robot_description', '/robot_description')
            ]
        ),
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            name='spawn_entity',
            output='screen',
            arguments=['-entity', 'my_robot', '-x', '0', '-y', '0', '-z', '0', '-robot_namespace', '', '-reference_frame', 'world', '-urdf', '/robot_description']
        )
    ])


