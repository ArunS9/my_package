import rclpy
from geometry_msgs.msg import Twist
import sys, select, termios, tty
import threading

moveBindings = {
    'i': (1.0, 0.0, 0.0, 0.0),    # Forward
    'o': (1.0, 0.0, 0.0, -1.0),   # Forward and right
    'j': (0.0, 0.0, 0.0, 1.0),    # Left
    'l': (0.0, 0.0, 0.0, -1.0),   # Right
    'u': (1.0, 0.0, 0.0, 1.0),    # Forward and left
    ',': (-1.0, 0.0, 0.0, 0.0),   # Backward
    '.': (-1.0, 0.0, 0.0, 1.0),   # Backward and right
    'm': (-1.0, 0.0, 0.0, -1.0),  # Backward and left
    'O': (1.0, -1.0, 0.0, 0.0),   # Rotate clockwise
    'I': (1.0, 0.0, 0.0, 0.0),    # Forward
    'J': (0.0, 1.0, 0.0, 0.0),    # Left
    'L': (0.0, -1.0, 0.0, 0.0),   # Right
    'U': (1.0, 1.0, 0.0, 0.0),    # Forward and left
    '<': (-1.0, 0.0, 0.0, 0.0),   # Backward
    '>': (-1.0, -1.0, 0.0, 0.0),  # Backward and right
    'M': (-1.0, 1.0, 0.0, 0.0),   # Backward and left
    't': (0.0, 0.0, 1.0, 0.0),    # Up
    'b': (0.0, 0.0, -1.0, 0.0),   # Down
}

speedBindings = {
    'q': (1.1, 1.1),
    'z': (.9, .9),
    'w': (1.1, 1),
    'x': (.9, 1),
    'e': (1, 1.1),
    'c': (1, .9),
}

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

class TeleopThread(threading.Thread):
    def __init__(self, pub):
        super().__init__()
        self.pub = pub
        self.velocity_command = Twist()
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            key = getKey()
            if key in moveBindings.keys():
                self.velocity_command.linear.x = moveBindings[key][0]
                self.velocity_command.linear.y = moveBindings[key][1]
                self.velocity_command.linear.z = moveBindings[key][2]
                self.velocity_command.angular.z = moveBindings[key][3]
            elif key in speedBindings.keys():
                self.velocity_command.linear.x *= speedBindings[key][0]
                self.velocity_command.angular.z *= speedBindings[key][1]
            else:
                self.velocity_command.linear.x = 0.0
                self.velocity_command.linear.y = 0.0
                self.velocity_command.linear.z = 0.0
                self.velocity_command.angular.z = 0.0
            self.pub.publish(self.velocity_command)

    def stop(self):
        self.running = False

def teleop():
    rclpy.init()
    node = rclpy.create_node('teleop_keyboard')
    pub = node.create_publisher(Twist, 'cmd_vel', 10)

    teleop_thread = TeleopThread(pub)
    teleop_thread.start()

    try:
        rclpy.spin(node)
    finally:
        teleop_thread.stop()
        teleop_thread.join()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)
    try:
        teleop()
    except Exception as e:
        print(e)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

