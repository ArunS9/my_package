bot_control Package

This package provides functionality for controlling a robot and visualizing its sensor data in ROS 2.
Installation

    Clone this repository into your ROS 2 workspace:

    bash

cd ~/arun_ws/src
git clone <repository_url>

Build your ROS 2 workspace:

bash

    cd ~/arun_ws
    colcon build

Dependencies

This package depends on the following ROS 2 packages:

    rospy
    std_msgs
    geometry_msgs
    sensor_msgs

Make sure these dependencies are installed in your ROS 2 environment.
Usage
Launching the Node

To launch the node that reads laser scan data and publishes filtered data, use the provided launch file:

bash

ros2 launch bot_control reading_laser.launch.py

Visualizing Filtered Scan Data

The launch file also starts RViz for visualizing the filtered scan data. Make sure you have a proper RViz configuration file to visualize laser scan data.
Testing

To test the package, you can manually subscribe to the /filtered_scan topic and verify that the filtered laser scan data is being published correctly. You can also check RViz to see if the filtered scan data is being visualized as expected.
Contributing

Contributions to this package are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.
License

This package is licensed under the MIT License.
