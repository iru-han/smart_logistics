import os
from PySide6 import QtWidgets, QtCore, QtUiTools

class SmartLogisticsUI(QtWidgets.QMainWindow):
    def __init__(self, db, robot):
        """
        UML 원칙: 의존성 주입 (Dependency Injection)
        db: InventoryDB 인스턴스
        robot: LogisticsNavigator 인스턴스
        """
        super().__init__()
        self.db = db
        self.robot = robot
        
        # UI 파일 로드 및 초기 설정
        self.setup_ui()
        
        # 위젯 연결 확인 및 시그널/슬롯 연결
        self.connect_signals()

    def setup_ui(self):
        """Qt Designer(.ui) 파일을 로드하여 GUI를 구성합니다."""
        loader = QtUiTools.QUiLoader()
        
        # 1. 파일 경로 설정 (dashboard.py와 같은 폴더의 main_window.ui)
        ui_file_path = os.path.join(os.path.dirname(__file__), 'main_window.ui')
        
        # 2. 파일 존재 여부 및 용량 체크 (0바이트 에러 방지)
        if not os.path.exists(ui_file_path):
            QtWidgets.QMessageBox.critical(self, "파일 오류", f"UI 파일을 찾을 수 없습니다:\n{ui_file_path}")
            return
        
        ui_file = QtCore.QFile(ui_file_path)
        if not ui_file.open(QtCore.QFile.ReadOnly):
            QtWidgets.QMessageBox.critical(self, "오류", f"UI 파일을 열 수 없습니다")
            return

        try:
            # 핵심 변경: self를 인자로 주지 않고 UI 객체만 생성합니다.
            self.ui = loader.load(ui_file)
            ui_file.close()

            if not self.ui:
                return

            # UI 파일 내부의 핵심 구성 요소들을 현재 윈도우(self)에 설정합니다.
            self.setCentralWidget(self.ui.centralwidget)  # UI의 메인 위젯 추출 
            self.setMenuBar(self.ui.menubar)              # 메뉴바 추출 [cite: 4]
            self.setStatusBar(self.ui.statusbar)          # 상태바 추출 [cite: 4]
            self.setWindowTitle("Turtleship Smart Logistics Center")
            
            # 메인 윈도우 크기를 UI 파일에 정의된 크기로 맞춤 
            self.resize(self.ui.size())
            
        except Exception as e:
            print(f"UI 로드 중 에러 발생: {e}")

    def connect_signals(self):
        """UI 객체 내부의 위젯 이름을 기반으로 연결합니다."""
        # loader.load()로 불러온 위젯들은 self.ui를 통해 접근해야 합니다.
        if hasattr(self.ui, 'btn_mission'):
            self.ui.btn_mission.clicked.connect(self.handle_mission)
        else:
            print("경고: UI 파일에 'btn_mission' 버튼이 정의되지 않았습니다.")

    @QtCore.Slot()
    def handle_mission(self):
        """버튼 클릭 시 실행되는 핵심 비즈니스 로직"""
        # 1. 입력창에서 데이터 가져오기 (objectName: edit_name, edit_qty)
        try:
            name = self.ui.edit_name.text().strip()
            change_val = self.ui.edit_qty.text().strip()
            
            if not name:
                QtWidgets.QMessageBox.warning(self, "입력 오류", "품목 이름을 입력하세요.")
                return

            # 2. DB 조회 (InventoryDB 객체 활용)
            result = self.db.get_item_by_name(name)
            if not result:
                QtWidgets.QMessageBox.critical(self, "조회 실패", f"'{name}' 품목이 DB에 없습니다.")
                return

            barcode, x, y, current_qty = result

            # 3. 로봇 동작 수행 (LogisticsNavigator 객체 활용)
            # GUI가 멈추지 않게 하려면 긴 동작은 쓰레드 처리가 필요하지만, 
            # 일단 기존 rotate_360 로직을 호출합니다.
            self.robot.rotate_360()

            # 4. 수량 업데이트 처리
            if change_val:
                try:
                    change = int(change_val)
                    new_qty = max(0, current_qty + change)
                    self.db.update_quantity(barcode, new_qty)
                    
                    status_msg = f"재고 업데이트 성공: {current_qty} -> {new_qty}\n로봇이 지점({x}, {y})을 확인했습니다."
                    QtWidgets.QMessageBox.information(self, "미션 완료", status_msg)
                    
                    # 입력창 초기화
                    self.ui.edit_qty.clear()
                except ValueError:
                    QtWidgets.QMessageBox.warning(self, "입력 오류", "수량에는 숫자만 입력 가능합니다.")
            else:
                QtWidgets.QMessageBox.information(self, "조회 완료", f"현재 '{name}'의 재고는 {current_qty}개 입니다.")

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "실행 오류", f"로직 처리 중 오류 발생: {str(e)}")