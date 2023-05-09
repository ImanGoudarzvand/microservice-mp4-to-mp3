from typing import List
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from .models import User, Base
from .database import engine, SessionLocal, pwd_context
from .schemas import User, UserCreate, UserLogin
from app.services.user import create_user
from app.selectors.user import get_user
from app.jwt.auth_handler import signJWT, decodeJWT
from app.jwt.jwt_bearer import JWTBearer


Base.metadata.create_all(bind=engine)

server = FastAPI()

# server.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend())

def get_db():
    db = SessionLocal()
    try:
        yield db  

    finally: 
        db.close()


@server.post('/signup/', response_model = User)
def register(
    request: Request,
    user: UserCreate,
    db: Session = Depends(get_db)):

    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code= 400, detail="email already registered!")


    if user.confirm_password != user.password:
        raise HTTPException(status_code= 400, detail="password and confirm password must match!")

    # save in the database (business logic)
    user_db = create_user(email = user.email, password = user.password, db=db)
        
    return user_db

    

@server.post('/login/')
def login(request: Request,
          user: UserLogin,
          db: Session = Depends(get_db)):


    user_db = get_user(email=user.email, db=db)

    if user_db is None:
        raise HTTPException(400, "No user found with this username, signup first!")

    correct_pass: bool = pwd_context.verify(user.password, user_db.password) 

    if not correct_pass:
        raise HTTPException(403, "missing Credentials")
   
    access_token = signJWT(user.email)
    return access_token


@server.get('/validate/', dependencies=[Depends(JWTBearer())])
def validate(request: Request):

    authorization = request.headers.get('Authorization')
    if authorization:
        token = authorization.split(" ")[1]
        payload = decodeJWT(token)
        print(payload)
        if payload is None:
            raise HTTPException(status_code=403, detail="expired token. give a fresh jwt again!")
        elif payload == {}:
            raise HTTPException(status_code=403, detail="missing credentials, wrong token")
        return {"message": "You are authenticated!" ,"payload": payload}
    raise HTTPException(status_code=403, detail="Invalid authentication scheme.")


