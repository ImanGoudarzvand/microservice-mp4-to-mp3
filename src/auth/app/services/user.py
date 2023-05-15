from sqlalchemy.orm import Session
from ..database import pwd_context
from ..models import User


def create_user(*, email, password, db: Session) -> User:

    hashed_password = pwd_context.hash(password)
    
    db_user = User(email=email, password = hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user