import os
from PySide6 import QtWidgets, QtCore, QtUiTools
from .components.dialogs import BaseInputDialog

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

        # 시작하자마자 재고 목록 불러오기
        self.refresh_table()

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
            """UI 객체 내부의 위젯 시그널 연결"""
            # 1. 페이지 전환 (Stacked Widget)
            if hasattr(self.ui, 'btn_go_admin'):
                self.ui.btn_go_admin.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
            if hasattr(self.ui, 'btn_go_main'):
                self.ui.btn_go_main.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))

            # 2. 메인 페이지: 미션 시작
            if hasattr(self.ui, 'btn_mission'):
                self.ui.btn_mission.clicked.connect(self.handle_mission)

            # 3. 어드민 페이지: 추가, 삭제, 새로고침
            if hasattr(self.ui, 'btn_add'):
                self.ui.btn_add.clicked.connect(self.handle_add)
            if hasattr(self.ui, 'btn_delete'):
                self.ui.btn_delete.clicked.connect(self.handle_delete)
    
    # --- 비즈니스 로직(Handle 계층) ---
    def handle_add(self):
        # 1. 재고 등록에 필요한 설계도 정의
        inventory_fields = {
            "barcode": ("바코드", str),
            "name": ("품목명", str),
            "x": ("X좌표", float),
            "y": ("Y좌표", float),
            "qty": ("수량", int)
        }
        
        # 2. 범용 다이얼로그 생성 시 설계도 주입
        dialog = BaseInputDialog("신규 재고 등록", inventory_fields, self)
        
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            data = dialog.get_data()
            
            # DB 로직 (바코드는 DB 고유값이므로 여기서 중복 체크)
            if self.db.add_item(data["barcode"], data["name"], 
                                float(data["x"]), float(data["y"]), int(data["qty"])):
                QtWidgets.QMessageBox.information(self, "성공", "등록되었습니다.")
                self.refresh_table()
            else:
                QtWidgets.QMessageBox.critical(self, "오류", "이미 존재하는 바코드입니다.")

    def refresh_table(self):
        """테이블 갱신 로직 (View 업데이트)"""
        items = self.db.get_all_items()
        for table_name in ['table_inventory', 'table_inventory_admin']:
            if hasattr(self.ui, table_name):
                self._fill_table(getattr(self.ui, table_name), items, is_admin=('admin' in table_name))

    def _fill_table(self, table, items, is_admin):
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["ID", "바코드", "이름", "X", "Y", "수량"])
        table.setRowCount(len(items))
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        for r_idx, row_data in enumerate(items):
            for c_idx, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                # UML 권한 제어: 관리자만 수정 가능
                item.setFlags(QtCore.Qt.ItemIsEnabled | (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable if is_admin else QtCore.Qt.NoItemFlags))
                table.setItem(r_idx, c_idx, item)

    @QtCore.Slot()
    def handle_mission(self):
        """버튼 클릭 시 실행되는 핵심 비즈니스 로직"""
        # 1. 입력창에서 데이터 가져오기 (objectName: edit_name, edit_qty)
        try:
            name = self.ui.edit_name.text().strip()
            
            if not name:
                QtWidgets.QMessageBox.warning(self, "입력 오류", "품목 이름을 입력하세요.")
                return

            # 2. DB 조회 (InventoryDB 객체 활용)
            result = self.db.get_item_by_name(name)
            if not result:
                QtWidgets.QMessageBox.critical(self, "조회 실패", f"'{name}' 품목이 DB에 없습니다.")
                return

            id, barcode, item_name, pos_x, pos_y, quantity = result

            # 2. 로봇 동작 수행 (회전이 아닌 목표 좌표로 이동)
            # GUI 동결 방지를 위해 로봇 이동을 담당하는 별도 메서드 호출
            self.move_robot_to_target(pos_x, pos_y)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "실행 오류", f"로직 처리 중 오류 발생: {str(e)}")
    
          
    def handle_delete(self):
        """어드민 페이지: 선택된 항목 삭제 (Delete)"""
        table = self.ui.table_inventory_admin
        current_row = table.currentRow()
        
        if current_row < 0:
            QtWidgets.QMessageBox.warning(self, "경고", "삭제할 항목을 선택하세요.")
            return

        # 테이블 0번 컬럼이 'ID'인 경우 (Primary Key)
        db_id = table.item(current_row, 0).text()
        item_name = table.item(current_row, 2).text() # 2번 컬럼이 '이름'일 경우
        
        confirm = QtWidgets.QMessageBox.question(
            self, "삭제 확인", f"ID {db_id} ({item_name}) 항목을 정말 삭제하시겠습니까?"
        )
        
        if confirm == QtWidgets.QMessageBox.Yes:
            self.db.delete_item(db_id) # ID 기반 삭제
            self.refresh_table()

    def move_robot_to_target(self, x, y):
        """로봇 이동 명령을 별도 스레드에서 실행 (GUI 멈춤 방지)"""
        # 간단한 구현을 위해 threading 사용
        import threading
        move_thread = threading.Thread(target=self.robot.go_to_pose, args=(x, y))
        move_thread.daemon = True
        move_thread.start()