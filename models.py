from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Связь многие-ко-многим между сотрудниками и навыками
employee_skills = db.Table(
    'employee_skills',
    db.Column('employee_id', db.Integer,
              db.ForeignKey('employee.employee_id')),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id')))


class DepartmentModel(db.Model):
    __tablename__ = "department"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    budget = db.Column(db.Float)
    employees = db.relationship('EmployeeModel',
                                backref='department',
                                lazy=True)

    def __repr__(self):
        return f"{self.name}"


class ProjectModel(db.Model):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    budget = db.Column(db.Float)
    employees = db.relationship('EmployeeModel', backref='project', lazy=True)

    def __repr__(self):
        return f"{self.name}"


class SkillModel(db.Model):
    __tablename__ = "skill"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)

    def __repr__(self):
        return f"{self.name}"


class EmployeeModel(db.Model):
    __tablename__ = "employee"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(255))
    age = db.Column(db.Integer())
    position = db.Column(db.String(80))
    salary = db.Column(db.Float)
    hire_date = db.Column(db.DateTime, default=datetime.utcnow)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    skills = db.relationship('SkillModel',
                             secondary=employee_skills,
                             backref='employees')

    def __init__(self,
                 employee_id,
                 name,
                 age,
                 position,
                 salary=None,
                 department_id=None,
                 project_id=None):
        self.employee_id = employee_id
        self.name = name
        self.age = age
        self.position = position
        self.salary = salary
        self.department_id = department_id
        self.project_id = project_id

    def __repr__(self):
        return f"{self.name}:{self.employee_id}"
