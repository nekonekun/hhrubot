from typing import List, Optional, Union, Dict
from pydantic import BaseModel, Field, EmailStr


class ResumeResumeNano(BaseModel):
    alternate_url: str = Field(..., description='URL резюме на сайте')
    id: str = Field(..., description='Идентификатор резюме')
    title: str = Field(..., description='Желаемая должность')


class FieldIncludesId(BaseModel):
    id: str = Field(..., description='Идентификатор')


class FieldIncludesIdName(FieldIncludesId):
    name: str = Field(..., description='Название')


class FieldIncludesIdNameUrl(FieldIncludesIdName):
    url: str = Field(..., description='URL получения информации о поле')


class ResumeObjectsDownloadPdfRtf(BaseModel):
    url: str = Field(..., description='Ссылка для получения PDF/RTF-версии резюме')


class ResumeObjectsDownload(BaseModel):
    pdf: ResumeObjectsDownloadPdfRtf = Field(..., description='PDF-версия резюме')
    rtf: ResumeObjectsDownloadPdfRtf = Field(..., description='RTF-версия резюме')


class ResumeObjectsCertificate(BaseModel):
    achieved_at: Optional[str] = Field(None, description='Дата получения (в формате `ГГГГ-ММ-ДД`)')
    owner: Optional[str] = Field(None, description='На кого выдан сертификат. Возвращается только для сертификатов с `type = microsoft`')
    title: Optional[str] = Field(None, description='Название сертификата')
    type: Optional[str] = Field(None, description='Тип сертификата. Доступные значения:\n\n* `custom`;\n* `microsoft`\n')
    url: Optional[str] = Field(None, description='Ссылка на страницу с описанием сертификата')


class ResumeObjectsEducationAdditional(BaseModel):
    name: str = Field(..., description='Название курса / теста')
    organization: str = Field(..., description='Организация, проводившая курс / тест')
    result: Optional[str] = Field(None, description='Специальность / специализация')
    year: float = Field(..., description='Год окончания / сдачи')


class ResumeObjectsEducationElementary(BaseModel):
    name: str = Field(..., description='Название учебного заведения')
    year: float = Field(..., description='Год окончания')


class ResumeObjectsEducationPrimary(BaseModel):
    name: str = Field(..., description='Название учебного заведения')
    name_id: Optional[str] = Field(None, description='Идентификатор учебного заведения')
    organization: Optional[str] = Field(None, description='Факультет')
    organization_id: Optional[str] = Field(None, description='Идентификатор факультета')
    result: Optional[str] = Field(None, description='Специальность / специализация')
    result_id: Optional[str] = Field(None, description='Идентификатор специальности / специализации')
    year: float = Field(..., description='Год окончания')


class ResumeObjectsEducation(BaseModel):
    additional: list[ResumeObjectsEducationAdditional] = Field(default_factory=lambda: [], description='Список куров повышения квалификации')
    attestation: list[ResumeObjectsEducationAdditional] = Field(default_factory=lambda: [], description='Список пройденных тестов или экзаменов')
    elementary: list[ResumeObjectsEducationElementary] = Field(default_factory=lambda: [], description='Среднее образование. Обычно заполняется только при отсутствии высшего образования')
    level: FieldIncludesIdName | None = Field(None, description='Уровень образования. Возможные значения приведены в поле `education_level` [справочника полей](#tag/Obshie-spravochniki/operation/get-dictionaries)')
    primary: list[ResumeObjectsEducationPrimary] = Field(default_factory=lambda: [], description='Список образований выше среднего')


class FieldIncludesLogoUrls(BaseModel):
    field_90: Optional[str] = Field(None, alias='90', description='URL логотипа с размером менее 90px по меньшей стороне')
    field_240: Optional[str] = Field(None, alias='240', description='URL логотипа с размером менее 240px по меньшей стороне')
    original: str = Field(..., description='URL необработанного логотипа')


class EmployersEmployerInfoShort(BaseModel):
    alternate_url: str = Field(..., description='Ссылка на описание работодателя на сайте')
    id: str = Field(..., description='Идентификатор работодателя')
    logo_urls: FieldIncludesLogoUrls | None = Field(None, description='Ссылки на изображения логотипов работодателя разных размеров. `original` — это необработанный логотип, который может быть большого размера. Если изначально загруженный компанией логотип меньше, чем 240px и/или 90px по меньшей стороне, то в соответствующих ключах будут ссылки на изображения оригинального размера. Объект может быть `null`, если компания не загрузила логотип. Клиент должен предусмотреть возможность отсутствия логотипа по указанной ссылке (ответ с кодом `404 Not Found`). Логотипы 90 и 240 присутствуют не во всех компаниях')
    name: str = Field(..., description='Название работодателя')
    url: str = Field(..., description='URL для получения полного описания работодателя')


class ResumeObjectsIndustry(BaseModel):
    id: str = Field(..., description='Идентификатор поля')
    name: str = Field(..., description='Название поля')


class ResumeObjectsExperienceProperties(BaseModel):
    area: FieldIncludesIdNameUrl | None = Field(None, description='Регион расположения организации. Элемент [справочника регионов](#tag/Obshie-spravochniki/operation/get-areas)')
    company: Optional[str] = Field(None, description='Название организации')
    company_id: Optional[str] = Field(None, description='Уникальный идентификатор организации')
    company_url: Optional[str] = Field(None, description='Сайт компании')
    description: Optional[str] = Field(None, description='Обязанности, функции, достижения')
    employer: EmployersEmployerInfoShort | None = Field(None, description='Работодатель')
    end: Optional[str] = Field(None, description='Окончание работы (дата в формате `ГГГГ-ММ-ДД`)')
    industries: Optional[List[FieldIncludesIdName]] = Field(None, description='Список отраслей компании. Возможные значения приведены в [справочнике индустрий](#tag/Obshie-spravochniki/operation/get-industries)')
    industry: ResumeObjectsIndustry | None = Field(None, description='Отрасль компании')
    position: Optional[str] = Field(None, description='Должность')
    start: Optional[str] = Field(None, description='Начало работы (дата в формате `ГГГГ-ММ-ДД`)')


class ResumeObjectsExperience(ResumeObjectsExperienceProperties):
    start: str = Field(..., description='Начало работы (дата в формате `ГГГГ-ММ-ДД`)')
    position: str = Field(..., description='Должность')
    industries: List[FieldIncludesIdName] = Field(..., description='Список отраслей компании. Возможные значения приведены в [справочнике индустрий](#tag/Obshie-spravochniki/operation/get-industries)')


class ResumeObjectsSalaryProperties(BaseModel):
    amount: Optional[float] = Field(None, description='Сумма')
    currency: Optional[str] = Field(None, description='Идентификатор валюты. Возможные значения перечислены в массиве `currency` [справочника полей](#tag/Obshie-spravochniki/operation/get-dictionaries)')


class ResumeObjectsTotalExperience(BaseModel):
    months: Optional[float] = Field(None, description='Общий опыт работы в месяцах, с округлением до месяца')


class FieldIncludesContactPhoneValue(BaseModel):
    city: str = Field(..., description='Код города')
    country: str = Field(..., description='Код страны')
    formatted: str = Field(..., description='Отформатированный номер телефона')
    number: str = Field(..., description='Номер телефона')


class FieldIncludesContactProperties(BaseModel):
    comment: Optional[str] = Field(None, description='Комментарий к контакту')
    need_verification: Optional[bool] = Field(None, description='Требуется ли подтверждение телефона')
    preferred: Optional[bool] = Field(None, description='Является ли предпочтительным способом связи')
    type: Optional[FieldIncludesIdName] = Field(None, description='Тип контакта. Элемент справочника [preferred_contact_type](#tag/Obshie-spravochniki/operation/get-dictionaries)')
    value: Optional[Union[EmailStr, FieldIncludesContactPhoneValue]] = Field(None, description='Значение контакта. Для телефона - объект, для email - строка')
    verified: Optional[bool] = Field(None, description='Является ли телефон подтвержденным')


class FieldIncludesContact(FieldIncludesContactProperties):
    type: FieldIncludesIdName = Field(..., description='Тип контакта. Элемент справочника [preferred_contact_type](#tag/Obshie-spravochniki/operation/get-dictionaries)')
    value: Union[EmailStr, FieldIncludesContactPhoneValue] = Field(..., description='Значение контакта. Для телефона - объект, для email - строка')
    preferred: bool = Field(..., description='Является ли предпочтительным способом связи')


class ResumeResumeProfile(ResumeResumeNano):
    age: Optional[float] = Field(None, description='Возраст')
    area: FieldIncludesIdNameUrl | None = None
    can_view_full_info: Optional[bool] = Field(None, description='Доступен ли просмотр контактной информации в резюме текущему работодателю')
    certificate: List[ResumeObjectsCertificate] = Field(..., description='Список сертификатов соискателя', min_items=0)
    created_at: str = Field(..., description='Дата и время создания резюме')
    download: ResumeObjectsDownload = Field(..., description='Ссылки для скачивания резюме в разных форматах')
    education: ResumeObjectsEducation = Field(..., description='Образование соискателя. \n\nОсобенности сохранения образования:\n\n* Если передать и высшее и среднее образование и уровень образования "средний", то сохранится только среднее образование.\n* Если передать и высшее и среднее образование и уровень образования "высшее", то сохранится только высшее образование\n')
    experience: List[ResumeObjectsExperience] = Field(..., description='Опыт работы', min_items=0)
    first_name: Optional[str] = Field(None, description='Имя')
    gender: Optional[FieldIncludesIdName] = None
    hidden_fields: List[FieldIncludesIdName] = Field(..., description='Справочник [Список скрытых полей](https://github.com/hhru/api/blob/master/docs/employer_resumes.md#hidden-fields). Возможные значения элементов приведены в поле `resume_hidden_fields` [справочника полей](#tag/Obshie-spravochniki/operation/get-dictionaries)', min_items=0)
    last_name: Optional[str] = Field(None, description='Фамилия')
    marked: Optional[bool] = Field(False, description='Выделено ли резюме в поиске')
    middle_name: Optional[str] = Field(None, description='Отчество')
    platform: Optional[FieldIncludesId] = Field(None, description='Ресурс, на котором было размещено резюме')
    salary: Optional[ResumeObjectsSalaryProperties] = None
    total_experience: Optional[ResumeObjectsTotalExperience] = None
    updated_at: str = Field(..., description='Дата и время обновления резюме')


class CredsAnswers(BaseModel):
    answer_group: Optional[str] = Field(None, description='Группа данного ответа, positive, negative, neutral')
    answer_id: Optional[str] = Field(None, description='Идентификатор ответа (совпадает с ключом объекта)')
    ask_questions_after: Optional[List[str]] = Field(None, description='Вопросы которые нужно задать после использования пользователем данного ответа')
    description: Optional[str] = Field(None, description='Описание ответа')
    positive_title: Optional[str] = Field(None, description='Текст ответа который можно использовать для отображения без самого вопроса')
    skip_at_result: Optional[bool] = Field(None, description='Нужно ли пропускать данный ответ на форме с отображением кредов пользователя')
    title: Optional[str] = Field(None, description='Текст ответа который нужно отрисовать для сбора ответов от пользователя')


class CredsQuestions(BaseModel):
    description: Optional[str] = Field(None, description='Описание вопроса')
    is_active: Optional[bool] = Field(None, description='Показан ли вопрос изначально, актуально для динамических вопросов')
    possible_answers: Optional[List[str]] = Field(None, description='Возможные ответы на вопрос, гарантировано придут в поле answers', min_items=1)
    question_id: Optional[str] = Field(None, description='Идентификатор вопроса (совпадает с ключом объекта)')
    question_title: Optional[str] = Field(None, description='Текст вопроса отображаемый на форме')
    question_type: Optional[str] = Field(None, description='Возможность мульти выбора ответов на данный вопрос "single_choice" / "multi_select"')
    required: Optional[bool] = Field(None, description='Обязателен ли вопрос для получения ответа')
    skip_title_at_view: Optional[bool] = Field(None, description='Пропускать ли текст вопроса на просмотре, если false - ответы внутри placeholder, если true - просто перечисляем без текста вопроса')
    view_title: Optional[str] = Field(None, description='Текст вопроса на просмотре')


class CredsCreds(BaseModel):
    answers: Optional[Dict[str, CredsAnswers]] = Field(None, title='Ответы на креды, передается в виде answer_id -> object')
    question_to_answer_map: Optional[Dict[str, List[str]]] = Field(None, title='Выбранные для кредов ответы пользователя')
    questions: Optional[Dict[str, CredsQuestions]] = Field(None, title='Тело вопроса в виде question_id -> object')


class ResumeObjectsDriverLicenseTypes(BaseModel):
    id: str = Field(..., description='Категория водительских прав соискателя. Элемент справочника [тип водительских прав](#tag/Obshie-spravochniki/operation/get-dictionaries)')


class FieldIncludesLanguageProperties(FieldIncludesIdName):
    level: Optional[FieldIncludesIdName] = Field(None, description='Уровень владения. Возможные значения элементов приведены в поле `language_level` [справочника полей](#tag/Obshie-spravochniki/operation/get-dictionaries)')


class FieldIncludesLanguageLevel(FieldIncludesLanguageProperties):
    level: FieldIncludesIdName = Field(..., description='Уровень владения. Возможные значения элементов приведены в поле `language_level` [справочника полей](#tag/Obshie-spravochniki/operation/get-dictionaries)')


class ResumeObjectsMetroLine(BaseModel):
    hex_color: str = Field(..., description='Цвет линии в HEX-формате `RRGGBB` (от `000000` до `FFFFFF`)')
    id: str = Field(..., description='Идентификатор линии')
    name: str = Field(..., description='Название линии')


class ResumeObjectsMetroStation(BaseModel):
    id: str = Field(..., description='Идентификатор станции метро')
    lat: float = Field(..., description='Широта')
    line: ResumeObjectsMetroLine = Field(..., description='Линия метро')
    lng: float = Field(..., description='Долгота')
    name: Optional[str] = Field(None, description='Название станции метро')
    order: float = Field(..., description='Порядковый номер станции в линии метро')


class ResumeObjectsPaidServices(BaseModel):
    active: bool = Field(..., description='Активна ли в данный момент услуга')
    expires: Optional[str] = Field(None, description='Время окончания действия услуги, если услуга активна')
    id: str = Field(..., description='Идентификатор услуги')
    name: str = Field(..., description='Название услуги')


class ResumeObjectsRecommendation(BaseModel):
    contact: Optional[str] = Field(None, description='Контакт')
    name: str = Field(..., description='Имя выдавшего рекомендацию')
    organization: str = Field(..., description='Организация')
    position: str = Field(..., description='Должность')


class FieldIncludesArea(BaseModel):
    id: str = Field(..., description='Идентификатор региона из [справочника](#tag/Obshie-spravochniki/operation/get-areas)')
    name: str = Field(..., description='Название региона')
    url: str = Field(..., description='Ссылка на информацию о регионе')


class ResumeObjectsRelocationPublic(BaseModel):
    area: Optional[List[FieldIncludesArea]] = Field(None, description='Список городов, в которые возможен переезд. Имеет смысл только с соответствующим полем `type`')
    district: Optional[List[FieldIncludesIdName]] = Field(None, description='Список районов, в которые возможен переезд. Имеет смысл только с соответствующим полем `type`')
    type: FieldIncludesIdName = Field(..., description='Готовность к переезду. Элемент справочника [relocation_type](#tag/Obshie-spravochniki/operation/get-dictionaries)')


class ResumeObjectsSite(BaseModel):
    type: Optional[FieldIncludesIdName] = Field(None, description='Тип профиля. Элемент справочника [resume_contacts_site_type](#tag/Obshie-spravochniki/operation/get-dictionaries)')
    url: Optional[str] = Field(None, description='Ссылка на профиль или идентификатор')


class ResumeResumeFull(ResumeResumeProfile):
    birth_date: Optional[str] = Field(None, description='День рождения (в формате `ГГГГ-ММ-ДД`)')
    business_trip_readiness: FieldIncludesIdName = Field(..., description='Готовность к командировкам. Элемент справочника [business_trip_readiness](#tag/Obshie-spravochniki/operation/get-dictionaries)')
    citizenship: List[FieldIncludesIdNameUrl] = Field(..., description='Список гражданств соискателя. Элементы [справочника регионов](#tag/Obshie-spravochniki/operation/get-areas)')
    contact: List[FieldIncludesContact] = Field(..., description='Список контактов соискателя')
    creds: Optional[CredsCreds] = None
    driver_license_types: List[ResumeObjectsDriverLicenseTypes] = Field(..., description='Список категорий водительских прав соискателя')
    employment: Optional[FieldIncludesIdName] = None
    employments: List[FieldIncludesIdName] = Field(..., description='Список подходящих соискателю типов занятостей. Элементы справочника [employment](#tag/Obshie-spravochniki/operation/get-dictionaries)')
    has_vehicle: Optional[bool] = Field(None, description='Наличие личного автомобиля у соискателя')
    language: List[FieldIncludesLanguageLevel] = Field(..., description='Список языков, которыми владеет соискатель. Элементы справочника [languages](#tag/Obshie-spravochniki/operation/get-languages)')
    metro: Optional[ResumeObjectsMetroStation] = None
    paid_services: List[ResumeObjectsPaidServices] = Field(..., description='Платные услуги по резюме')
    professional_roles: Optional[List[FieldIncludesIdName]] = Field(None, description='Массив объектов профролей')
    recommendation: List[ResumeObjectsRecommendation] = Field(..., description='Список рекомендаций')
    relocation: ResumeObjectsRelocationPublic = Field(..., description='Возможность переезда')
    resume_locale: FieldIncludesIdName = Field(..., description='Язык, на котором составлено резюме (локаль). Элемент справочника [локали резюме](#tag/Obshie-spravochniki/operation/get-locales)')
    schedule: FieldIncludesIdName
    schedules: List[FieldIncludesIdName] = Field(..., description='Список подходящих соискателю графиков работы. Элементы справочника [schedule](#tag/Obshie-spravochniki/operation/get-dictionaries)')
    site: List[ResumeObjectsSite] = Field(..., description='Профили в соц. сетях и других сервисах')
    skill_set: List[str] = Field(..., description='Ключевые навыки (список уникальных строк)')
    skills: Optional[str] = Field(None, description='Дополнительная информация, описание навыков в свободной форме')
    travel_time: FieldIncludesIdName = Field(..., description='Желательное время в пути до работы. Элемент справочника [travel_time](#tag/Obshie-spravochniki/operation/get-dictionaries)')
    work_ticket: List[FieldIncludesIdNameUrl] = Field(..., description='Список регионов, в которых соискатель имеет разрешение на работу. Элементы [справочника регионов](#tag/Obshie-spravochniki/operation/get-areas)\n')
