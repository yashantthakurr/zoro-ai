
from pydantic import BaseModel

class AccessToken(BaseModel):

    access_token: str
    username: str
    role: str
    token_type: str
    