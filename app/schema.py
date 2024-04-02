from pydantic import BaseModel

class PokeBase(BaseModel):
    title: str
    content : str
    published : bool = True #passing a default value makes a field optional
    #using optional (standard)
    
class PostCreate(PokeBase):
    pass

#This schema is used as a response model for our application to send response in the standarized format
class Post(BaseModel):
    title: str
    published : bool
    
    class Config:
        orm_mode = True