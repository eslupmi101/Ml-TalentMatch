from typing import List
from getpass import getpass
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.prompts import load_prompt, PromptTemplate
from langchain_openai import ChatOpenAI
import json


class Contact(BaseModel):
    value: str = Field(description="Value")
    comment: str = Field(description="Comment")
    contact_type: str = Field(
        description="""
        Contact type, if its not a phone number MAKE SURE TO LOOK AT PROVIDED URL, if it doesnt fit any of the given variants do not include it""",
        enum=(
            "Телефон", "Email", "Skype", "Telegram", "Github")
    )


class Education(BaseModel):
    year: str = Field(description="Year of completion")
    organization: str = Field(
        description="Name of the educational institution")
    faculty: str = Field(description="Faculty")
    specialty: str = Field(description="Specialty")
    result: str = Field(
        description="Relevant skills and courses that candidate learnt as a result of this education")
    education_type: str = Field(description="Education type", enum=[
        'School', 'Refresher course', 'Certificate', 'Formal'
    ])
    # "Начальное", "Повышение квалификации", "Сертификаты", "Основное"])
    education_level: str = Field(description="Education level, MAKE SURE TO CONSIDER DURATION OF EDUCATION AND SCHOOL NAME", enum=[
        'Secondary', 'Trade school', 'Unfinished bachelor', 'Bachelor', 'Master', 'PhD candidate', 'PhD'
    ])
    # "Среднее", "Среднее специальное", "Неоконченное высшее", "Высшее, Бакалавр", "Магистр", "Кандидат наук", "Доктор наук"])


class Experience(BaseModel):
    starts: str = Field(description="Year of start")
    ends: str = Field(description="Year of end")
    employer: str = Field(description="Organization")
    city: str = Field(description="City")
    url: str = Field(description="Employer`s website URL")
    position: str = Field(description="Position")
    description: str = Field(description="Position description")
    order: str = Field(
        description="List of companies where candidate has worked, sorted by year of start in ascending order")  # Ну это надо посмотреть


class Language(BaseModel):
    language: str = Field(description="Language")
    language_level: str = Field(description="Language proficiency level, choose best option fitting from options given in \"enum\" field", enum=[
        "Beginner", "Elementary", "Intermediate", "Upper-intermediate", "Advanced", "Fluent", "Native"])
    # "Начальный", "Элементарный", "Средний", "Средне-продвинутый", "Продвинутый", "В совершенстве", "Родной"]
    # doesnt parse enums correctly


class Resume(BaseModel):
    first_name: str = Field(description="First name")
    last_name: str = Field(description="Surname")
    middle_name: str = Field(description="Middle name")
    birth_date: str = Field(description="Date of birth in YYYY-MM-DD format")
    # birth_date_year_only: bool = Field(
    #     description="true if only year of birth was provided, else false (examples: birth date 2002: true, birth date 2002-03-04: false), IF BIRTH DATE WAS NOT GIVEN DO NOT FILL")  # Вот это лучше ручками
    country: str = Field(description="Country")
    city: str = Field(description="City")
    about: str = Field(description="about")
    key_skills: str = Field(description="Key skills and tools")
    salary_expectations_amount: str = Field(
        description="Salary expectation amount")
    salary_expectations_currency: str = Field(
        description="Salary expectations currency")
    photo_path: str = Field(description="Photo URL")
    gender: str = Field(description="Gender", enum=['Male', 'Female'])
    resume_name: str = Field(description="Resume`s name")
    # source_link: str = Field(description="Ссылка на источник резюме")
    contact: List[Contact] = Field(description="Contacts")
    education: List[Education] = Field(description="Education")
    experience: List[Experience] = Field(
        description="ALL RELEVANT WORK EXPERIENCE")
    # sometimes doesnt add experience ANDREY PODKIDYSHEV
    # probably because employer is university chatgpt thinks that its education
    language: List[Language] = Field(
        description="Proficiency in languages")

    # Update prompt template to include a variable placeholder for the result


def get_json(resume_text: str, api_key: str) -> dict:
    # Initialize ChatOpenAI instance

    openai = ChatOpenAI(temperature=0.0, api_key=api_key,
                        model_name="gpt-3.5-turbo")

    # Initialize JsonOutputParser
    parser = JsonOutputParser(pydantic_object=Resume)

    # Get format instructions
    instructions = parser.get_format_instructions()
    decoded_instructions = bytes(
        instructions, "utf-8").decode("unicode_escape")

    prompt_template = """
            You are very experienced human resource manager named Lisa, 
            given resume of a candidate as a text below, 

            text: {text}
            
            fill out json dictionary ACCORDING TO FORMAT_INSTRUCTIONS AND ONLY WITH INFORMATION PRESENT IN GIVEN TEXT, 
            DO NOT FILL IN INFORMATION THAT WAS NOT IN THE TEXT OR IS FACTUALLY INCORRECT
            
            format_instructions:
            {format_instructions}
        """
    # print(decoded_instructions)
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
