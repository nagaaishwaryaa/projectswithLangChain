import os
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# API setup
llm = ChatOpenAI(
    api_key=os.getenv("API_KEY"),
    model_name="gpt-4o",
    temperature=0.6
)

# Prompt template
prompt = PromptTemplate(
    input_variables=["user_input"],
    template="""
    You are a helpful AI assistant.
    user says: {user_input}
    your response:
    """
)

# Chain creation
chain = LLMChain(llm=llm, prompt=prompt)

if __name__ == "__main__":
    user_input = input("Enter any question: ")
    response = chain.invoke({"user_input": user_input})
    print("AI says:", response["text"])  # ✅ Extract the actual output
