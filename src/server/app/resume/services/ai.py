from typing import List
from getpass import getpass
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.prompts import load_prompt, PromptTemplate
from langchain_openai import ChatOpenAI


class Contact(BaseModel):
    value: str = Field(description="Значение")
    comment: str = Field(description="Комментарий")
    contact_type: str = Field(description="Тип контакта", enum=(
        "Телефон", "Email", "Skype", "Telegram", "Github"))


class Education(BaseModel):
    year: str = Field(description="Год окончания")
    organization: str = Field(description="Название учебного заведения")
    faculty: str = Field(description="Факультет")
    specialty: str = Field(description="Специальность")
    result: str = Field(description="Результат обучения")
    education_type: str = Field(description="Тип образования", enum=[
                                "Начальное", "Повышение квалификации", "Сертификаты", "Основное"])
    education_level: str = Field(description="Уровень образования", enum=[
                                 "Среднее", "Среднее специальное", "Неоконченное высшее", "Высшее, Бакалавр", "Магистр", "Кандидат наук", "Доктор наук"])


class Experience(BaseModel):
    starts: str = Field(description="Год начала")
    ends: str = Field(description="Год окончания")
    employer: str = Field(description="Организация")
    city: str = Field(description="Город")
    url: str = Field(description="Ссылка на сайт работодателя")
    position: str = Field(description="Должность")
    description: str = Field(description="Описание")
    order: str = Field(
        description="Порядок следования в массиве опыта работы (для сортировки)")  # Ну это надо посмотреть


class Language(BaseModel):
    language: str = Field(description="Язык")
    language_level: str = Field(description="Уровень владения языком", enum=[
                                "Начальный", "Элементарный", "Средний", "Средне-продвинутый", "Продвинутый", "В совершенстве", "Родной"])


class Resume(BaseModel):
    first_name: str = Field(description="Имя")
    last_name: str = Field(description="Фамилия")
    middle_name: str = Field(description="Отчество")
    birth_date: str = Field(description="Дата рождения в формате YYYY-MM-DD")
    birth_date_year_only: bool = Field(
        description="Если true, дата рождения вычисляется из возраста (Например, возраст 20 -> 2004-01-01)")  # Вот это лучше ручками
    country: str = Field(description="Страна")
    city: str = Field(description="Город")
    about: str = Field(description="Описание")
    key_skills: str = Field(description="Ключевые навыки")
    salary_expectations_amount: str = Field(description="Зарплатные ожидания")
    salary_expectations_currency: str = Field(
        description="Валюта зарплатных ожиданий")
    photo_path: str = Field(description="Ссылка на фото")
    gender: str = Field(description="Пол", enum=['Мужской', 'Женский'])
    resume_name: str = Field(description="Название резюме")
    source_link: str = Field(description="Ссылка на источник резюме")
    contactItems: List[Contact] = Field(description="Контактные данные")
    educationItems: List[Education] = Field(description="Образование")
    experienceItems: List[Experience] = Field(description="Опыт работы")
    languageItems: List[Language] = Field(
        description="Владение иностранными языками")


# Update prompt template to include a variable placeholder for the result
prompt_template = """Из следующего текста извлеки информацию:

    text: {text}

    Заполняй json таблицу только информацией содержащей в тексте выше, при ее отсутствии не заполняй поле.

    format_instructions:
    {format_instructions}
"""


async def get_result(resume_text: str, api_key: str) -> dict:
    # Initialize ChatOpenAI instance
    openai = ChatOpenAI(temperature=0.0, api_key=api_key,
                        model_name="gpt-3.5-turbo")

    # Initialize JsonOutputParser
    parser = JsonOutputParser(pydantic_object=Resume)

    # Get format instructions
    instructions = parser.get_format_instructions()
    decoded_instructions = bytes(
        instructions, "utf-8").decode("unicode_escape")

    # Prepare prompt
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["text"],
        partial_variables={"format_instructions": decoded_instructions},
    )

    # Run the pipeline
    chain = prompt | openai | parser
    result = chain.invoke({"text": resume_text})

    return result
