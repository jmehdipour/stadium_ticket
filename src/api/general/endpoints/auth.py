from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from mongoengine import NotUniqueError

from src.api.schemas import UserOut, UserIn
from src.auth.jwt import create_access_token, authenticate_user, get_password_hash, \
    get_current_user
from src.auth.schemas import Token
from src.config import get_settings
from src.data.connections.mongodb import counter
from src.data.models.mongodb import User

router = APIRouter()


@router.get("/users/me/", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user.to_mongo()


@router.post("/auth/sign_up", response_model=UserOut)
async def sign_up_new_user(user_data: UserIn):
    try:
        mongo_user = User(id=counter('user'), **user_data.dict(exclude={'password'}),
                          hashed_password=get_password_hash(user_data.password))
        mongo_user.save()
    except NotUniqueError as ex:
        raise HTTPException(status_code=409, detail="duplicate email address")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="internal server error")
    return mongo_user.to_mongo()


@router.post("/auth/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
