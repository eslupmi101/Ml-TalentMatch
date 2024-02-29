import aspose.words as aw

doc = aw.Document("/Users/koluj/Documents/GitHub/Ml-TalentMatch/src/ai/resumes/Alina   MANAFLI.pdf")
# print(doc.to_string())
doc.save("alina_manafli.md")
