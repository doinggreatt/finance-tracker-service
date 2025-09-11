from fastapi import APIRouter, Request, HTTPException

from src.db import DBSession
from src.schemas.users import WriteSingleUserSchema, ReadSingleUserSchema, AuthorizeSingleAccessTokenSchema, ReadSingleAccessTokenSchema
from src.enums.users import UserLookupField
from src.service.users import create, get_user_by, authorize

router = APIRouter(prefix="/users")

@router.post("", response_model=ReadSingleUserSchema)
async def create_user(db_sess: DBSession, user_data: WriteSingleUserSchema):
    user = await create(db_sess=db_sess, user_data=user_data)
    return user



@router.get("/me", response_model=ReadSingleUserSchema)
async def me(db_sess: DBSession, req: Request):
    user = await get_user_by(db_sess=db_sess, field=UserLookupField.REQUEST, value=req)
    if not user:
        raise HTTPException(status_code=404, detail="Not Found")
    return user

@router.post("/authorize", response_model=ReadSingleAccessTokenSchema)
async def authorize_user(db_sess: DBSession, auth_data: AuthorizeSingleAccessTokenSchema):
    access_token = await authorize(db_sess=db_sess, auth_data=auth_data)

    return access_token

