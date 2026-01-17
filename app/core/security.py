from fastapi import HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials

from app.utils import decode_access_token

# MUST match your login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


class AccessTokenBearer(HTTPBearer):
    async def __call__(
        self,
        request: Request,
    ) -> dict:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        token = credentials.credentials
        token_data = decode_access_token(token)

        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )

        return token_data


access_token_bearer = AccessTokenBearer()
