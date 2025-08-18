from pydantic import BaseModel

class User(BaseModel):
    query: str
    