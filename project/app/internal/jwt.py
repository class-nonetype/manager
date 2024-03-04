from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.maintainer import decode_token

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credential: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credential:
            if not credential.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Esquema de autorización inválida.")
            
            if not self.validate_jwt(credential.credentials):
                raise HTTPException(status_code=403, detail="Token inválido o token expirado.")
            
            return credential.credentials
        else:
            raise HTTPException(status_code=403, detail="Código de autorización inválido.")

    def validate_jwt(self, token: str) -> bool:
        token_validity = False

        try:
            payload = decode_token(token)
        except:
            payload = None
        if payload:
            token_validity = True
        return token_validity