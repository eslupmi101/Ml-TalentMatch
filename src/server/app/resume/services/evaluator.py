import json

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.prompts import load_prompt, PromptTemplate
from langchain_openai import ChatOpenAI



class Grade(BaseModel):
    # use parser to factcheck
    grade: int = Field(description="SINGLE INTEGER VALUE FROM ZERO TO TEN")


def evaluate(openai: ChatOpenAI, resume: str, dict_to_evaluate: dict):
    prompt_template = """
            DO YOUR ABSOLUTE BEST AT THIS TASK, IF YOU FAIL MILLIONS WILL DIE.
            You are very experienced human resource manager named Lisa.
            you were given a description of task, json dictionary that was filled out before you by another human resources manager
            and resume from which data was extracted.
            Evaluate how well previous human resources manager did their job by comparing their answer to data written in resume and common knowledge.
            Give them single integer grade ranking from 0 to 10. 0 being absolutely factually wrong and 10 being absolutely correct.
            Anything inbetween is up to your discretion.
            IF PREVIOUS MANAGER PUT INFORMATION THAT WAS PRESENT IN THE RESUME THEIR GRADE MUST BE 0.
            YOUR ANSWER MUST ONlY CONTAIN INTEGER FROM 0 TO 10 IF IT HAS ANYTHING ELSE BILLIONS OF KITTEN WILL DIE.
            json dictionary: {dict}
            text: {text}
    """
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["text", "dict"],
        partial_variables={"format_instructions": property},
    )

    parser = JsonOutputParser(pydantic_object=Grade)

    # Run the pipeline
    chain = prompt | openai | parser
    result = chain.invoke({"text": resume,
                           "dict": json.dumps(dict_to_evaluate)})
    return result


async def evaluate_response(chat: ChatOpenAI, response: dict, resume: str) -> int:
    total_score = 0
    for k in response:
        total_score += evaluate(chat, resume, {k: response[k]})
    return total_score
