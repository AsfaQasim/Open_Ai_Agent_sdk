from pydantic import BaseModel

class MyDataOutput(BaseModel):
    is_hotel_asfas_query: bool
    is_hotel_asfas_account_or_tax_query: bool
    reason: str
    