from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.sqltypes import LargeBinary, DateTime
from argon2.exceptions import VerifyMismatchError


from .config import Base
from .utils import hash_password, hasher


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    username: Mapped[str]
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    balance: Mapped[float] = mapped_column(nullable=False, default=0.00)


    def set_password(self, password: str) -> None:
        """Set a new password for the user."""
        if not password:
            raise ValueError("Password cannot be empty")
        password = bytes(password, encoding='utf-8')
        self.password = hash_password(password)

    def verify_password(self, password: str) -> bool:
        """Verifies inputted password with user's password."""
        if not password:
            return False
        try:
            verify: bool = hasher.verify(self.password, password)
            return verify
        except VerifyMismatchError:
            return False

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    description: Mapped[str]
    is_income: Mapped[bool] = mapped_column(nullable=False, default=True)
    value: Mapped[float]
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


