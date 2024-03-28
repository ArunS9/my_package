import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from xacro import process_file

def generate_launch_description():
    # Get the path to the world file
    world_file_name = 'my_world.world'
    world_file_path = os.path.join(get_package_share_directory('bot_world'), 'worlds', world_file_name)

    # Launch Gazebo
    gazebo_node = Node(
        package='gazebo_ros',
        executable='gazebo',
        name='gazebo',
        output='screen',
        arguments=['-s', 'libgazebo_ros_factory.so', world_file_path]
    )

    # Convert Xacro to URDF
    xacro_file_path = os.path.join(get_package_share_directory('bot_description'), 'description', 'robot.urdf.xacro')
    urdf_file_path = os.path.join(get_package_share_directory('bot_description'), 'description', 'robot.urdf')
    process_file(xacro_file_path, output=urdf_file_path)

    # Spawn the robot URDF model
    robot_spawner_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': True}],
        arguments=[urdf_file_path]
    )

    return LaunchDescription([gazebo_node, robot_spawner_node])

