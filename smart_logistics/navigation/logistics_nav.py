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

    def go_to_pose(self, x, y):
        """DB에서 받은 좌표로 로봇을 이동시킵니다."""
        self.get_logger().info(f"목표 지점으로 이동 시작: x={x}, y={y}")
        
        # 실제 Nav2 액션 클라이언트 호출 로직이 들어가야 함
        # 지금은 테스트를 위해 로그만 남기고 이동하는 척하는 로직으로 대체 확인
        # 성공 시 True 반환
        return True