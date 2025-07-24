import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Safety check
if not api_key:
    st.error("Please set your OPENAI_API_KEY in a .env file")
    st.stop()

# Set up LLM
llm = ChatOpenAI(temperature=0.7, model_name="gpt-4", api_key=api_key)

# Define the prompt template
email_prompt = PromptTemplate(
    input_variables=["bullet_points", "tone"],
    template="""
You are a professional email writer.

Your task is to convert the following bullet points into a well-structured email.

The tone of the email should be {tone} (e.g., friendly, professional, polite).

Bullet Points:
{bullet_points}

Write the email below:
"""
)

# Create the LangChain LLMChain
email_chain = LLMChain(
    llm=llm,
    prompt=email_prompt,
    verbose=True
)

# Streamlit UI setup
st.set_page_config(page_title="📧 Personalized Email Writer", layout="centered")
st.title("📧 Personalized Email Writer")
st.markdown("Turn bullet points into professional and friendly emails.")

# Input fields
bullet_points = st.text_area(
    "Enter Bullet Points", 
    height=200, 
    placeholder="- Project update\n- Next steps\n- Deadline extension"
)

tone = st.selectbox("Select Tone", ["Friendly", "Professional", "Polite", "Empathetic"])

# Button to trigger email generation
if st.button("Generate Email"):
    if bullet_points.strip() == "":
        st.warning("Please enter some bullet points.")
    else:
        with st.spinner("Generating email..."):
            try:
                email = email_chain.run({"bullet_points": bullet_points, "tone": tone.lower()})
                st.subheader("✉️ Generated Email")
                st.text_area("Email Output", email, height=300)
            except Exception as e:
                st.error(f"Error generating email: {e}")
