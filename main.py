import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from app_main.chain import Chain
from app_main.portfolio import Portfolio
from app_main.utils import clean_text

def create_streamlit_app(llm,portfolio, clean_text):
    st.title(" cold mail generator ")
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-32222")
    submit_button = st.button("submit")

    if submit_button:
        try:
            loader = WebBaseLoader(url_input)
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get("skills", [])
                print(skills)  
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')

        except Exception as e:
            st.error(f"An Error Occured: {e}")     


if __name__=="__main__":
            chain = Chain() 
            portfolio = Portfolio()
            st.set_page_config(layout="wide",page_title="cold Email generator", page_icon="")
            create_streamlit_app(chain, portfolio, clean_text)