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
                barcode TEXT PRIMARY KEY,
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
        cursor.executemany("INSERT OR IGNORE INTO inventory VALUES (?,?,?,?,?)", samples)
        conn.commit()
        conn.close()

    def get_item_by_name(self, name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT barcode, pos_x, pos_y, quantity FROM inventory WHERE item_name = ?", (name,))
        result = cursor.fetchone()
        conn.close()
        return result

    def update_quantity(self, barcode, new_qty):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE inventory SET quantity = ? WHERE barcode = ?", (new_qty, barcode))
        conn.commit()
        conn.close()

    def get_all_items(self):
        """나중에 표(TableWidget)를 채울 때 사용할 전체 목록 조회 함수"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory")
        rows = cursor.fetchall()
        conn.close()
        return rows