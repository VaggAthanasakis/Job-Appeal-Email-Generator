import streamlit as st
from chains import Chain
from portfolio import Portfolio
from langchain_community.document_loaders import WebBaseLoader
from utils import clean_text

# tutorial from: https://www.youtube.com/watch?v=CO4E_9V6li0&t=1025s

def create_streamlit_app(chain, portfolio):
    st.title("Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://www.logicea.com/careers/24-SQL20-gre") # value is the default
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = chain.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills',[])
                links = portfolio.query_links(skills=skills)
                CV = portfolio.insert_cv()
                email = chain.write_mail(job,CV,links)
                st.code(email,language='markdown')
        except Exception as e:
            st.error(f"An error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide",page_title="Cold Email Generator")
    create_streamlit_app(chain,portfolio)