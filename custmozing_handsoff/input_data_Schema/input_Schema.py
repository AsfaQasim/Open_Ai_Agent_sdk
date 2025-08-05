from pydantic import BaseModel

class MyInputData(BaseModel):
    reason: str
    