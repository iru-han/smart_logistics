import sqlite3

class InventoryDB:
    def __init__(self, db_name='turtleship_inventory.db'):
        self.db_path = db_name
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                barcode TEXT UNIQUE,
                item_name TEXT NOT NULL,
                pos_x REAL,
                pos_y REAL,
                quantity INTEGER DEFAULT 0
            )
        ''')
        samples = [
            ('A001', 'Motor', 1.2, 3.5, 10),
            ('B002', 'Sensor', -2.0, 4.1, 5),
            ('C003', 'Battery', 0.5, -1.2, 2)
        ]
        cursor.executemany(
            "INSERT OR IGNORE INTO inventory (barcode, item_name, pos_x, pos_y, quantity) VALUES (?,?,?,?,?)", 
            samples
        )
        conn.commit()
        conn.close()

    def get_all_items(self):
        """전체 목록 조회 (Read)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, barcode, item_name, pos_x, pos_y, quantity FROM inventory")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_item_by_name(self, name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, barcode, item_name, pos_x, pos_y, quantity FROM inventory WHERE item_name = ?", (name,))
        result = cursor.fetchone()
        conn.close()
        return result

    def update_quantity(self, barcode, new_qty):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE inventory SET quantity = ? WHERE barcode = ?", (new_qty, barcode))
        conn.commit()
        conn.close()
    
    def add_item(self, barcode, name, x, y, qty):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            # barcode 컬럼에 UNIQUE 제약 조건이 있어야 합니다.
            cursor.execute(
                "INSERT INTO inventory (barcode, item_name, pos_x, pos_y, quantity) VALUES (?, ?, ?, ?, ?)",
                (barcode, name, x, y, qty)
            )
            conn.commit()
            return True # 저장 성공
        except sqlite3.IntegrityError:
            return False # 바코드 중복 발생
        finally:
            conn.close()

    def delete_item(self, db_id):
        """id 기반 삭제 (Delete)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE id = ?", (db_id,))
        conn.commit()
        conn.close()