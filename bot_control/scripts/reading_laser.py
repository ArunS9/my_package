import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class LaserSubscriber(Node):
    def __init__(self):
        super().__init__('laser_subscriber')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.laser_callback,
            10
        )
        self.publisher = self.create_publisher(LaserScan, '/filtered_scan', 10)
        self.subscription

    def laser_callback(self, msg):
        # Modify the laser scan data to filter the range to 0-120 degrees
        filtered_ranges = msg.ranges[0:240]  # Get ranges corresponding to 0-120 degrees
        msg.ranges = filtered_ranges

        # Publish the filtered laser scan data
        self.publisher.publish(msg)
        self.get_logger().info('Published filtered laser scan data.')

def main(args=None):
    rclpy.init(args=args)
    laser_subscriber = LaserSubscriber()
    rclpy.spin(laser_subscriber)
    laser_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

