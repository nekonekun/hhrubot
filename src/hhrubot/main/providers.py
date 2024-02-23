import os
from typing import AsyncIterator

from dishka import Provider, Scope, provide

from hhrubot.adapter.headhunter import (
    HeadhunterAccessToken,
    HeadhunterAppSession,
    HeadhunterAppSessionFactory,
    HeadhunterSettings,
    HeadhunterUserSession,
    HeadhunterUserSessionFactory,
)
from hhrubot.application.headhunter import AuthenticateUser, BuildLoginURL, GetResumeList, GetResume


class HeadhunterOfflineProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> HeadhunterSettings:
        return HeadhunterSettings(
            client_id=os.getenv('HEADHUNTER_CLIENT_ID'),
            client_secret=os.getenv('HEADHUNTER_CLIENT_SECRET'),
            app_token=os.getenv('HEADHUNTER_APP_TOKEN'),
            redirect_uri_template=os.getenv('HEADHUNTER_REDIRECT_URI_TEMPLATE'),
            auth_uri_template=os.getenv('HEADHUNTER_AUTH_URI_TEMPLATE'),
            api_url=os.getenv('HEADHUNTER_API_URL'),
            app_name=os.getenv('HEADHUNTER_APP_NAME'),
            app_version=os.getenv('HEADHUNTER_APP_VERSION'),
            contact_email=os.getenv('HEADHUNTER_CONTACT_EMAIL'),
        )

    build_login_url = provide(BuildLoginURL, scope=Scope.APP)


class HeadhunterOnlineProvider(Provider):
    session_factory = provide(HeadhunterAppSessionFactory, scope=Scope.APP)
    employee_session_factory = provide(HeadhunterUserSessionFactory, scope=Scope.APP)

    @provide(scope=Scope.REQUEST)
    async def get_app_session(self, factory: HeadhunterAppSessionFactory) -> AsyncIterator[HeadhunterAppSession]:
        async with factory() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def get_employee_session(
        self,
        factory: HeadhunterUserSessionFactory,
        access_token: HeadhunterAccessToken,
    ) -> AsyncIterator[HeadhunterUserSession]:
        async with factory(access_token=access_token) as session:
            yield session


class HeadhunterMethodsProvider(Provider):
    authenticate_user = provide(AuthenticateUser, scope=Scope.REQUEST)
    get_resume_list = provide(GetResumeList, scope=Scope.REQUEST)
    get_resume = provide(GetResume, scope=Scope.REQUEST)
