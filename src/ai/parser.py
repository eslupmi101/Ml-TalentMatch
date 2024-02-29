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
                        model_name="gpt-4-turbo-preview")

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


def fix_language(api_key: str, response: dict):
    openai = ChatOpenAI(temperature=0.0, api_key=api_key,
                        model_name="gpt-4-turbo-preview")
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

