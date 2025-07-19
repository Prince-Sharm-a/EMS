from pydantic import BaseModel, Field
from typing import Optional,List,Dict
from datetime import datetime

class EmployeeResponse(BaseModel):
    e_id:int
    e_full_name:str
    e_phone_num:str
    e_joining_date:datetime
    d_name:str
    d_block:str
    e_salary:float
    
    class Config:
        from_attributes=True
    
class AttendanceResponse(BaseModel):
    e_id:int
    e_full_name:str
    date:datetime
    working_hours:float
    
    class Config:
        from_attributes=True
        
class AddingNewEmployee(BaseModel):
    e_name:str
    e_email:str
    e_mobile_code:Optional[str]="+91"
    e_mobile_no:str
    e_address:Optional[str]="0"
    e_department:int
    e_salary:float
    
    class Config:
        from_attributes=True
    
class departmentResponse(BaseModel):
    d_name:str
    d_description:Optional[str]=0
    d_location:int
    
    class Config:
        from_attributes=True
        
        

class projectAssign(BaseModel):
    e_id:int
    e_full_name:Optional[str]="0"
    pj_id:int
    pj_name:Optional[str]="0"
    pj_description:Optional[str]="0"
    
    class Config:
        from_attributes=True
        
class AddingNewProject(BaseModel):
    pj_name:Optional[str]='0'
    pj_description:Optional[str]=pj_name
    
    class Config:
        from_attributes=True
    
class checkIn(BaseModel):
    e_id:int
    Check_in_time:Optional[datetime]=datetime.now()
    
    class Config:
        from_attributes=True
    
class checkOut(BaseModel):
    e_id:int
    Check_out_time:Optional[datetime]=datetime.now()    
    
    class Config:
        from_attributes=True
        
class updateResponse(BaseModel):
    e_id:Optional[int]=0
    e_name:Optional[str]="0"
    e_address:Optional[str]="0"
    e_phone_code:Optional[str]='+91'
    e_email:Optional[str]="0"
    e_phone_no:Optional[str]='0'
    e_department:Optional[int]=0
    
    d_id:Optional[int]=0
    d_name:Optional[str]='0'
    d_description:Optional[str]="0"
    d_location:Optional[str]="0"
    Salary_Before_Deduction:Optional[float]=0
    
    pj_id:Optional[int]=0
    pj_name:Optional[str]="0"
    pj_description:Optional[str]="0"
    
    table_name:str
    class Config:
        from_attributes=True

class addingBuildingLocation(BaseModel):
    d_block_name:str
    class Config:
        from_attributes=True