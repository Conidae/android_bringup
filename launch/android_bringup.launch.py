import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    urdf_path=os.path.join(get_package_share_directory("android_bringup"),"urdf","android_model.urdf")
    with open(urdf_path,"r") as infp:
        robot_description=infp.read()
    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description':robot_description}],
            arguments=['urdf']
        ),
        Node(
            package="laser_filters",
            executable="scan_to_scan_filter_chain",
            parameters=[
                PathJoinSubstitution([
                    get_package_share_directory("android_bringup"),
                    "config", "laser_filter.yaml",
                ])],
            remappings=[('/scan', 'ldlidar_node/scan')]
        ),
        Node(
            ## Configure the TF of the robot to the origin of the map coordinatesf
            package='tf2_ros',
            executable='static_transform_publisher',
            namespace='',
            output='screen',
            arguments=['0.40', '0.0', '-0.33', '-1.5708', '0.0', '0.0', 'android_camera', 'ldlidar_base']
        )
    ])