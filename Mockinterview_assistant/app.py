import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY not found. Please add it to your .env file.")
    st.stop()

# Initialize OpenAI LLM
llm = ChatOpenAI(temperature=0.7, model_name="gpt-4", api_key=api_key)

# Define Prompt Template
interview_prompt = PromptTemplate(
    input_variables=["job_role", "job_description"],
    template="""
You are an AI-powered interview assistant.

Your task is to generate a list of **mock interview questions and answers** to help someone prepare for a job interview.

Job Role: {job_role}
Job Description: {job_description}

Only include questions that fall under these categories:
- Technical skills
- Domain knowledge
- Problem-solving ability

❌ Do NOT include any behavioral, HR-based, or situational questions.

Provide:
- 5 to 8 questions
- Each with a brief, model answer

Format:
Q1: [Question]
A1: [Answer]
...
"""
)

# LangChain chain
interview_chain = LLMChain(
    llm=llm,
    prompt=interview_prompt,
    verbose=True
)

# Streamlit UI
st.set_page_config(page_title="🤖 Mock Interview Assistant", layout="centered")
st.title("🤖 Mock Interview Assistant")

st.markdown("Generate technical, domain, and problem-solving questions & answers based on the job you're preparing for.")

# User Inputs
job_role = st.text_input("Job Role*")
job_description = st.text_area("Job Description*", height=200)

# Generate Questions & Answers
if st.button("Generate Interview Q&A"):
    if not job_role.strip() or not job_description.strip():
        st.warning("Please fill in both Job Role and Job Description.")
    else:
        with st.spinner("Generating interview questions and answers..."):
            try:
                qa_output = interview_chain.run({
                    "job_role": job_role.strip(),
                    "job_description": job_description.strip()
                })
                st.subheader("📝 Mock Interview Questions & Answers")
                st.text_area("Output", qa_output, height=400)
            except Exception as e:
                st.error(f"❌ Error: {e}")
