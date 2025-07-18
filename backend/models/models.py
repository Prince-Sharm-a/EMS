from sqlalchemy import Column, Date, Integer, Float, String, func, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship


from db.database import settings, get_db, get_raw_db,SessionLocal,Base

class Employee(Base):
    __tablename__="employee"
    
    e_id=Column(Integer,primary_key=True)
    e_full_name=Column(String(50),nullable=False)
    e_address=Column(Text)
    e_email=Column(String(50),nullable=False)
    e_phone_code=Column(String(3),nullable=False,default="+91")
    e_phone_no=Column(String(10),nullable=False)
    e_department=Column(Integer,ForeignKey("department.d_id"))
    e_joining_date=Column(Date,nullable=False,server_default=func.now())
    
    emp_department=relationship("Department",back_populates="")
    e_payroll=relationship("Payroll",back_populates="employee_pr")
    e_project_assigned=relationship("Project_Assigned",back_populates="pra_employee")
    e_attendance=relationship("Attendance",back_populates="att_employees")
    
class Department(Base):
    __tablename__="department"
    
    d_id=Column(Integer,primary_key=True)
    d_name=Column(String(50),nullable=False)
    d_description=Column(String(100))
    d_location=Column(Integer,ForeignKey("department_location.d_location_id"))
    
    d_employees=relationship("Employee",back_populates="emp_department")
    dept_loc=relationship("Department_Location",back_populates="loc_department")
    
class Department_Location(Base):
    __tablename__='department_location'
    
    d_location_id=Column(Integer,primary_key=True)
    d_block_name=Column(String(50),nullable=False)
    
    loc_department=relationship("Department",back_populates="dept_loc")
    
class Payroll(Base):
    __tablename__="payroll"
    
    pr_id=Column(Integer,primary_key=True)
    e_id=Column(Integer,ForeignKey("employee.e_id"))
    Salary_Before_Deduction=Column(Float)
    Salary_After_Deduction=Column(Float,default=Salary_Before_Deduction-((Salary_Before_Deduction/100)*6))
    per_hour_salary=Column(Float,default=((Salary_After_Deduction/12)/30)/8)
    
    employee_pr=relationship("Employee",back_populates="e_payroll")
    
class Project(Base):
    __tablename__="projects"
    
    pj_id=Column(Integer,primary_key=True)
    pj_name=Column(String(30),nullable=False)
    pj_description=Column(Text)
    
    pj_project_As=relationship("Project_Assigned",back_populates="pra_project")
    
class Project_Assigned(Base):
    __tablename__="project_Assigned"
    
    temp_id=Column(Integer,primary_key=True)
    pj_id=Column(Integer,ForeignKey("projects.pj_id"))
    e_id=Column(Integer,ForeignKey("employee.e_id"))
    
    pra_employee=relationship("Employee",back_populates="e_project_assigned")
    pra_project=relationship("Project",back_populates="pj_project_As")
    
class Attendance(Base):
    __tablename__="attendance"
    
    id=Column(Integer,primary_key=True)
    e_id=Column(Integer,ForeignKey("employee.e_id"))
    check_in=Column(DateTime,nullable=True)
    check_out=Column(DateTime,nullable=True)
    working_hours=Column(Integer,nullable=False,default=0)
    per_day_pay=Column(Integer)
    
    att_employees=relationship("Employee",back_populates="e_attendance")