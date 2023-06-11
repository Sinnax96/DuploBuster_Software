import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class NodeAI(Node):
    def __init__(self):
        super().__init__('node_ai')
        self.publisher_ = self.create_publisher(String, 'duplo_position', 10)
        timer_period = 1  # seconds
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
    node_ai = NodeAI()
    print("Let's spin the sentient AI")
    rclpy.spin(node_ai)

    node_ai.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
