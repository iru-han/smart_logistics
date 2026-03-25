# smart_logistics/ui/components/dialogs.py
from PySide6 import QtWidgets, QtCore
from ...core.validator import DataValidator

class BaseInputDialog(QtWidgets.QDialog):
    def __init__(self, title, schema, parent=None):
        super().__init__(parent)
        self.schema = schema  # 검증 및 UI 설계도 주입받음
        self.setWindowTitle(title)
        self.setFixedSize(350, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QFormLayout(self)
        self.edits = {} # 입력창들을 담을 저장소
        
        # 설계도(schema)에 따라 입력창 자동 생성
        for key, (label, _) in self.schema.items():
            edit = QtWidgets.QLineEdit()
            layout.addRow(f"{label}:", edit)
            self.edits[key] = edit

        self.btn_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        self.btn_box.accepted.connect(self.handle_ok)
        self.btn_box.rejected.connect(self.reject)
        layout.addWidget(self.btn_box)

    def get_data(self):
        """[핵심] 이제 딕셔너리에서 데이터를 동적으로 가져옵니다."""
        return {key: edit.text().strip() for key, edit in self.edits.items()}

    def handle_ok(self):
        """검증에 통과해야만 창이 닫히도록 제어"""
        data = self.get_data()
        is_valid, message = DataValidator.validate(data, self.schema)
        
        if not is_valid:
            QtWidgets.QMessageBox.warning(self, "입력 오류", message)
            return  # 창이 안 닫힘

        super().accept() # 검증 통과 시에만 닫힘