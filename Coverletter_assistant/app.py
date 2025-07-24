import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Check API key
if not api_key:
    st.error("OPENAI_API_KEY not found. Please add it to your .env file.")
    st.stop()

# Set up the LLM
llm = ChatOpenAI(temperature=0.6, model_name="gpt-4", api_key=api_key)

# Prompt Template
cover_letter_prompt = PromptTemplate(
    input_variables=["job_title", "job_description", "company_name", "resume"],
    template="""
You are a professional cover letter writer.

Using the candidate's resume below, write a personalized and professional cover letter for a job application.

Job Title: {job_title}
Company Name: {company_name}
Job Description:
{job_description}

Candidate Resume:
{resume}

The letter should:
- Start with a greeting
- Show enthusiasm for the role
- Highlight relevant experience and skills from the resume
- Express alignment with the company and job
- End with a polite and confident closing

Keep the tone formal and engaging.
"""
)

# LangChain Chain
cover_letter_chain = LLMChain(
    llm=llm,
    prompt=cover_letter_prompt,
    verbose=True
)

# Streamlit UI
st.set_page_config(page_title="📄 Cover Letter Generator", layout="centered")
st.title("📄 AI-Powered Cover Letter Generator")

st.markdown("Fill in the required details and get a professional cover letter generated instantly.")

# Input Fields
job_title = st.text_input("Job Title*")
job_description = st.text_area("Job Description*", height=200)
resume = st.text_area("Your Resume / Summary*", height=200)
company_name = st.text_input("Company Name (Optional)")

# Button to generate cover letter
if st.button("Generate Cover Letter"):
    # Validate required fields
    if not job_title.strip() or not job_description.strip() or not resume.strip():
        st.warning("Please fill in all required fields: Job Title, Job Description, and Resume.")
    else:
        with st.spinner("Generating your cover letter..."):
            try:
                letter = cover_letter_chain.run({
                    "job_title": job_title.strip(),
                    "job_description": job_description.strip(),
                    "company_name": company_name.strip() if company_name else "the company",
                    "resume": resume.strip()
                })
                st.subheader("📬 Generated Cover Letter")
                st.text_area("Output", letter, height=350)
            except Exception as e:
                st.error(f"❌ Error: {e}")
