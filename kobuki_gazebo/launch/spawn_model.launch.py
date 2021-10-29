import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
  
  use_sim_time = LaunchConfiguration('use_sim_time', default='True')
  
  urdf_file = get_package_share_directory('kobuki_description')+'/urdf/kobuki.urdf'

  with open(urdf_file, 'r') as infp:
    robot_desc = infp.read()

  sim_time_argument = DeclareLaunchArgument(
    'use_sim_time',
    default_value='True',
    description='Use simulation (Gazebo) clock if true',
  )

  kobuki_model = Node(
    package='robot_state_publisher',
    executable='robot_state_publisher',
    name='robot_state_publisher',
    output='screen',
    parameters=[
      {'use_sim_time'      : use_sim_time,
       'robot_description' : robot_desc}],
    arguments=[urdf_file]
  )

  spawn_entity = ExecuteProcess(
    cmd=['ros2', 'run', 'gazebo_ros', 'spawn_entity.py', '-topic', '/robot_description', '-entity', 'kobuki'], output='screen')

  ld = LaunchDescription()
  ld.add_action(sim_time_argument)
  ld.add_action(kobuki_model)
  ld.add_action(spawn_entity)

  return ld
