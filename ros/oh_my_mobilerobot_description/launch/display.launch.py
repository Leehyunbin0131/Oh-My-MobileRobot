"""Display a generated URDF in ROS 2. SPDX-License-Identifier: CERN-OHL-P-2.0."""
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def setup(context):
    share = Path(get_package_share_directory('oh_my_mobilerobot_description'))
    variant = LaunchConfiguration('variant').perform(context)
    supplied_model = LaunchConfiguration('model').perform(context)
    model = Path(supplied_model) if supplied_model else share / 'urdf' / f'{variant}.urdf'
    description = model.read_text(encoding='utf-8')
    use_sim_time = ParameterValue(LaunchConfiguration('use_sim_time'), value_type=bool)
    nodes = [
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': description, 'use_sim_time': use_sim_time}], output='screen'),
        Node(package='rviz2', executable='rviz2', condition=IfCondition(LaunchConfiguration('rviz')),
             arguments=['-d', str(share / 'rviz/ros2.rviz')], parameters=[{'use_sim_time': use_sim_time}]),
    ]
    if LaunchConfiguration('publish_joint_states').perform(context).lower() == 'true':
        nodes.extend([
            Node(package='joint_state_publisher_gui', executable='joint_state_publisher_gui',
                 condition=IfCondition(LaunchConfiguration('gui')), parameters=[{'use_sim_time': use_sim_time}]),
            Node(package='joint_state_publisher', executable='joint_state_publisher',
                 condition=UnlessCondition(LaunchConfiguration('gui')), parameters=[{'use_sim_time': use_sim_time}]),
        ])
    return nodes


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('variant', default_value='base', choices=['base', 'cargo', 'arm', 'display']),
        DeclareLaunchArgument('model', default_value='', description='Optional custom URDF path'),
        DeclareLaunchArgument('gui', default_value='true', choices=['true', 'false']),
        DeclareLaunchArgument('publish_joint_states', default_value='true', choices=['true', 'false']),
        DeclareLaunchArgument('rviz', default_value='true', choices=['true', 'false']),
        DeclareLaunchArgument('use_sim_time', default_value='false', choices=['true', 'false']),
        OpaqueFunction(function=setup),
    ])
