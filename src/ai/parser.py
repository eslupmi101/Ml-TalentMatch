from typing import List
from getpass import getpass
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.prompts import load_prompt, PromptTemplate
from langchain_openai import ChatOpenAI
import json
from src.ai.evaluator import evaluate

class Contact(BaseModel):
    # use parser to factcheck
    value: str = Field(description="Value")
    comment: str = Field(description="Comment")
    contact_type: str = Field(
        description="""
        Contact type, if its not a phone number MAKE SURE TO LOOK AT PROVIDED URL, if it doesnt fit any of the given variants do not include it""",
        enum=(
            "Телефон", "Email", "Skype", "Telegram", "Github")
    )


class Education(BaseModel):
    # may be use another prompt to factcheck
    year: str = Field(description="Year of completion")
    organization: str = Field(description="Name of the educational institution")
    faculty: str = Field(description="Faculty")
    specialty: str = Field(description="Specialty")
    result: str = Field(description="Relevant skills and courses that candidate learnt as a result of this education")
    education_type: str = Field(description="Education type", enum=[
        'School', 'Refresher course', 'Certificate', 'Formal'
    ])
    # "Начальное", "Повышение квалификации", "Сертификаты", "Основное"])
    education_level: str = Field(description="Education level, MAKE SURE TO CONSIDER DURATION OF EDUCATION AND SCHOOL NAME", enum=[
        'Secondary', 'Trade school', 'Unfinished bachelor', 'Bachelor', 'Master', 'PhD candidate', 'PhD'
    ])
    # "Среднее", "Среднее специальное", "Неоконченное высшее", "Высшее, Бакалавр", "Магистр", "Кандидат наук", "Доктор наук"])


class Experience(BaseModel):
    # may be use another prompt to factcheck
    starts: str = Field(description="Date of start in format YYYY-MM-DD")
    ends: str = Field(description="Date of end in format YYYY-MM-DD")
    employer: str = Field(description="Organization")
    city: str = Field(description="City")
    # maybe use agent?
    url: str = Field(description="Employer`s website URL")
    position: str = Field(description="Position")
    description: str = Field(description="Position description")
    # better to sort by
    # order: str = Field(
    #     description="List of companies where candidate has worked, sorted by year of start in ASCENDING ORDER")  # Ну это надо посмотреть


class Language(BaseModel):
    # check by parser
    language: str = Field(description="Language")
    # check by parser
    language_level: str = Field(description="Language proficiency level, choose best option fitting from options given in field", enum=[
        "Beginner", "Elementary", "Intermediate", "Upper-intermediate", "Advanced", "Fluent", "Native"])
        # "Начальный", "Элементарный", "Средний", "Средне-продвинутый", "Продвинутый", "В совершенстве", "Родной"]
    # doesnt parse enums correctly


class Resume(BaseModel):
    # separate parser to check location, name and birth date, key_skills, amount of salary expectation
    first_name: str = Field(description="First name")
    last_name: str = Field(description="Surname")
    middle_name: str = Field(description="Middle name")
    birth_date: str = Field(description="Date of birth in YYYY-MM-DD format, if only year was given use YYYY format")
    # this should be done by parsing birth_date
    # birth_date_year_only: bool = Field(
    #     description="true if only year of birth was provided, else false (examples: birth date 2002: true, birth date 2002-03-04: false), IF BIRTH DATE WAS NOT GIVEN DO NOT FILL")
    country: str = Field(description="Country where the candidate is located")
    city: str = Field(description="City where the candidate is located")
    about: str = Field(description="about")
    key_skills: str = Field(description="Key skills and tools")
    salary_expectations_amount: str = Field(description="Salary expectation amount")
    salary_expectations_currency: str = Field(
        description="Salary expectations currency")
    # separate parser
    # photo_path: str = Field(description="Photo URL")
    # should this even be here?
    gender: str = Field(description="Gender", enum=['Male', 'Female'])
    # separate parser
    # resume_name: str = Field(description="Resume`s name")
    # backend
    # source_link: str = Field(description="Ссылка на источник резюме")
    # check links
    contact: List[Contact] = Field(description="Contacts")
    education: List[Education] = Field(description="Education")
    experience: List[Experience] = Field(description="ALL RELEVANT WORK EXPERIENCE")
    # sometimes doesnt add experience ANDREY PODKIDYSHEV
    # probably because employer is university chatgpt thinks that its education
    language: List[Language] = Field(
        description="Proficiency in languages")


    # Update prompt template to include a variable placeholder for the result



def get_json(resume_text: str, api_key: str) -> dict:
    # Initialize ChatOpenAI instance
    openai = ChatOpenAI(temperature=0.0, api_key=api_key,
                        model_name="gpt-4-turbo")

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


def fix_language(api_key: str, response: dict):
    openai = ChatOpenAI(temperature=0.0, api_key=api_key,
                        model_name="gpt-4-turbo")
    language_items = response['language']
    result = []
    # Initialize JsonOutputParser
    for l in language_items:
        parser = JsonOutputParser(pydantic_object=Language)

        instructions = parser.get_format_instructions()
        decoded_instructions = bytes(
            instructions, "utf-8").decode("unicode_escape")
        prompt_template = """
            YOU ARE A POLYGLOT AND EXPERT IN LANGUAGES, 
            THOUSANDS PEOPLES LIFE DEPENDS ON THIS, DO YOUR ABSOLUTE BEST to replace language proficiency levels in the json object below to the best fitting level from specified:
            "Beginner", "Elementary", "Intermediate", "Upper-intermediate", "Advanced", "Fluent", "Native"
            {text}
            PROVIDE ANSWER IN JSON FORMAT
        """
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["text"],
            partial_variables={"format_instructions": decoded_instructions},
        )

        # Run the pipeline
        chain = prompt | openai | parser
        fixed_language = chain.invoke({"text": json.dumps(l)})
        result.append(fixed_language)
    return result


def evaluate_response(chat: ChatOpenAI, response: dict, resume: str) -> int:
    total_score = 0
    for k in response:
        total_score += evaluate(chat, resume, {k: response[k]})
    return total_score

