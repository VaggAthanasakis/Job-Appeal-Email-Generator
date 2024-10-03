
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_community.document_loaders import PyPDFLoader


class Chain:
    def __init__(self):
        self.llm = Ollama(model="llama3.1:8b", temperature = 0.1)


    def extract_jobs(self,cleaned_text):

        prompt_extract = PromptTemplate.from_template(
        """
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data}
        ### INSTRUCTION:
        The scraped text is from the career's page of a website.
        Your job is to extract the job postings and return them in JSON format containing the 
        following keys: `role`, `experience level`, `On site or not`, `skills` and `description`.
        Only return the valid JSON.
        Do not write any opening or ending phrases, return only the JSON.
        ### VALID JSON (NO PREAMBLE):    
        """
        )

        # Create the chain
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input = {'page_data':cleaned_text})

        try: 
            # Create the json
            json_parser = JsonOutputParser()
            res = json_parser.parse(res)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res,list) else [res]
    
    #######
    def write_mail(self,job,CV,links):
        promt_email = PromptTemplate.from_template(
        """
        ### JOB DESCRIPTION:
        {job_description}
        
        ### INSTRUCTION:
        You are Evangelos Athanasakis, a 
        Final year Electrical and Computer Engineering student eager to launch a career in software engineering and to work hard to gain experience and be productive both on team and individual projects.
        A quick learner, an organized and responsible person with excellent time management and ability to work under pressure in order to achieve time goals.
        You are currently working in your diploma thesis that has to do with Large Language Models.
        Your CV is the following: {CV}
        Find any potential skill from the CV in order to include them in the email but do not just provide them as a seperate answer.
        Your job is to write a cold email to the hiring company regarding the job mentioned above describing the capability
        in fulfilling their needs.
        Also, if there are relevant links add the most relevant ones from the following ones to showcase Evangelos's work portfolio: {link_list}
        Do not add any link if you have not conduct any relevant work.
        Do not provide a preamble.
        Do not write any opening or ending phrases.
        The output that you will provide must constist ONLY of the email structure.
        ### EMAIL (NO PREAMBLE):
        """
        )

        chain_email = promt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "CV": CV,"link_list": links})
        return res