import os

import dramatiq
import httpx

from hhrubot.application.texpdf import render


@dramatiq.actor
def make_documents(*, telegram_id: int, filename: str, resume: dict):
    render(filename, resume)
    base_url = os.getenv('HHRU_BOT_API_URL').rstrip('/')
    httpx.post(f'{base_url}/internal/tex-pdf/', json={'telegram_id': telegram_id, 'filename': filename})
