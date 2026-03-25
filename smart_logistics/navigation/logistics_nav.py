import time
from rclpy.node import Node
from geometry_msgs.msg import Twist

class LogisticsNavigator(Node):
    def __init__(self):
        super().__init__('logistics_navigator')
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)

    def rotate_360(self):
        """제자리에서 한 바퀴 회전"""
        twist = Twist()
        twist.angular.z = 1.0
        duration = 6.3 
        
        self.get_logger().info("터틀봇 회전 시작...")
        start_time = time.time()
        while (time.time() - start_time) < duration:
            self.cmd_vel_pub.publish(twist)
            time.sleep(0.1)
            
        twist.angular.z = 0.0
        self.cmd_vel_pub.publish(twist)
        self.get_logger().info("회전 완료.")