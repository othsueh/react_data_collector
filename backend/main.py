from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, test_connection
from models import Student, Session, StudentSession, MachineRecord, StudentRecord
from pydantic import BaseModel
from typing import List, Optional
import json

app = FastAPI(title="React Data Collector API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 依賴注入：獲取數據庫會話
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic 模型
class StudentCreate(BaseModel):
    name: str
    class_type: str  # 'morning' or 'afternoon'

class SessionCreate(BaseModel):
    name: str
    n_cycles: int
    class_type: str  # 'morning' or 'afternoon'

class SessionUpdate(BaseModel):
    name: Optional[str] = None
    n_cycles: Optional[int] = None
    class_type: Optional[str] = None

class StudentSessionCreate(BaseModel):
    session_id: int
    student_id: int

class MachineRecordCreate(BaseModel):
    session_id: int
    student_session_id: str
    student_id: int
    hit_miss_array: List[int]  # [1,0,1,0,...]

class StudentRecordCreate(BaseModel):
    session_id: int
    student_session_id: str
    student_id: int
    hit_miss_array: List[int]  # [1,0,1,0,...]
    goals_scored: Optional[int] = None

# API 路由
@app.get("/")
async def root():
    return {"message": "React Data Collector API"}

@app.get("/health")
async def health_check():
    """健康檢查"""
    if test_connection():
        return {"status": "healthy", "database": "connected"}
    else:
        raise HTTPException(status_code=500, detail="Database connection failed")

@app.post("/students/")
async def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """創建學生"""
    db_student = Student(name=student.name, class_type=student.class_type)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/")
async def get_students(class_type: Optional[str] = None, db: Session = Depends(get_db)):
    """獲取學生列表"""
    query = db.query(Student)
    if class_type:
        query = query.filter(Student.class_type == class_type)
    return query.all()

@app.get("/students/{student_id}")
async def get_student_by_id(student_id: int, db: Session = Depends(get_db)):
    """根據學生ID獲取學生資訊"""
    student = db.query(Student).get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.post("/sessions/")
async def create_session(session: SessionCreate, db: Session = Depends(get_db)):
    db_session = Session(
        name=session.name,
        n_cycles=session.n_cycles,
        class_type=session.class_type,
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

# 取得此 session 的學生名單（即時查詢，不做快照）
@app.get("/sessions/{session_id}/students")
async def get_session_students(session_id: int, db: Session = Depends(get_db)):
    sess = db.query(Session).get(session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")
    return db.query(Student).filter(Student.class_type == sess.class_type).all()

@app.get("/sessions/")
async def get_sessions(db: Session = Depends(get_db)):
    """獲取所有會話"""
    return db.query(Session).all()

@app.get("/sessions/current")
async def get_current_session(db: Session = Depends(get_db)):
    """獲取目前活躍的 session (若多個，取最新建立者) """
    current = (
        db.query(Session)
        .filter(Session.is_active == True)
        .order_by(Session.created_at.desc())
        .first()
    )
    if not current:
        raise HTTPException(status_code=404, detail="No active session")
    return current

@app.put("/sessions/current")
async def update_current_session(update: SessionUpdate, db: Session = Depends(get_db)):
    """更新目前活躍的 session"""
    current = (
        db.query(Session)
        .filter(Session.is_active == True)
        .order_by(Session.created_at.desc())
        .first()
    )
    if not current:
        raise HTTPException(status_code=404, detail="No active session")
    if update.name is not None:
        current.name = update.name
    if update.n_cycles is not None:
        current.n_cycles = update.n_cycles
    if update.class_type is not None:
        current.class_type = update.class_type
    db.commit()
    db.refresh(current)
    return current

@app.put("/sessions/current/deactivate")
async def deactivate_current_session(db: Session = Depends(get_db)):
    """將目前活躍的 session 設為不啟用"""
    current = (
        db.query(Session)
        .filter(Session.is_active == True)
        .order_by(Session.created_at.desc())
        .first()
    )
    if not current:
        raise HTTPException(status_code=404, detail="No active session to deactivate")
    current.is_active = False
    db.commit()
    db.refresh(current)
    return {"status": "deactivated", "session_id": current.id}

@app.post("/student-sessions/")
async def create_student_session(student_session: StudentSessionCreate, db: Session = Depends(get_db)):
    """創建學生會話"""
    db_student_session = StudentSession(
        session_id=student_session.session_id,
        student_id=student_session.student_id
    )
    db.add(db_student_session)
    db.commit()
    db.refresh(db_student_session)
    return db_student_session

@app.get("/student-sessions/current")
async def get_current_student_session(db: Session = Depends(get_db)):
    """獲取當前活躍的學生會話"""
    current_session = db.query(StudentSession).filter(StudentSession.is_active == True).first()
    if current_session:
        return {
            "student_session_uuid": current_session.student_session_uuid,
            "student_id": current_session.student_id,
            "session_id": current_session.session_id
        }
    return None

@app.put("/student-sessions/current/deactivate")
async def deactivate_current_student_session(db: Session = Depends(get_db)):
    """將目前活躍的學生會話設為不啟用"""
    current_student_session = (
        db.query(StudentSession)
        .filter(StudentSession.is_active == True)
        .order_by(StudentSession.created_at.desc())
        .first()
    )
    if not current_student_session:
        raise HTTPException(status_code=404, detail="No active student session to deactivate")
    current_student_session.is_active = False
    db.commit()
    db.refresh(current_student_session)
    return {
        "status": "deactivated",
        "student_session_uuid": current_student_session.student_session_uuid
    }

@app.get("/student-sessions/session/{session_id}")
async def get_student_sessions_by_session(session_id: int, db: Session = Depends(get_db)):
    """Get all student sessions for a given session"""
    return db.query(StudentSession).filter(StudentSession.session_id == session_id).all()

@app.post("/machine-records/")
async def create_machine_record(record: MachineRecordCreate, db: Session = Depends(get_db)):
    """創建機器記錄"""
    db_record = MachineRecord(
        session_id=record.session_id,
        student_session_id=record.student_session_id,
        student_id=record.student_id,
        hit_miss_array=json.dumps(record.hit_miss_array)
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@app.get("/machine-records/")
async def get_all_machine_records(db: Session = Depends(get_db)):
    """獲取所有學生記錄"""
    records = db.query(MachineRecord).all()
    return records

@app.get("/machine-records/session/{session_id}")
async def get_machine_records_by_session(session_id: int, db: Session = Depends(get_db)):
    """Get all machine records for a given session"""
    return db.query(MachineRecord).filter(MachineRecord.session_id == session_id).all()

@app.post("/student-records/")
async def create_student_record(record: StudentRecordCreate, db: Session = Depends(get_db)):
    """創建學生記錄"""
    db_record = StudentRecord(
        session_id=record.session_id,
        student_session_id=record.student_session_id,
        student_id=record.student_id,
        hit_miss_array=json.dumps(record.hit_miss_array),
        goals_scored=record.goals_scored
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@app.get("/student-records/")
async def get_all_student_records(db: Session = Depends(get_db)):
    """獲取所有學生記錄"""
    records = db.query(StudentRecord).all()
    return records

@app.get("/student-records/session/{session_id}")
async def get_student_records_by_session(session_id: int, db: Session = Depends(get_db)):
    """Get all student records for a given session"""
    return db.query(StudentRecord).filter(StudentRecord.session_id == session_id).all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)