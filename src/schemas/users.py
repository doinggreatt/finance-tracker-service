from pydantic import BaseModel, model_validator


class WriteSingleUserSchema(BaseModel):
    username: str
    password: str
    password_2: str

    @model_validator(mode="after")
    def validate_passwords_match(self) -> "WriteSingleUserSchema":
        if self.password != self.password_2:
            raise ValueError("password should match")
        return self

class ReadSingleUserSchema(BaseModel):
    id: int
    username: str
    balance: float


class AuthorizeSingleAccessTokenSchema(BaseModel):
    username: str
    password: str

class ReadSingleAccessTokenSchema(BaseModel):
    access_token: str
