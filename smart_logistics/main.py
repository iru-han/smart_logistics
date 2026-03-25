import sys
import rclpy
import threading
from PySide6.QtWidgets import QApplication
from .database.inventory_db import InventoryDB
from .navigation.logistics_nav import LogisticsNavigator
from .ui.dashboard import SmartLogisticsUI

def main():
    # 1. ROS 2 초기화
    rclpy.init()
    
    # 2. 핵심 모듈(UML 객체) 생성
    db = InventoryDB()
    robot = LogisticsNavigator()
    
    # 3. ROS 2 스핀을 백그라운드 쓰레드에서 실행
    ros_thread = threading.Thread(target=rclpy.spin, args=(robot,), daemon=True)
    ros_thread.start()
    
    # 4. Qt6 애플리케이션 실행
    app = QApplication(sys.argv)
    
    # 스타일 테마 적용 (선택 사항: Qt6는 기본 테마가 훨씬 깔끔합니다)
    app.setStyle('Fusion')
    
    view = SmartLogisticsUI(db, robot)
    view.show()
    
    # 5. 앱 종료 시 ROS 2도 함께 종료
    exit_code = app.exec()
    rclpy.shutdown()
    sys.exit(exit_code)

if __name__ == '__main__':
    main()