from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..database import pwd_context
from ..models import User


def get_user(*, email: str, db: Session)-> User | None:

    db_user = db.query(User).filter(User.email == email).first()
    # if db_user is None:
    #     raise HTTPException(400, "No user found with this username, signup first!")

    # correct_pass: bool = pwd_context.verify(password, db_user.password) 

    # if not correct_pass:
    #     raise HTTPException(403, "missing correct credentials")
    
    return db_user