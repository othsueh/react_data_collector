from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, DateTime, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from database import Base
import uuid

# 台灣時區
TAIWAN_TZ = timezone(timedelta(hours=8))

def taiwan_now():
    """獲取台灣當前時間"""
    return datetime.now(TAIWAN_TZ)

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    class_type = Column(String(20), nullable=False)  # 'morning' or 'afternoon'
    created_at = Column(DateTime, default=taiwan_now)
    
    # Relationships
    machine_records = relationship("MachineRecord", back_populates="student")
    student_records = relationship("StudentRecord", back_populates="student")


class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    n_cycles = Column(Integer, nullable=False)
    class_type = Column(String(20), nullable=False)  # 'morning' or 'afternoon'
    created_at = Column(DateTime, default=taiwan_now)
    is_active = Column(Boolean, default=True)
    
    machine_records = relationship("MachineRecord", back_populates="session")
    student_records = relationship("StudentRecord", back_populates="session")


class StudentSession(Base):
    __tablename__ = "student_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    student_session_uuid = Column(String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))
    is_active = Column(Boolean, default=True)  # 標記當前正在進行的學生測試
    created_at = Column(DateTime, default=taiwan_now)
    
    # Relationships
    session = relationship("Session")
    student = relationship("Student")
    machine_record = relationship("MachineRecord", back_populates="student_session", uselist=False)
    student_record = relationship("StudentRecord", back_populates="student_session", uselist=False)


class MachineRecord(Base):
    __tablename__ = "machine_records"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    student_session_id = Column(String(36), ForeignKey("student_sessions.student_session_uuid"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)  # 被測試的學生
    hit_miss_array = Column(Text, nullable=False)  # JSON array: [1,0,1,0,...] 長度為N
    recorded_at = Column(DateTime, default=taiwan_now)
    
    # Relationships
    session = relationship("Session", back_populates="machine_records")
    student = relationship("Student", back_populates="machine_records")
    student_session = relationship("StudentSession", back_populates="machine_record")


class StudentRecord(Base):
    __tablename__ = "student_records"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    student_session_id = Column(String(36), ForeignKey("student_sessions.student_session_uuid"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    hit_miss_array = Column(Text, nullable=False)  # JSON array: [1,0,1,0,...] 長度為N
    goals_scored = Column(Integer, nullable=True)  # 最後一次記錄的進球數
    recorded_at = Column(DateTime, default=taiwan_now)
    
    # Relationships
    session = relationship("Session", back_populates="student_records")
    student = relationship("Student", back_populates="student_records")
    student_session = relationship("StudentSession", back_populates="student_record")