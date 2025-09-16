from database import engine, Base
from models import Student, Session, StudentSession, MachineRecord, StudentRecord

def create_tables():
    """創建所有數據庫表"""
    try:
        # 創建所有表
        # 問題：每次都會重新創建表，會丟失數據
        Base.metadata.create_all(bind=engine)
        print("✅ 所有數據庫表創建成功！")
        
        # 列出創建的表
        print("📋 已創建的表：")
        for table_name in Base.metadata.tables.keys():
            print(f"  - {table_name}")
            
    except Exception as e:
        print(f"❌ 創建表失敗: {e}")

if __name__ == "__main__":
    create_tables()