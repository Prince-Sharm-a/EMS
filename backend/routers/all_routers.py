from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from datetime import datetime
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from pymysql.connections import Connection
from pymysql.cursors import DictCursor

from db.database import settings, get_db, get_raw_db,SessionLocal,Base
from models.models import Employee,Payroll,Attendance,Department,Department_Location,Project,Project_Assigned
from schema.schema import EmployeeResponse,AddingNewEmployee,AttendanceResponse,checkIn,checkOut,projectAssign,departmentResponse,AddingNewProject,updateResponse,addingBuildingLocation

emp=APIRouter(
    prefix="/EMS",
    tags=["EMS"]
)

@emp.get("/employee_list")
async def get_employee_details(
    e_id:Optional[int]=None,
    d_id:Optional[int]=None,
    db:Session=Depends(get_db),
    rdb:Session=Depends(get_raw_db)
):
    try:
        cursor=rdb.cursor(cursor=DictCursor)
        query=f'''
        select 
        emp.e_id ,
        emp.e_full_name,
        concat(emp.e_phone_code,' ',emp.e_phone_no) as e_phone_no,
        dprt.d_name ,
        dprt.block_name as d_block,
        emp.e_joining_date 
        from employee emp
        left join (select dpt.d_id, 
        dpt.d_name, 
        dptl.d_block_name as block_name 
        from department dpt 
        left join department_location dptl on dptl.d_location_id=dpt.d_location) as dprt on dprt.d_id=emp.e_department
        '''
        if e_id:
            condition=f'''where emp.e_id={e_id}'''
            query=query+' '+condition
        
        if d_id:
            condition=f'dprt.d_id={d_id}'
            if e_id:
                condition='and'+' '+condition
            else :
                condition='where'+' '+condition
            
            query=query+' '+condition
        
        cursor.execute(query)
        result= cursor.fetchall()
        
        return list(row for row in result)
    except Exception as e:
        if e_id or d_id:
            raise HTTPException(status_code=404,detail=f"user not found \n{e}")
        else :
            raise HTTPException(status_code=500,detail=f"{e}")

@emp.post("/adding_new_employee")
async def adding_new_employee(response:AddingNewEmployee,db:Session=Depends(get_db)):
    try :
        if len(response.e_mobile_no)!=10:
            raise HTTPException(status_code=500,detail="Enter valid mobile number")
        new_employee=Employee(
            e_full_name=response.e_name.title(),
            e_address=response.e_address,
            e_email=response.e_email,
            e_phone_code=response.e_mobile_code,
            e_phone_no=response.e_mobile_no,
            e_department=response.e_department,
        )
        
        db.add(new_employee)
        db.flush()
        
        new_employee_salary=Payroll(
            e_id=new_employee.e_id,
            Salary_Before_Deduction=response.e_salary,
        )
        db.add(new_employee_salary)
        db.commit()
        return {"Message":"Successfully added new employee","New Employee":{"e_name":new_employee.e_full_name,"e_address":new_employee.e_address,"e_email":new_employee.e_email,"e_phone_code":new_employee.e_phone_code,"e_phone_noe":new_employee.e_phone_no,"e_department":new_employee.e_department}}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")
    
    
@emp.post("/assigning_project",response_model=projectAssign)
async def assign_project(response:projectAssign,db:Session=Depends(get_db),rdb:Session=Depends(get_raw_db)):
    try :
        new_assign_project=Project_Assigned(
            e_id=response.e_id,
            pj_id=response.pj_id
        )
        db.add(new_assign_project) 
        db.commit
        
    
        return new_assign_project
    except Exception as e:
        raise HTTPException(status_code=500,detail=f'Not found!\n{e}')
    
@emp.put('/Update_name')
def update_table(response:updateResponse,background_Tasks:BackgroundTasks):
    try :
        if response.table_name=='employee':
            background_Tasks.add_task(
                update_employee,
                response
            )
            
            return {"Updation":"Successful","Table":"employee","Data":AddingNewEmployee(
                e_id=response.e_id,
                e_name=response.e_name,
                e_email=response.e_email,
                e_mobile_code=response.e_phone_code,
                e_mobile_no=response.e_phone_no,
                e_address=response.e_address,
                e_department=response.e_department,
                
            )}
        elif response.table_name=='department':
            background_Tasks.add_task(
                update_department,
                response
            )
            
            return {"Updation":"Successful","Table":"department","Data":departmentResponse(
                d_name=response.d_name,
                d_description=response.d_description,
                d_location=response.d_location                
            )}
        elif response.table_name=='projects':
            background_Tasks.add_task(
                update_project,
                response
            )
            return {"Updation":"Successfull","Table":"projects","Data":AddingNewProject(
                pj_name=response.pj_name,
                pj_description=response.pj_description,
            )}
        else :
            raise HTTPException(status_code=404,detail="Table is not selected")
    except Exception as e:
        raise HTTPException(status_code=404,detail=f'Cannot find data based on given id on the given table {e}')

def update_employee(response:updateResponse):
    try :
        db=SessionLocal()
        emp_person=db.query(Employee).filter(Employee.e_id==response.id).first()
        emp_person.e_full_name=response
        db.commit()
        
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Employee table Updation failed \n{e}")
    finally :
        db.close()
    
def update_department(response:updateResponse):
    try:
        db=SessionLocal()
        upd_dep=db.query(Department).filter(Department.d_id==response.d_id).first()
        upd_dep.d_name=response.d_name
        upd_dep.d_description=response.d_description
        upd_dep.d_location=response.d_location
        
        db.commit()
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Departement table Updation failed \n{e}")
    finally :
        db.close()
    
def update_project(response:updateResponse):
    try:
        db=SessionLocal()
        upd_proj=db.query(Project).filter(Project.pj_id==response.pj_id).first()
        
        upd_proj.pj_name=response.pj_name
        upd_proj.pj_description=response.pj_description
        
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Project table Updation failed \n{e}")
    finally :
        db.close()
    
@emp.post("/adding_department")
def adding_department(response:departmentResponse,db:Session=Depends(get_db)):
    try:
        new_dept=Department(
            d_name=response.d_name.title(),
            d_description=response.d_name+' : '+response.d_description,
            d_location=response.d_location
        )
        db.add(new_dept)
        db.commit()
        
        return {"Adding":"Successful","Data":{"d_name":new_dept.d_name,"d_description":new_dept.d_description,"d_location":new_dept.d_location}}
    except Exception as e :
        raise HTTPException(status_code=500,detail=f"Adding new department failed \n{e}")
    
    
@emp.post("/adding_new_project")
def add_new_project(response:AddingNewProject,db:Session=Depends(get_db)):
    try:
        new_project=Project(
            pj_name=response.pj_name.title(),
            pj_description=response.pj_name+' : '+response.pj_description
        )
        db.add(new_project)
        db.commit()
        
        return {"Adding":"Successful","Data":{"project_name":new_project.pj_name,"project_description":new_project.pj_description}}
    except Exception as e :
        raise HTTPException(status_code=500,detail=f"Adding New Project Failed \n{e}")
    
@emp.post("/adding_building_block")
def add_building_block(response:addingBuildingLocation,db:Session=Depends(get_db)):
    try:
        new_block=Department_Location(
            d_block_name=response.d_block_name.title()
        )
        
        db.add(new_block)
        db.commit()
        return {"Adding":"Successful","Data":{"block_name":new_block.d_block_name}}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Adding New building block failed \n {e}")