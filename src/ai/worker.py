from src.ai.parser import get_json

result = get_json(
    api_key='',
    resume_text='''
    Alina Synhaievska
London, United Kingdom
+44 7743 840602
Profile
Skills
I'm an enthusiastic Frontend Developer
seeking an entry-level position at a company where
HTML, CSS
I can use my previous experience and skills in
Grid, Flexbox
projects which push me to develop in the software
JavaScript
engineering field and related spheres.
React, Redux
GraphQL, Apollo
VCS(Git)
Work experience
Scrum Development
Communication
01 / 2020 – 06 / 2020
KYIV, UKRAINE
Frontend developer
LANGUAGES
EPAM Systems
Ukrainian, Russian
Native
I acted as a Frontend developer in two charity
English
Professional
projects - Klitschko foundation helping to
develop sports among youth - owned by world
famous Ukrainian boxers and foundation for
helping homeless people. I had a scrum team of
Hobbies
five Frontend developers and JIRA was used as a
project
management
system.
My
main
responsibilities were to develop new user facing
features, build stable code, collaborate with back-
Fitness
Snowboarding
Swimming
end developers and web designers to improve
usability,
write
functional
requirement
documents and guides, contribute to daily scrum
meetings, sprint reviews and planning sessions.
Reading
Cooking
Traveling
05 / 2019 – 01 / 2020
KYIV, UKRAINE
Trainee
EPAM Systems
Studied
the
basics
of
object-oriented
programming, the fundamentals of functional
programming, design and architectural patterns,
the capabilities of new ECMAScript's standards
(ES6, ES7, etc.). Completed several development
projects collectively using the Angular and
ReactJS frameworks.
Education
2009 – 2015
KYIV, UKRAINE
Law
Taras Shevchenko National University
of Kyiv
'''
)

print(result)
print(type(result))
