from contextlib import asynccontextmanager
from typing import AsyncIterable

import aiohttp
from pydantic import BaseModel


class HeadhunterSettings(BaseModel):
    client_id: str
    client_secret: str
    app_token: str
    redirect_uri_template: str
    auth_uri_template: str
    api_url: str
    app_name: str
    app_version: str
    contact_email: str


class HeadhunterAppSession(aiohttp.ClientSession):
    pass


class HeadhunterUserSession(aiohttp.ClientSession):
    pass


class HeadhunterAccessToken(str):
    pass


class HeadhunterAppSessionFactory:
    def __init__(self, settings: HeadhunterSettings):
        self.settings = settings

    @asynccontextmanager
    async def __call__(self) -> AsyncIterable[HeadhunterAppSession]:
        base_url = self.settings.api_url
        headers = {
            'Authorization': f'Bearer {self.settings.app_token}',
            'Content-Type': 'application/json',
            'HH-User-Agent': f'{self.settings.app_name}/{self.settings.app_version} ({self.settings.contact_email})'
        }
        async with HeadhunterAppSession(base_url, headers=headers) as session:
            yield session


class HeadhunterUserSessionFactory:
    def __init__(self, settings: HeadhunterSettings):
        self.settings = settings

    @asynccontextmanager
    async def __call__(self, access_token: HeadhunterAccessToken) -> AsyncIterable[HeadhunterUserSession]:
        base_url = self.settings.api_url
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'HH-User-Agent': f'{self.settings.app_name}/{self.settings.app_version} ({self.settings.contact_email})'
        }
        async with HeadhunterUserSession(base_url, headers=headers) as session:
            yield session
