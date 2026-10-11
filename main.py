import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import jwt
from jwt import InvalidTokenError

ISSUER = "https://idp.exam.local"
AUDIENCE = "tds-3wj4ix91.apps.exam.local"

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2okOHspNjgA+2rTLbeuY
cxiP/hG8C6Sb9iwg3yiLAA4HCnpITcbWCSelbvbYGuc3EbNy4xFyf5Cbj5DHJMID
EkryOgyd2giIIIBOUBj8S63uGcnRpOBh9NFatfNwheKuzsPuVNldu6A9cNteNpXc
WyJjG2axVfmq7i6SuKr1JoWYG7xTTAvKPujSl4OtsQfO3h5NepzdfXpr28oNnzfW
ed+zclR6BcmNNo/WVfJ4xyCLSf0BCOgdTgW6PdaChd1l9VDetJZVEgC5tkyvXsfI
SI6iyrYbKR0NEBSqq4XkadEjsCs4F1RncsS4LlgniT7GlkL9Mce3b0wGLs9/7ZIX
dQIDAQAB
-----END PUBLIC KEY-----"""

app = FastAPI(title="RS256 JWT Verification API", version="1.0.0")


class VerifyRequest(BaseModel):
    token: str


@app.get("/")
def health():
    return {"status": "ok", "endpoint": "/verify"}


@app.post("/verify")
def verify_token(body: VerifyRequest):
    try:
        # Explicitly restrict the accepted algorithm; validate signature, issuer,
        # audience and expiry. Require all response claims to be present.
        claims = jwt.decode(
            body.token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            issuer=ISSUER,
            audience=AUDIENCE,
            options={
                "require": ["exp", "iss", "aud", "sub", "email"],
                "verify_signature": True,
                "verify_exp": True,
                "verify_iss": True,
                "verify_aud": True,
            },
        )
        return {
            "valid": True,
            "email": claims["email"],
            "sub": claims["sub"],
            "aud": claims["aud"],
        }
    except (InvalidTokenError, KeyError, TypeError, ValueError):
        return JSONResponse(status_code=401, content={"valid": False})
