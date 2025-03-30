from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    webauthn_auth_options: Optional[dict] = None


class TokenPayload(BaseModel):
    sub: str
    exp: int 