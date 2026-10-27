# import os
# from langchain_groq import ChatGroq
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import JsonOutputParser
# from langchain_core.exceptions import OutputParserException
# from dotenv import load_dotenv

# load_dotenv()

# class Chain:
#     def __init__(self):
#         self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")

#     def extract_jobs(self, cleaned_text):
#         prompt_extract = PromptTemplate.from_template(
#             """
#             ### SCRAPED TEXT FROM WEBSITE:
#             {page_data}
#             ### INSTRUCTION:
#             The scraped text is from the career's page of a website.
#             Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
#             Only return the valid JSON.
#             ### VALID JSON (NO PREAMBLE):
#             """
#         )
#         chain_extract = prompt_extract | self.llm
#         res = chain_extract.invoke(input={"page_data": cleaned_text})
#         try:
#             json_parser = JsonOutputParser()
#             res = json_parser.parse(res.content)
#         except OutputParserException:
#             raise OutputParserException("Context too big. Unable to parse jobs.")
#         return res if isinstance(res, list) else [res]

#     def write_mail(self, job, links):
#         prompt_email = PromptTemplate.from_template(
#             """
#             ### JOB DESCRIPTION:
#             {job_description}

#             ### INSTRUCTION:
#             You are Mohan, a business development executive at AtliQ. AtliQ is an AI & Software Consulting company dedicated to facilitating
#             the seamless integration of business processes through automated tools. 
#             Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
#             process optimization, cost reduction, and heightened overall efficiency. 
#             Your job is to write a cold email to the client regarding the job mentioned above describing the capability of AtliQ 
#             in fulfilling their needs.
#             Also add the most relevant ones from the following links to showcase Atliq's portfolio: {link_list}
#             Remember you are Mohan, BDE at AtliQ. 
#             Do not provide a preamble.
#             ### EMAIL (NO PREAMBLE):

#             """
#         )
#         chain_email = prompt_email | self.llm
#         res = chain_email.invoke({"job_description": str(job), "link_list": links})
#         return res.content

# if __name__ == "__main__":
#     print(os.getenv("GROQ_API_KEY"))



import os
import json

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.exceptions import OutputParserException

load_dotenv()


class Chain:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is missing. Add it to your .env file.")

        self.llm = ChatGroq(
            temperature=0,
            api_key=api_key,
            model="openai/gpt-oss-120b",
        )

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the
            following keys: `role`, `experience`, `skills` and `description`.
            `skills` must be a list of strings.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm | JsonOutputParser()
        try:
            res = chain_extract.invoke({"page_data": cleaned_text})
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]


    def write_mail(self, job, resume_text):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### CANDIDATE RESUME (the ONLY source of facts about the candidate):
            {resume}

            ### INSTRUCTION:
            You are the candidate described in the resume above. Write a short, simple
            cold email in the first person to the HR / hiring team for the job above.

            SOURCE RULES (strict):
            - Use ONLY facts written in the resume. Never add or exaggerate any skill,
              project, company, number, or years of experience.
            - Take the name, current role, employer and contact details from the resume.
              Include only the ones that appear there.
            - If the job asks for something the resume does not show, leave it out.
              Never claim it and never apologize for it.

            CONTENT RULES:
            - Mention only the 3 or 4 points from the resume that best match the job.
              Do not summarize the resume or list all skills, projects or education.
            - Keep each point to one short line (what you worked on and with which
              technology). Skip details that are not directly relevant to this job.

            STYLE RULES:
            - Plain, simple, polite language, like a normal person writing to HR.
            - No fancy words, no buzzwords, no exaggeration, no emojis, no bullet lists.
            - Short sentences.

            FORMAT RULES:
            - First line: "Subject: ..." (short, with the job title).
            - Then: greeting, one sentence introducing yourself, the 2-3 matching points
              in a few short lines, one sentence saying you would be happy to share more
              or discuss, and a polite closing.
            - Sign off with your name and email/phone from the resume (only if present).
            - Maximum 100 words in the body.
            - No placeholders like [Your Name] or [Company]. If a detail is missing, omit it.
            - Output only the email. No preamble, no notes, no explanation.

            ### EMAIL:
            """
        )
        chain_email = prompt_email | self.llm | StrOutputParser()
        return chain_email.invoke({
            "job_description": json.dumps(job, indent=2),
            "resume": resume_text,
        })

if __name__ == "__main__":
    print("GROQ key found:", bool(os.getenv("GROQ_API_KEY")))