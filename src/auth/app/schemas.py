from pydantic import BaseModel, validator
from fastapi import HTTPException, status
from .validators import (number_validator,
                        special_char_validator,
                        letter_validator,
                        min_length_validator,
                        simple_email_validator)

class User(BaseModel):
    email: str 

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str  

    @validator('password')
    def check_password_is_not_blank(cls, v):
        
        min_length_validator(v) # ro make sure password is set
        return v

    @validator('email')
    def check_email_is_not_blank(cls, v):
        
        if v == " " :   # ro make sure email is set
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Please enter your email!")

        return v
        



class UserCreate(BaseModel):
    email: str
    password: str  
    confirm_password: str

    @validator('password')
    def password_must_contain_letter_number_special_char(cls, v):
        
        min_length_validator(v)
        number_validator(v)
        special_char_validator(v)
        letter_validator(v)
    
        return v

    @validator('email')
    def check_if_email_is_a_proper_email(cls, v):
        
        simple_email_validator(v)
    
        return v
        