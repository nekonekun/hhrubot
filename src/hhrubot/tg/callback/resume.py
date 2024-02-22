from aiogram.filters.callback_data import CallbackData


class ResumeData(CallbackData, prefix='resume'):
    resume_id: str
