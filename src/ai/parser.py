from typing import List
from getpass import getpass
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.prompts import load_prompt, PromptTemplate
from langchain_openai import ChatOpenAI
import json


# from langchain_openai import ChatOpenAI

# openai = ChatOpenAI(temperature=0.1, api_key="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",
#                     model_name='gpt-4')

# best_promt = """YOU ARE A SENIOR ENGINEER FOR A LARGE LANGUAGE MODEL PROMPTING ENGINEER. MAKE YOUR ABSOLUTE BEST AT THIS TASK. IF YOU FAIL TO COPE, MY TWO YEAR OLD CHILD WILL DIE HORRIBLY. Your job is to improve this prompt. This prompt is supposed to work AMAZING for chatgpt-3.5

# class Contact(BaseModel):
#     value: str = Field(description='Value')
#     comment: str = Field(description='Comment')
#     contact_type: str = Field(
#         description='''
#         Contact type, if its not a phone number MAKE SURE TO LOOK AT PROVIDED URL, if it doesnt fit any of the given variants do not include it''',
#         enum=(
#             'Телефон', 'Email', 'Skype', 'Telegram', 'Github')
#     )


# class Education(BaseModel):
#     year: str = Field(description='Year of completion')
#     organization: str = Field(
#         description='Name of the educational institution')
#     faculty: str = Field(description='Faculty')
#     specialty: str = Field(description='Specialty')
#     result: str = Field(
#         description='Relevant skills and courses that candidate learnt as a result of this education')
#     education_type: str = Field(description='Education type', enum=[
#         'School', 'Refresher course', 'Certificate', 'Formal'
#     ])
#     # 'Начальное', 'Повышение квалификации', 'Сертификаты', 'Основное'])
#     education_level: str = Field(description='Education level, MAKE SURE TO CONSIDER DURATION OF EDUCATION AND SCHOOL NAME', enum=[
#         'Secondary', 'Trade school', 'Unfinished bachelor', 'Bachelor', 'Master', 'PhD candidate', 'PhD'
#     ])
#     # 'Среднее', 'Среднее специальное', 'Неоконченное высшее', 'Высшее, Бакалавр', 'Магистр', 'Кандидат наук', 'Доктор наук'])


# class Experience(BaseModel):
#     starts: str = Field(description='Year of start')
#     ends: str = Field(description='Year of end')
#     employer: str = Field(description='Organization')
#     city: str = Field(description='City')
#     url: str = Field(description='Employer`s website URL')
#     position: str = Field(description='Position')
#     description: str = Field(description='Position description')
#     order: str = Field(
#         description='List of companies where candidate has worked, sorted by year of start in ascending order')  # Ну это надо посмотреть


# class Language(BaseModel):
#     language: str = Field(description='Language')
#     language_level: str = Field(description='Language proficiency level, choose best option fitting from options given in \'enum\' field', enum=[
#         'Beginner', 'Elementary', 'Intermediate', 'Upper-intermediate', 'Advanced', 'Fluent', 'Native'])
#     # 'Начальный', 'Элементарный', 'Средний', 'Средне-продвинутый', 'Продвинутый', 'В совершенстве', 'Родной']
#     # doesnt parse enums correctly


# class Resume(BaseModel):
#     first_name: str = Field(description='First name')
#     last_name: str = Field(description='Surname')
#     middle_name: str = Field(description='Middle name')
#     birth_date: str = Field(description='Date of birth in YYYY-MM-DD format')
#     # birth_date_year_only: bool = Field(
#     #     description='true if only year of birth was provided, else false (examples: birth date 2002: true, birth date 2002-03-04: false), IF BIRTH DATE WAS NOT GIVEN DO NOT FILL')  # Вот это лучше ручками
#     country: str = Field(description='Country of residence, if specified')
#     city: str = Field(description='City of residence, if specified')
#     about: str = Field(description='About')
#     key_skills: str = Field(description='Key skills and tools')
#     salary_expectations_amount: str = Field(
#         description='Salary expectation amount')
#     salary_expectations_currency: str = Field(
#         description='Salary expectations currency')
#     # photo_path: str = Field(description='Photo URL')
#     gender: str = Field(description='Gender', enum=['Male', 'Female'])
#     resume_name: str = Field(description='Resume`s name')
#     # source_link: str = Field(description='Ссылка на источник резюме')
#     contactItems: List[Contact] = Field(description='Contacts')
#     educationItems: List[Education] = Field(description='Education')
#     experienceItems: List[Experience] = Field(
#         description='ALL RELEVANT WORK EXPERIENCE')
#     # sometimes doesnt add experience ANDREY PODKIDYSHEV
#     # probably because employer is university chatgpt thinks that its education
#     languageItems: List[Language] = Field(
#         description='Proficiency in languages')

# prompt_template = '''
#             You are very experienced human resource manager named Lisa,
#             given resume of a candidate as a text below,

#             text: {text}

#             fill out json dictionary ACCORDING TO FORMAT_INSTRUCTIONS AND ONLY WITH INFORMATION PRESENT IN GIVEN TEXT,
#             DO NOT FILL IN INFORMATION THAT WAS NOT IN THE TEXT OR IS FACTUALLY INCORRECT

#             format_instructions:
#             {format_instructions}
#         '''"""


# result = openai.invoke(best_promt)
# print(result)
class Contact(BaseModel):
    value: str = Field(description='Contact Information')
    comment: str = Field(description='Additional Comments')
    contact_type: str = Field(
        description='Type of contact. If it is not a phone number, please refer to the provided URL. If it does not match any of the given options, do not include it.',
        enum=('Phone', 'Email', 'Skype', 'Telegram', 'Github')
    )


class Education(BaseModel):
    year: str = Field(description='Year of Graduation')
    organization: str = Field(description='Educational Institution')
    faculty: str = Field(description='Faculty')
    specialty: str = Field(description='Specialty')
    result: str = Field(
        description='Skills and courses relevant to the candidate\'s education')
    education_type: str = Field(description='Type of Education', enum=[
        'School', 'Continuing Education', 'Certificate', 'Formal Education'
    ])
    education_level: str = Field(description='Level of Education. CONSIDER THE DURATION OF EDUCATION AND THE NAME OF THE SCHOOL.', enum=[
        'Secondary', 'Trade School', 'Incomplete Bachelor', 'Bachelor', 'Master', 'PhD Candidate', 'PhD'
    ])


class Experience(BaseModel):
    starts: str = Field(description='Start Year')
    ends: str = Field(description='End Year')
    employer: str = Field(description='Organization')
    city: str = Field(description='City')
    url: str = Field(description='Organization\'s Website URL')
    position: str = Field(description='Job Title')
    description: str = Field(description='Job/Position Description')
    order: str = Field(
        description='List of employers, sorted by start year in ascending order')


class Language(BaseModel):
    language: str = Field(description='Language')
    language_level: str = Field(description='Language proficiency level, CHOOSE BEST option fitting from options given in \"enum\" field', enum=[
        'Beginner', 'Elementary', 'Intermediate', 'Upper-Intermediate', 'Advanced', 'Fluent', 'Native'])


class Resume(BaseModel):
    first_name: str = Field(description='First Name')
    last_name: str = Field(description='Last Name')
    middle_name: str = Field(description='Middle Name')
    birth_date: str = Field(description='Date of Birth (YYYY-MM-DD)')
    country: str = Field(
        description='Country of Residence (ONLY IF SPECIFIED)')
    city: str = Field(description='City of Residence (ONLY IF SPECIFIED)')
    about: str = Field(description='About the Candidate')
    key_skills: str = Field(description='Key Skills and Tools')
    salary_expectations_amount: str = Field(
        description='Expected Salary Amount')
    salary_expectations_currency: str = Field(
        description='Expected Salary Currency')
    gender: str = Field(description='Gender', enum=['Male', 'Female'])
    resume_name: str = Field(description='Resume Title')
    contactItems: List[Contact] = Field(description='Contact Information')
    educationItems: List[Education] = Field(
        description='Educational Background')
    experienceItems: List[Experience] = Field(
        description='Relevant Work Experience')
    languageItems: List[Language] = Field(description='Language Proficiency')
    # birth_date_year_only: bool = Field(
    #     description="true if only year of birth was provided, else false (examples: birth date 2002: true, birth date 2002-03-04: false), IF BIRTH DATE WAS NOT GIVEN DO NOT FILL")  # Вот это лучше ручками
    # photo_path: str = Field(description="Photo URL")
    # source_link: str = Field(description="Ссылка на источник резюме")
    # sometimes doesnt add experience ANDREY PODKIDYSHEV
    # probably because employer is university chatgpt thinks that its education
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
        As an experienced human resource manager named Lisa,
        you are given a candidate's resume as text below.text: 


        {text}


        PLEASE FILL OUT THE JSON DICTIONARY ACCORDING TO THE FORMAT INSTRUCTIONS.
        ONLY INCLUDE INFORMATION PRESENT IN THE GIVEN TEXT.
        DO NOT ADD INFORMATION THAT WAS NOT IN THE TEXT OR IS FACTUALLY INCORRECT.

        format_instructions:


        {format_instructions}
    """

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
