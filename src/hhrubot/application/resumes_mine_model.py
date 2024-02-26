from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


class ResumeObjectsDownloadPdfRtf(BaseModel):
    url: str = Field(..., description='Ссылка для получения PDF/RTF-версии резюме')


class ResumeObjectsDownload(BaseModel):
    pdf: ResumeObjectsDownloadPdfRtf = Field(..., description='PDF-версия резюме')
    rtf: ResumeObjectsDownloadPdfRtf = Field(..., description='RTF-версия резюме')


class ResumeObjectsActionsForOwner(BaseModel):
    download: ResumeObjectsDownload = Field(..., description="Ссылки для скачивания резюме в нескольких форматах ([подробнее](#tag/Prosmotr-rezyume/operation/get-resume)) (атрибут 'actions')\n")


class FieldIncludesId(BaseModel):
    id: str = Field(..., description='Идентификатор')


class FieldIncludesIdName(FieldIncludesId):
    name: str = Field(..., description='Название')


class FieldIncludesIdNameUrl(FieldIncludesIdName):
    url: str = Field(..., description='URL получения информации о поле')


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


class ResumeObjectsExperienceForOwner(BaseModel):
    area: FieldIncludesIdNameUrl | None = Field(None, description='Регион расположения организации. Элемент [справочника регионов](#tag/Obshie-spravochniki/operation/get-areas)')
    company: Optional[str] = Field(None, description='Название организации')
    company_id: Optional[str] = Field(None, description='Уникальный идентификатор организации')
    company_url: Optional[str] = Field(None, description='Сайт компании')
    employer: EmployersEmployerInfoShort | None = Field(None, description='Работодатель')
    end: Optional[str] = Field(None, description='Окончание работы (дата в формате `ГГГГ-ММ-ДД`)')
    industries: List[FieldIncludesIdName] = Field(..., description='Список отраслей компании. Возможные значения приведены в [справочнике индустрий](#tag/Obshie-spravochniki/operation/get-industries)')
    industry: ResumeObjectsIndustry | None = Field(None, description='Отрасль компании')
    position: str | None = Field(None, description='Должность')
    start: str = Field(..., description='Начало работы (дата в формате `ГГГГ-ММ-ДД`)')


class ProfilePhoto(BaseModel):
    field_40: Optional[str] = Field(None, alias='40')
    field_100: Optional[str] = Field(None, alias='100')
    field_500: Optional[str] = Field(None, alias='500')
    id: str = Field(..., description='Уникальный идентификатор изображения')
    medium: str = Field(..., description='URL среднего по размеру изображения. Изображение по данному url доступно ограниченное время, после получения ответа. Приложение должно быть готово к тому, что на запрос изображения вернётся `404 Not Found`\n')
    small: str = Field(..., description='URL уменьшенного изображения. Изображение по данному url доступно ограниченное время, после получения ответа. Приложение должно быть готово к тому, что на запрос изображения вернётся `404 Not Found`\n')


class ResumeObjectsSalaryProperties(BaseModel):
    amount: Optional[float] = Field(None, description='Сумма')
    currency: Optional[str] = Field(None, description='Идентификатор валюты. Возможные значения перечислены в массиве `currency` [справочника полей](#tag/Obshie-spravochniki/operation/get-dictionaries)')


class ResumeObjectsTotalExperience(BaseModel):
    months: Optional[float] = Field(None, description='Общий опыт работы в месяцах, с округлением до месяца')


class ResumeResumeShortForOwner(BaseModel):
    actions: ResumeObjectsActionsForOwner = Field(..., description='Дополнительные действия')
    age: float | None = Field(None, description='Возраст')
    alternate_url: str = Field(..., description='URL резюме на сайте')
    area: FieldIncludesIdNameUrl | None = Field(None, description='Город проживания. Элемент справочника [areas](#tag/Obshie-spravochniki/operation/get-areas)')
    auto_hide_time: FieldIncludesIdName | None = None
    can_view_full_info: bool | None = Field(None, description='Доступен ли просмотр контактной информации в резюме текущему работодателю')
    certificate: list[ResumeObjectsCertificate] = Field(..., description='Список сертификатов соискателя', min_items=0)
    created_at: str = Field(..., description='Дата и время создания резюме')
    download: ResumeObjectsDownload = Field(..., description='Ссылки для скачивания резюме в разных форматах')
    education: ResumeObjectsEducation = Field(..., description='Образование соискателя. \n\nОсобенности сохранения образования:\n\n* Если передать и высшее и среднее образование и уровень образования "средний", то сохранится только среднее образование.\n* Если передать и высшее и среднее образование и уровень образования "высшее", то сохранится только высшее образование\n')
    experience: List[ResumeObjectsExperienceForOwner] = Field(..., description='Опыт работы', min_items=0)
    first_name: Optional[str] = Field(None, description='Имя')
    gender: FieldIncludesIdName | None = Field(None, description='Пол соискателя. Возможные значения перечислены в поле `gender` [справочника полей](#tag/Obshie-spravochniki/operation/get-dictionaries)')
    hidden_fields: List[FieldIncludesIdName] = Field(..., description='Документация [Список скрытых полей](https://github.com/hhru/api/blob/master/docs/employer_resumes.md#hidden-fields). Возможные значения элементов приведены в поле `resume_hidden_fields` [справочника полей](#tag/Obshie-spravochniki/operation/get-dictionaries)', min_items=0)
    id: str = Field(..., description='Идентификатор резюме')
    last_name: Optional[str] = Field(None, description='Фамилия')
    marked: bool | None = Field(None, description='Выделено ли резюме в поиске')
    middle_name: Optional[str] = Field(None, description='Отчество')
    photo: ProfilePhoto | None = Field(None, description='Фотография пользователя')
    platform: Optional[FieldIncludesId] = Field(None, description='Ресурс, на котором было размещено резюме')
    salary: Optional[ResumeObjectsSalaryProperties] = Field(None, description='Желаемая зарплата')
    title: Optional[str] = Field(None, description='Желаемая должность')
    total_experience: Optional[ResumeObjectsTotalExperience] = Field(None, description='Общий опыт работы')
    updated_at: str = Field(..., description='Дата и время обновления резюме')
    url: str | None = Field(None, description='URL резюме на сайте')


class FieldIncludesPagination(BaseModel):
    found: float = Field(..., description='Найдено результатов', example=6)
    page: float = Field(..., description='Номер страницы', example=1)
    pages: float = Field(..., description='Всего страниц', example=2)
    per_page: float = Field(..., description='Результатов на странице', example=5)


class ResumeStatus(BaseModel):
    blocked: bool = Field(..., description='Заблокировано ли резюме ([подробнее](#tag/Rezyume.-Prosmotr-informacii/Status-rezyume))')
    can_publish_or_update: Optional[bool] = Field(None, description='Можно ли опубликовать или обновить данное резюме')
    finished: bool = Field(..., description='Заполнено ли резюме')
    status: FieldIncludesIdName = Field(..., description='[Статус резюме](#tag/Rezyume.-Prosmotr-informacii/Status-rezyume)\n')


class ResumeObjectsAccess(BaseModel):
    type: FieldIncludesIdName = Field(..., description='Определяет, кому будет доступно резюме в поиске и по прямой ссылке.\n\nУстановить значение параметра можно при [создании](#tag/Rezyume.-Sozdanie-i-obnovlenie/operation/create-resume) или [редактировании](#tag/Rezyume.-Sozdanie-i-obnovlenie/operation/edit-resume) резюме. Возможные значения приведены в поле `resume_access_type` [справочника полей](#tag/Obshie-spravochniki/operation/get-dictionaries).\n\nС 1 сентября 2021 года тип видимости `everyone` стал недоступен для сохранения из-за законодательных ограничений.\n\nЧтобы управлять списком работодателей, которые могут просматривать резюме, воспользуйтесь группой методов [Резюме. Списки видимости](#tag/Rezyume.-Spiski-vidimosti)\n')


class ResumeObjectsPaidServices(BaseModel):
    active: bool = Field(..., description='Активна ли в данный момент услуга')
    expires: Optional[str] = Field(None, description='Время окончания действия услуги, если услуга активна')
    id: str = Field(..., description='Идентификатор услуги')
    name: str = Field(..., description='Название услуги')


class ResumeApplicantFields(BaseModel):
    access: ResumeObjectsAccess
    actions: ResumeObjectsActionsForOwner = Field(..., description='Дополнительные действия')
    new_views: float = Field(..., description='Число новых просмотров. Данный счетчик сбрасывается при получении [детальной истории просмотров](#tag/Rezyume.-Prosmotr-informacii/operation/get-resume-view-history)\n')
    next_publish_at: Optional[str] = Field(None, description='Дата и время следующей возможной публикации/обновления. Для неопубликованных резюме возвращается `null`')
    paid_services: List[ResumeObjectsPaidServices] = Field(..., description='Платные услуги по резюме для автора')
    total_views: float = Field(..., description='Число просмотров резюме')
    views_url: str = Field(..., description='URL, по которому необходимо сделать GET-запрос для получения [детальной истории просмотров](#tag/Rezyume.-Prosmotr-informacii/operation/get-resume-view-history)\n')


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
    value: EmailStr | FieldIncludesContactPhoneValue | None = Field(None, description='Значение контакта. Для телефона - объект, для email - строка')
    verified: Optional[bool] = Field(None, description='Является ли телефон подтвержденным')


class FieldIncludesContact(FieldIncludesContactProperties):
    type: FieldIncludesIdName = Field(..., description='Тип контакта. Элемент справочника [preferred_contact_type](#tag/Obshie-spravochniki/operation/get-dictionaries)')
    value: EmailStr | FieldIncludesContactPhoneValue = Field(..., description='Значение контакта. Для телефона - объект, для email - строка')
    preferred: bool = Field(..., description='Является ли предпочтительным способом связи')


class ResumeObjectsCounters(BaseModel):
    total: float = Field(..., description='Количество подходящих вакансий')


class ResumeObjectsSimilarVacancies(BaseModel):
    counters: ResumeObjectsCounters
    url: str = Field(..., description='URL, по которому необходимо сделать GET-запрос, для получения [вакансий, похожих на данное резюме](#tag/Poisk-vakansij-dlya-soiskatelya/operation/get-vacancies-similar-to-resume)')


class ResumesMineItem(ResumeResumeShortForOwner, ResumeStatus, ResumeApplicantFields):
    contact: List[FieldIncludesContact] = Field(..., description='Список контактов соискателя')
    created: str = Field(..., description='Дата и время создания резюме')
    similar_vacancies: ResumeObjectsSimilarVacancies
    updated: str = Field(..., description='Дата и время обновления резюме')
    visible: bool = Field(..., description='Видно ли резюме в поиске')


class ResumesMineItems(BaseModel):
    items: List[ResumesMineItem] = Field(..., description='Список резюме текущего пользователя', min_items=0)


class ResumesMineResponse(FieldIncludesPagination, ResumesMineItems):
    pass
