from hhrubot.adapter.headhunter import (
    HeadhunterAppSession,
    HeadhunterSettings,
    HeadhunterUserSession,
)
from hhrubot.adapter.redisgram import RedisGram
from hhrubot.application.resume_full_model import ResumeResumeFull
from hhrubot.application.resumes_mine_model import ResumesMineResponse


class BuildLoginURL:
    def __init__(
        self,
        settings: HeadhunterSettings,
    ):
        self.settings = settings

    def __call__(self, telegram_id: int):
        redirect_uri = self.settings.redirect_uri_template.format(
            telegram_id=telegram_id,
        )
        return self.settings.auth_uri_template.format(
            client_id=self.settings.client_id,
            redirect_uri=redirect_uri,
        )


class AuthenticateUser:
    def __init__(
        self,
        session: HeadhunterAppSession,
        settings: HeadhunterSettings,
        redisgram: RedisGram,
    ):
        self.session = session
        self.settings = settings
        self.redisgram = redisgram

    async def __call__(self, telegram_id: int, code: str):
        redirect_uri = self.settings.redirect_uri_template.format(
            telegram_id=telegram_id,
        )
        async with self.session.post(
            '/token',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={
                'client_id': self.settings.client_id,
                'client_secret': self.settings.client_secret,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': redirect_uri,
            },
        ) as response:
            content = await response.json()
        await self.redisgram.update_data(
            data={'access_token': content['access_token']},
            user_id=telegram_id,
        )


class GetResumeList:
    def __init__(self, session: HeadhunterUserSession):
        self.session = session

    async def __call__(self) -> ResumesMineResponse:
        async with self.session.get(
            '/resumes/mine',
        ) as response:
            content = await response.json()
        return ResumesMineResponse.model_validate(content)


class GetResume:
    def __init__(self, session: HeadhunterUserSession):
        self.session = session

    async def __call__(self, resume_id: str) -> ResumeResumeFull:
        async with self.session.get(f'/resumes/{resume_id}') as response:
            content = await response.json()
        return ResumeResumeFull.model_validate(content)
