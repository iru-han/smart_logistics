import time
from rclpy.node import Node
from rclpy.action import ActionClient
from geometry_msgs.msg import Twist, PoseStamped
from nav2_msgs.action import NavigateToPose
from rclpy.duration import Duration

class LogisticsNavigator(Node):
    def __init__(self):
        super().__init__('logistics_navigator')
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        
        # Nav2 NavigateToPose 액션 클라이언트 생성
        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

    def go_to_pose(self, x, y):
        """지도 상의 (x, y) 좌표로 Nav2를 이용해 주행합니다."""
        self.get_logger().info(f"목표 지점 전송 중... (x: {x}, y: {y})")

        # 1. 액션 서버 연결 확인
        if not self._action_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error('Nav2 액션 서버를 찾을 수 없습니다. Navigation2가 실행 중인지 확인하세요.')
            return False

        # 2. 목표 위치(Goal) 메시지 생성
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'  # 로드한 지도 기준 좌표계
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        
        # 좌표 설정
        goal_msg.pose.pose.position.x = float(x)
        goal_msg.pose.pose.position.y = float(y)
        goal_msg.pose.pose.orientation.w = 1.0  # 정면 방향

        # 3. 비동기로 목표 전송
        self.get_logger().info(f'좌표 ({x}, {y})로 이동 명령을 보냅니다.')
        send_goal_future = self._action_client.send_goal_async(goal_msg)
        
        # (참고) 결과 대기 로직을 추가할 수도 있지만, 
        # GUI 스레드 분리 상태이므로 여기서는 명령 전달까지만 보장합니다.
        return True

    def rotate_360(self):
        # 기존 회전 로직 유지
        pass