from pydantic import BaseModel

#Input Schema 
class BlogCreate(BaseModel):
    title : str
    content : str

class BlogResponse(BaseModel):
    id : int
    title : str
    content : str
    is_active : bool

    class Config:
        from_attributes = True
        
