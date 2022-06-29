from pydantic import BaseModel


class MonkeyBase(BaseModel):
    monkey_name: str
    monkey_age: int
    species: str
    gender: str

class MonkeyAdd(MonkeyBase):
    monkey_id: str
    vip: bool
    
    class Config:
        orm_mode = True

class Monkey(MonkeyAdd):
    id: int
    
    class Config:
        orm_mode = True
        
class UpdateMonkey(BaseModel):
    vip: bool
    
    class Config:
        orm_mode = True
