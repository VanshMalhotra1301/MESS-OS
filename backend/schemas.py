from pydantic import BaseModel

class InventoryCreate(BaseModel):
    item_name: str
    category: str
    current_stock: float
    unit: str

class MenuUpdate(BaseModel):
    day: str
    meal: str
    items: str # "Dal, Rice, Roti"

class StudentRegister(BaseModel):
    full_name: str
    roll_number: str
    email: str