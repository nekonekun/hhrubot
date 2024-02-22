from hhrubot.adapter.headhunter import HeadhunterSettings, HeadhunterAppSession, HeadhunterUserSession
from hhrubot.adapter.redisgram import RedisGram


class BuildLoginURL:
    def __init__(
        self,
        settings: HeadhunterSettings,
    ):
        self.settings = settings

    def __call__(self, telegram_id: int):
        redirect_uri = self.settings.redirect_uri_template.format(telegram_id=telegram_id)
        return self.settings.auth_uri_template.format(client_id=self.settings.client_id, redirect_uri=redirect_uri)


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
        async with self.session.post(
            '/token',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={
                'client_id': self.settings.client_id,
                'client_secret': self.settings.client_secret,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': self.settings.redirect_uri_template.format(telegram_id=telegram_id)
            }
        ) as response:
            content = await response.json()
        await self.redisgram.update_data(data={'access_token': content['access_token']}, user_id=telegram_id)


class GetResumeList:
    def __init__(self, session: HeadhunterUserSession):
        self.session = session

    async def __call__(self):
        async with self.session.get(
            '/resumes/mine'
        ) as response:
            content = await response.json()
        return content
