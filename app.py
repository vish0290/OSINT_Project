import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
from langchain.schema import Document
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain

# Load API key from .env file
load_dotenv()
api_key = os.environ["mistral_key"]

# Step 1: Load CSV with pandas
df = pd.read_csv("output.csv")

# Step 2: Convert each row into a LangChain Document
docs = [Document(page_content=str(row)) for _, row in df.iterrows()]

# Step 3: Split text into chunks
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)

# Step 4: Define embeddings
embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key=api_key)

# Step 5: Create a vector store
vector = FAISS.from_documents(documents, embeddings)

# Step 6: Define a retriever
retriever = vector.as_retriever()

# Step 7: Define the language model
model = ChatMistralAI(mistral_api_key=api_key)

# Step 8: Define the prompt template
prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

# Step 9: Create a retrieval chain
document_chain = create_stuff_documents_chain(model, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)
st.title("Startup Opinion Assistant")
user_input=st.text_input("enter your question")
if st.button("Get Answer"):
    if user_input.strip():
        response=retrieval_chain.invoke({"input":user_input})
        answer=response.get("answer", "No answer found.")
        st.subheader(f"Answer:{answer}")

    else:
        st.error("please enter a question")

# Step 10: Ask a question
# response = retrieval_chain.invoke({"input": "people opninons on startup?"})
# print(response["answer"])
