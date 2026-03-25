import tkinter as tk
from tkinter import messagebox

class SmartLogisticsUI(tk.Tk):
    def __init__(self, db, robot):
        super().__init__()
        self.db = db
        self.robot = robot
        
        self.title("Smart Logistics Dashboard")
        self.geometry("300x200")
        
        # 간단한 UI 구성
        tk.Label(self, text="품목 이름:").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()
        
        tk.Button(self, text="재고 확인 및 이동", command=self.on_click).pack(pady=20)

    def on_click(self):
        name = self.name_entry.get().strip()
        item = self.db.get_item_by_name(name)
        
        if item:
            barcode, x, y, qty = item
            # 로봇 동작 실행
            self.robot.rotate_360()
            messagebox.showinfo("완료", f"{name} 위치({x}, {y})로 이동 완료!")
        else:
            messagebox.showerror("오류", "품목을 찾을 수 없습니다.")