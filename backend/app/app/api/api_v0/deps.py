from typing import AsyncGenerator, Optional

from authlib.integrations.base_client import BaseOAuth
from authlib.integrations.starlette_client.apps import StarletteOAuth1App, StarletteOAuth2App
from authlib.integrations.starlette_client.integration import StarletteIntegration
from authlib.oidc.core import UserInfo
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.openapi.models import OpenIdConnect as OpenIdConnectModel
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from httpx import HTTPStatusError
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.core.settings import settings
from app.db.session import async_session


def add_swagger_config(app: FastAPI) -> None:
    app.swagger_ui_init_oauth = {
        "usePkceWithAuthorizationCodeGrant": True,
        "useBasicAuthenticationWithAccessCodeGrant": True,
        "clientId": settings.OIDC_CLIENT_ID,
        "clientSecret": settings.OIDC_CLIENT_SECRET,
        "scopes": settings.OIDC_SCOPES,
        "appName": "fastapi-keycloak-demo",
    }


class StarletteOAuth2AppCustom(StarletteOAuth2App):
    async def fetch_userinfo(self, access_token: str, **kwargs) -> UserInfo:  # type: ignore
        metadata = await self.load_server_metadata()

        # TODO: Using end_session_endpoint

        userinfo_endpoint = metadata.get("userinfo_endpoint")
        if not userinfo_endpoint:
            raise RuntimeError('Missing "userinfo_endpoint" value')

        async with self._get_oauth_client(**metadata) as client:
            # resp = await client.request(
            #     "POST",
            #     userinfo_endpoint,
            #     withhold_token=True,
            #     data={
            #         "token": access_token,
            #         "client_id": client.client_id,
            #         "client_secret": client.client_secret,
            #     },
            #     **kwargs,
            # )
            resp = await client.request(
                "GET",
                userinfo_endpoint,
                withhold_token=True,
                # params={
                #     "access_token": access_token,
                #     # "token": access_token,
                #     # "client_id": client.client_id,
                #     # "client_secret": client.client_secret,
                # },
                headers={
                    # "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Bearer {access_token}",
                },
            )
        resp.raise_for_status()
        data = resp.json()

        # active = data.get("active")

        # if active is None:
        #     raise RuntimeError('Missing "active" value')

        # if active is False:
        #     return None

        return UserInfo(data)


class OAuthCustom(BaseOAuth):
    oauth1_client_cls = StarletteOAuth1App
    oauth2_client_cls = StarletteOAuth2AppCustom
    framework_integration_cls = StarletteIntegration

    def __init__(self, config=None, cache=None, fetch_token=None, update_token=None) -> None:  # type: ignore
        super(OAuthCustom, self).__init__(
            cache=cache, fetch_token=fetch_token, update_token=update_token
        )
        self.config = config


oauth = OAuthCustom()
oauth.register(
    name="stockk_oidc",
    client_id=settings.OIDC_CLIENT_ID,
    client_secret=settings.OIDC_CLIENT_SECRET,
    server_metadata_url=settings.OIDC_DISCOVERY_URL,
    client_kwargs={
        "scope": settings.OIDC_SCOPES,
        "code_challenge_method": "S256",
    },  # enable PKCE
)


class OpenIdConnectWithCookie(SecurityBase):
    def __init__(
        self,
        *,
        openIdConnectUrl: str,
        scheme_name: Optional[str] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        self.model = OpenIdConnectModel(openIdConnectUrl=openIdConnectUrl, description=description)
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> Optional[str]:
        # TODO: Get userinfo instead of call api
        if access_token := request.cookies.get("access_token"):
            return access_token
        authorization = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        return None if not authorization or scheme.lower() != "bearer" else param


reusable_oidc = OpenIdConnectWithCookie(openIdConnectUrl=settings.OIDC_DISCOVERY_URL)


async def get_db() -> AsyncGenerator:
    """
    Dependency function that yields db sessions
    """
    async with async_session() as session:
        yield session
        await session.commit()


async def get_userinfo_from_token(accessToken: str) -> schemas.OIDCUser:
    try:
        userInfo = await oauth.stockk_oidc.fetch_userinfo(access_token=accessToken)
    except HTTPStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    if not userInfo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        oidcUser = schemas.OIDCUser(**userInfo)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        ) from e
    return oidcUser


async def get_current_user_from_oidc(
    db: AsyncSession = Depends(get_db),
    tokenOidc: Optional[str] = Depends(reusable_oidc),
) -> models.User:
    if tokenOidc is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    oidcUser = await get_userinfo_from_token(tokenOidc)
    user, _ = await crud.user.get_or_create_by_email(
        db, email=oidcUser.email, full_name=oidcUser.name
    )
    return user


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    tokenOidc: Optional[str] = Depends(reusable_oidc),
) -> models.User:
    if tokenOidc is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return await get_current_user_from_oidc(db=db, tokenOidc=tokenOidc)


async def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return current_user


async def get_current_oidc_user(
    tokenOidc: Optional[str] = Depends(reusable_oidc),
) -> schemas.OIDCUser:
    if tokenOidc is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await get_userinfo_from_token(tokenOidc)


async def get_influxdb_client(request: Request) -> InfluxDBClientAsync:
    """
    Dependency function that yields redis connection
    """
    if not hasattr(request.app.state, "influxdb_client"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="influxdb_client attribute not set on app state",
        )
    return request.app.state.influxdb_client
