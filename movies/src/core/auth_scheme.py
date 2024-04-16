import time
from http import HTTPStatus

import aiohttp
from fastapi import HTTPException, Request, Response
from fastapi.security import HTTPBearer
from jose import jwt
from passlib.context import CryptContext

from .config import fastapi_config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request, response: Response) -> dict:

        token_dirty = request.cookies.get("Authorization")

        if not token_dirty or token_dirty == '':
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail='Invalid authorization code.')
        if not token_dirty[:6] == 'Bearer':
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail='Only Bearer token might be accepted')
        decoded_token = self.parse_token(token_dirty[7:])
        token_user_agent: str = decoded_token.get("user_agent")
        user_agent: str = request.headers.get("user-agent")

        if not decoded_token or user_agent != token_user_agent:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail='Invalid token.')
        expire = decoded_token.get("exp")
        if int(time.time()) < expire:
            return decoded_token

        session = aiohttp.ClientSession()
        url = 'http://auth:8081/auth/api/v1/auth/refresh'
        cookies = {'Authorization': request.cookies.get('Authorization'),
                   'refresh_token': request.cookies.get('refresh_token')}
        headers = {'user-agent': request.headers.get('user-agent')}

        async with session.get(url, cookies=cookies, headers=headers) as resp:
            status = resp.status
            body = await resp.json()
            new_token = body.get('access_token')
            new_refresh_token = body.get('refresh_token')

        await session.close()

        if status != HTTPStatus.OK:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail='Tokens are expired.')

        response.set_cookie(
            key="refresh_token", httponly=True, value=new_refresh_token)
        response.set_cookie(
            key="Authorization", httponly=True, value=f"Bearer {new_token}")
        decoded_token = self.parse_token(new_token) # взять из ретурна сессии

        return decoded_token

    @staticmethod
    def parse_token(jwt_token: str):
        return jwt.decode(
            jwt_token,
            fastapi_config.SECRET_KEY,
            algorithms=fastapi_config.ALGORITHM,
            options={"verify_exp": False},)


security_jwt = JWTBearer()
