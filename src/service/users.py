from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Request, HTTPException

from src.config.security import authx as security
from src.db.models import User
from src.schemas.users import WriteSingleUserSchema, AuthorizeSingleAccessTokenSchema
from src.enums.users import UserLookupField



async def get_user_by(
        *,
        db_sess: AsyncSession,
        field: UserLookupField,
        value: str | int | Request
) -> User | None:
    """Get user by some field"""
    stmt = None

    match field:
        case UserLookupField.USERNAME:
            stmt = select(User).where(User.username == value)
        case UserLookupField.ID:
            stmt = select(User).where(User.id == int(value))
        case UserLookupField.TOKEN:
            sub = security.verify_token(value).sub
            stmt = select(User).where(User.id == int(sub))
        case UserLookupField.REQUEST:
            token = await security.get_access_token_from_request(value)
            sub = security.verify_token(token).sub
            print(sub)
            stmt = select(User).where(User.id == int(sub))
        case _:
            raise ValueError(f"unsupported lookup: {field}")

    res = await db_sess.execute(stmt)
    res = res.scalar_one_or_none()

    return res


async def create(*, db_sess: AsyncSession, user_data: WriteSingleUserSchema) -> User:
    """Create new user"""
    if await get_user_by(db_sess=db_sess,
                         field=UserLookupField.USERNAME,
                         value=user_data.username):

        raise HTTPException(
            status_code=400,
            detail="This username is already taken."
        )

    try:
        new_user = User(**user_data.model_dump(exclude={"password", "password_2"}))
        new_user.set_password(user_data.password)

        db_sess.add(new_user)
        await db_sess.commit()
        await db_sess.refresh(new_user)

        return new_user

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

async def authorize(*, db_sess: AsyncSession, auth_data: AuthorizeSingleAccessTokenSchema) -> dict[str, str]:
    """Authorizes user"""
    user = await get_user_by(db_sess=db_sess, field=UserLookupField.USERNAME, value=auth_data.username)

    if user and user.verify_password(auth_data.password):
        access_token = security.create_access_token(uid=str(user.id))
        return {'access_token': access_token}


    raise HTTPException(status_code=401, detail="Wrong Credentials")
