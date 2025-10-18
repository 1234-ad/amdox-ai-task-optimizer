"""
Database Models
SQLAlchemy models for the application
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .connection import Base

class Employee(Base):
    """Employee model"""
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    department = Column(String(50))
    position = Column(String(100))
    skills = Column(JSON)  # List of skills
    experience_years = Column(Float, default=0)
    performance_rating = Column(Float, default=0.7)
    available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    emotion_analyses = relationship("EmotionAnalysis", back_populates="employee")
    alerts = relationship("Alert", back_populates="employee")
    tasks = relationship("Task", back_populates="assigned_employee")

class Task(Base):
    """Task model"""
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(50))  # creative, analytical, routine, etc.
    priority = Column(String(20))  # low, medium, high
    complexity = Column(String(20))  # low, medium, high, expert
    required_skills = Column(JSON)  # List of required skills
    estimated_hours = Column(Float, default=2.0)
    status = Column(String(20), default='pending')  # pending, in_progress, completed
    assigned_to = Column(Integer, ForeignKey('employees.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    assigned_employee = relationship("Employee", back_populates="tasks")

class EmotionAnalysis(Base):
    """Emotion analysis record"""
    __tablename__ = 'emotion_analyses'
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    dominant_emotion = Column(String(50))
    emotion_scores = Column(JSON)  # Dict of emotion scores
    stress_score = Column(Float)
    burnout_risk_level = Column(String(20))
    confidence = Column(Float)
    modalities_used = Column(JSON)  # List of modalities (text, facial, speech)
    raw_data = Column(JSON)  # Full emotion fusion result
    
    # Relationships
    employee = relationship("Employee", back_populates="emotion_analyses")

class Alert(Base):
    """HR alert record"""
    __tablename__ = 'alerts'
    
    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String(100), unique=True, index=True, nullable=False)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    severity = Column(String(20), nullable=False)  # critical, high, medium, low
    title = Column(String(200), nullable=False)
    description = Column(Text)
    recommendation = Column(Text)
    status = Column(String(20), default='open')  # open, acknowledged, resolved
    priority = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    acknowledged_by = Column(String(100))
    acknowledged_at = Column(DateTime)
    resolved_by = Column(String(100))
    resolved_at = Column(DateTime)
    resolution_notes = Column(Text)
    related_emotion_data = Column(JSON)
    
    # Relationships
    employee = relationship("Employee", back_populates="alerts")
