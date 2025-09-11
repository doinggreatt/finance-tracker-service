from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Request, HTTPException
from sqlalchemy import select

from src.db.config import DBSession
from src.db.models import Transaction
from src.service.users import get_user_by
from src.enums.users import UserLookupField
from src.schemas.finances import WriteSingleTransactionSchema, ReadSingleTransactionSchema


router = APIRouter(prefix="/finances", tags=["Finance"])
TZ = ZoneInfo("Asia/Almaty")

@router.post("", description="Add new transaction", response_model=ReadSingleTransactionSchema)
async def create(db_sess: DBSession, trnsctn_data: WriteSingleTransactionSchema, req: Request):

    user = await get_user_by(db_sess=db_sess, field=UserLookupField.REQUEST, value=req)

    if not user:
        raise HTTPException(status_code=404, detail="Not Found")

    if not trnsctn_data.date:
        trnsctn_data.date = datetime.now(tz=TZ)

    new_trnsctn = Transaction(
        user_id=user.id,
        description=trnsctn_data.description,
        is_income=trnsctn_data.is_income,
        value=trnsctn_data.value,
        date=trnsctn_data.date
    )

    db_sess.add(new_trnsctn)
    await db_sess.commit()

    return new_trnsctn


@router.get("", response_model=list[ReadSingleTransactionSchema])
async def get_user_transactions(db_sess: DBSession, req: Request):
    user = await get_user_by(db_sess=db_sess, field=UserLookupField.REQUEST, value=req)

    if not user:
        raise HTTPException(status_code=404, detail="Not Found")

    stmt = select(Transaction).where(Transaction.user_id == user.id)
    rslt = await db_sess.execute(stmt)

    trnsctns = rslt.scalars().all()

    return trnsctns

@router.delete("/{trnsctn_id}", status_code=204)
async def delete_user_transaction(db_sess: DBSession, trnsctn_id: int, req: Request):
    user = await get_user_by(db_sess=db_sess, field=UserLookupField.REQUEST, value=req)

    if not user:
        raise HTTPException(status_code=404, detail="Not Found")

    stmt = select(Transaction).where(Transaction.id == trnsctn_id)
    rslt = await db_sess.execute(stmt)

    trnsctn = rslt.scalars().one_or_none()

    if not trnsctn or trnsctn.user_id != user.id:
        raise HTTPException(status_code=404, detail="Not Found")

    await db_sess.delete(trnsctn)
    await db_sess.commit()

    return
