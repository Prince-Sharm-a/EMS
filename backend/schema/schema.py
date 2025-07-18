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
    e_address:Optional[str]=None
    e_department:Optional[int]=0
    e_joining_date:Optional[datetime]=None
    e_salary:float
    
    class Config:
        from_attributes=True
    
class departmentResponse(BaseModel):
    d_name:str
    d_description:Optional[str]=None
    d_location:int
    
    class Config:
        from_attributes=True
        
        

class projectAssign(BaseModel):
    e_id:int
    e_full_name:Optional[str]=None
    pj_id:int
    pj_name:Optional[str]=None
    pj_description:Optional[str]=None
    
    class Config:
        from_attributes=True
        
class AddingNewProject(BaseModel):
    pj_name:Optional[str]=None
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
    e_id:Optional[int]=None
    e_name:Optional[str]=None
    e_address:Optional[str]=None
    e_phone_code:Optional[str]='+91'
    e_email:Optional[str]=None
    e_phone_no:Optional[str]=None
    e_department:Optional[int]=None
    
    d_id:Optional[str]=None
    d_name:Optional[str]=None
    d_description:Optional[str]=None
    d_location:Optional[str]=None
    Salary_Before_Deduction:Optional[float]=None
    
    pj_id:Optional[int]=None
    pj_name:Optional[str]=None
    pj_description:Optional[str]=None
    
    table_name:str
    class Config:
        from_attributes=True

class addingBuildingLocation(BaseModel):
    d_block_name:str
    class Config:
        from_attributes=True