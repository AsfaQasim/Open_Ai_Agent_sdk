# from dataclasses import dataclass
from pydantic import BaseModel


#  data class(schema)
# @dataclass
# class UserDataType: 
#     name: str
#     age: int
#     role: str
    
#  pydantic schema

class UserData(BaseModel):
    name : str
    age: int
    role: str