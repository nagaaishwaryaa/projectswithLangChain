import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set OpenAI base and model (adjust as needed)
client = openai.OpenAI()

# Streamlit UI
st.set_page_config(page_title="Python Code Assistant", layout="centered")
st.title("💡 Python Code Assistant")
st.markdown("Type what you want to build in Python, and get ready-to-use code!")

# User input
user_prompt = st.text_area("📝 What Python code do you want?", placeholder="e.g., Create a function to reverse a string")

# Generate button
if st.button("Generate Code"):
    if not user_prompt.strip():
        st.warning("⚠️ Please enter a prompt before generating code.")
    else:
        with st.spinner("Generating Python code..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that writes clean and working Python code."},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.3,
                    max_tokens=400
                )
                code_output = response.choices[0].message.content
                st.success("✅ Code generated below:")
                
                # Display code block
                st.code(code_output, language="python")
                
                # Copy section
               # st.text_area("📋 Copy your code here:", value=code_output, height=200)
            except Exception as e:
                st.error(f"🚨 Error: {e}")
