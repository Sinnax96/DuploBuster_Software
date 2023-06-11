import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class DuploVision(Node):

    def __init__(self):
        super().__init__('duplo_vision')
        self.publisher_ = self.create_publisher(String, 'duplo_position', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Duplo at : %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)

    duplo_vision = DuploVision()

    rclpy.spin(minimal_publisher)

    duplo_vision.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
