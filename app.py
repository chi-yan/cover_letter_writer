import streamlit as st
import coverletter
import sys
import time
import os

def main():
    st.title('Cover Letter Generator')
    # Input fields for environment variables
    openai_api_key = st.text_input('OpenAI API Key')
    serper_api_key = st.text_input('SERPER API Key (This is a Google Web Search API - get the key from serpev.dev)')

    # Set environment variables
    os.environ["OPENAI_API_KEY"] = openai_api_key
    os.environ["SERPER_API_KEY"] = serper_api_key

    # Textboxes for user input
    company_name = st.text_input('Company Name', 'Rokt')
    industry = st.text_input('Industry', 'Web Design')
    position = st.text_input('Position', 'Front-End Engineer')
    job_posting_url = st.text_input('Job Posting URL', 'https://au.talent.com/view?id=fb77f0ae8520')
    applicant_name = st.text_input('Your Name', 'Corgi Tang')

    if st.button('Generate Cover Letter'):
        result = coverletter.write_cover_letter(company_name, industry, position, job_posting_url, applicant_name)
        st.text_area('Generated Cover Letter', value=result, height=400)
        
    st.text("To fill in explaining this app: Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
if __name__ == '__main__':
    main()
