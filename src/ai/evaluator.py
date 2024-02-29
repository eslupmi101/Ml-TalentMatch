from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.prompts import load_prompt, PromptTemplate
from langchain_openai import ChatOpenAI
import json



class Grade(BaseModel):
    # use parser to factcheck
    grade: int = Field(description="SINGLE INTEGER VALUE FROM ZERO TO TEN")

def evaluate(api_key: str, resume: str, dict_to_evaluate: dict):
    openai = ChatOpenAI(temperature=0.0, api_key=api_key,
                        model_name="gpt-4")
    result = []
    prompt_template = """
            DO YOUR ABSOLUTE BEST AT THIS TASK, IF YOU FAIL MILLIONS WILL DIE.
            You are very experienced human resource manager named Lisa.
            you were given a description of task, json dictionary that was filled out before you by another human resources manager
            and resume from which data was extracted.
            Evaluate how well previous human resources manager did their job by comparing their answer to data written in resume and common knowledge.
            Give them single integer grade ranking from 0 to 10. 0 being absolutely factually wrong and 10 being absolutely correct.
            IF PREVIOUS MANAGER PUT INFORMATION THAT WAS PRESENT IN THE RESUME THEIR GRADE MUST BE 0.
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

if __name__ == "__main__":
    to_eval = json.loads("""
    {
       "first_name":"Alina",
       "last_name":"Manafli",
       "middle_name":"",
       "birth_date":"",
       "country":"",
       "city":"",
       "about":"",
       "key_skills":"Java, JavaScript, C, C++, OpenCL, CUDA, OpenMP, OpenGL, React, Spring, Git",
       "salary_expectations_amount":"",
       "salary_expectations_currency":"",
       "gender":"",
       "contact":[
          {
             "value":"+46 764 595 000",
             "comment":"",
             "contact_type":"Телефон"
          },
          {
             "value":"aaaaaamanafli@gmail.com",
             "comment":"",
             "contact_type":"Email"
          }
       ],
       "education":[
          {
             "year":"2021",
             "organization":"Tallinn University of Technology",
             "faculty":"Computer and Systems Engineering",
             "specialty":"",
             "result":"Computer Systems Engineering, Object Oriented Programming",
             "education_type":"Formal",
             "education_level":"Master"
          },
          {
             "year":"2021",
             "organization":"Uppsala University",
             "faculty":"Computer Science",
             "specialty":"",
             "result":"Software Engineering and Project Management, Advanced Computer Architecture, Computer Graphics, Low-Level Parallel Programming, Parallel Programming for EPciency, Computer Networks, Agile and Extreme Project Management",
             "education_type":"Formal",
             "education_level":"Master"
          },
          {
             "year":"2019",
             "organization":"Lomonosov Moscow State University",
             "faculty":"Applied Mathematics",
             "specialty":"",
             "result":"Programming in C/C++, Discrete Mathematics, Parallel Programming, Linear Algebra, Calculus, Mathematical Statistics, Methods of Optimisation, Numerical Methods",
             "education_type":"Formal",
             "education_level":"Bachelor"
          },
          {
             "year":"2017",
             "organization":"Peter the Great St.Petersburg Polytechnic University",
             "faculty":"Microelectronic Devices Programming",
             "specialty":"",
             "result":"",
             "education_type":"Summer School",
             "education_level":""
          }
       ],
       "experience":[
          {
             "starts":"2020",
             "ends":"2020",
             "employer":"Kuehne + Nagel",
             "city":"Tallinn, Estonia",
             "url":"",
             "position":"IT Trainee",
             "description":"Designing and developing an open source fullstack application for Supply Chain Management of a fictional business.",
             "order":"1"
          },
          {
             "starts":"2020",
             "ends":"2020",
             "employer":"Uppsala University",
             "city":"Uppsala, Sweden",
             "url":"",
             "position":"Teaching Assistant",
             "description":"Assisting in teaching of the Software Engineering and Project Management course by leading the project work of four groups of students in the role of a Scrum coach and the project’s client.",
             "order":"2"
          },
          {
             "starts":"2018",
             "ends":"2018",
             "employer":"CERN",
             "city":"Geneva, Switzerland",
             "url":"",
             "position":"Openlab Summer Intern",
             "description":"Tested and optimized a set of common Question Answering NLP models on The Stanford Question Answering Dataset using Tensorflow.",
             "order":"3"
          },
          {
             "starts":"2017",
             "ends":"2017",
             "employer":"R.I.S.K. Company",
             "city":"Baku, Azerbaijan",
             "url":"",
             "position":"Software Engineer Intern",
             "description":"Programmed a voice recorder with Arduino by applying Digital Signal Processing methods.",
             "order":"4"
          }
       ],
       "language":[
          {
             "language":"English",
             "language_level":"Fluent"
          },
          {
             "language":"Russian",
             "language_level":"Native"
          },
          {
             "language":"Azerbaijani",
             "language_level":"Native"
          }
       ]
    }""")

    resume = """
             ![](alina_manafli.001.png)
    
    **Evaluation Only. Created with Aspose.Words. Copyright 2003-2024 Aspose Pty Ltd.**
    
    **Alina** +46 764 595 000 ![](alina_manafli.002.png)![](alina_manafli.003.png)**MANAFLI ![](alina_manafli.004.png)[ aaaaaamanafli@gmail.com ](mailto:aaaaaamanafli@gmail.com)**
    
    **EDUCATION**
    
    9/2019 – 6/2021 **Tallinn University of Technology** 
    
    Expected  *MSc Computer and Systems Engineering, GPA 4.4/5.O* 
    
    Computer Systems Engineering, Object Oriented Programming 
    
    1/2020 - 1/2021  **Uppsala University** 
    
    Expected  *NORDTEK Exchange Studies, Computer Science, GPA 5.O/5.O* 
    
    Software Engineering and Project Management, Advanced Computer Architecture, Computer Graphics, Low-Level Parallel Programming, Parallel Programming for EPciency, Computer Networks, Agile and Extreme Project Management 
    
    9/2015 - 6/2019  **Lomonosov Moscow State University** 
    
    *BSc Applied Mathematics, GPA 5.O/5.O* 
    
    Programming in C/C++, Discrete Mathematics, Parallel Programming, Linear Algebra, Calculus, Math- ematical Statistics, Methods of Optimisation, Numerical Methods 
    
    7/2017 - 8/2017  **Peter the Great St.Petersburg Polytechnic University** 
    
    *Summer School in Microelectronic Devices Programming* 
    
    ` `**EXPERIENCE**  
    
    8/2020 - 11/2020 **Kuehne + Nagel  Tallinn, Estonia (remote)** Ongoing *IT Trainee* 
    
    Designing and developing an open source fullstack application for Supply Chain Management of a fictional business. 
    
    React  /  Spring  /   HTML  /   CSS  /   Jira 
    
    8/2020 - 11/2020 **Uppsala University  Uppsala, Sweden** Ongoing *Teaching Assistant* 
    
    Assisting in teaching of the Software Engineering and Project Management course by leading the project work of four groups of students in the role of a Scrum coach and the project’s client. 
    
    Agile  /  Scrum  /   Kanban 
    
    7/2018 – 9/2018  **CERN  Geneva, Switzerland** 
    
    *Openlab Summer Intern* 
    
    Tested and optimized a set of common Question Answering NLP models on The Stanford Question Answering Dataset using Tensorflow . 
    
    Python  /  NLP  /   Tensorflow  /   CUDA 
    
    5/2017 - 7/2017  **R.I.S.K. Company  Baku, Azerbaijan** 
    
    *Software Engineer Intern* 
    
    Programmed a voice recorder with Arduino by applying Digital Signal Processing methods. Arduino  /  C  /   DSP 
    
    ` `**PROJECTS**  
    
    August 2020  **Conway’s Game of Life Visualizer [|    Github  ](https://github.com/AmiManafli/SpringReactGameOfLife)![ref1]**
    
    Built a fullstack application in React and Spring to visualize the evolution of alive and dead cells on a grid by the rules described by John Conway. 
    
    Java  /  Spring  /   React  /   HTML  /   CSS 
    
    July 2020  **Music Advisor [|    Github  ](https://github.com/AmiManafli/JBMusicAdvisor)![ref1]**
    
    Created a personal music advisor that makes preference-based suggestions and provides links to new releases and featured playlists through Spotify API. 
    
    Java  /  Spotify API  /   OAuth 
    
    May 2020  **Space Simulator** | [   Youtube  ](https://youtu.be/IaEwY0Ksi28)![](alina_manafli.006.png)
    
    Designed and built a C++ application with OpenGL able to procedurally generate and render a large number of solar systems, allowing the user to move in the created space. Parallelized with OpenMP. 
    
    C++  /  OpenGL  /  GLSL  /  OpenMP 
    
    **SKILLS**
    
    **Programming Languages:**  Java, JavaScript, C, C++
    
    **Parallel Programming / GPU:**  OpenCL, CUDA, OpenMP, OpenGL 
    
    **Web:**  React, Spring
    
    **Version Control:**  Git 
    
    **Languages:**  English (fluent), Russian (native), Azerbaijani (native)
    
    ` `**CERTIFICATES AND AWARDS**  
    
    Aug 2020  Google Get Ahead Program 
    
    - *Participated in a 8 week virtual program for selected CS students from all over EMEA* 
    - *The program involved technical challenges, YouTube live training and interview workshops* 
    
    Jan 2020  Nordplus grant for NORDTEK exchange studies recipient 
    
    Jan 2020  Kristjan Jaak Study Periods Abroad Scholarship recipient 
    
    Sep 2019  Dora Pluss Scholarship recipient 
    
    Dec 2018  Representative of Applied Mathematics Faculty at the Second National Student Conference Nov 2017  Participant of ACM ICPC Subregional Programming contest 
    
    Jul 2017  Intel FPGA Technical Training, Peter the Great St. Petersburg 
    
    Oct 2016  Participant of ACM ICPC Subregional Programming contest 
    
    Sep 2016  Media Team Volunteer at 42nd Chess Olympiad 
    
    Apr 2016  Participant of the All-Republican Olympiad in Information Science 
    **Created with an evaluation copy of Aspose.Words. To discover the full versions of our APIs please visit: https://products.aspose.com/words/**
    
    [ref1]: alina_manafli.005.png
    
             """

    to_eval = to_eval['experience']
    result = evaluate('api_key',
             resume,
             to_eval)
    print(result)
